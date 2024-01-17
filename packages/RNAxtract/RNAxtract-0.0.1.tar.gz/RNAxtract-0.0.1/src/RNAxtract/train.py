# config:utf_8

import os
os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'
import shutil
import itertools
import numpy as np
from itertools import product, permutations
import warnings

import time
import sys
import datetime
import tensorflow as tf
print(tf.__version__)
from tensorflow import keras
from tensorflow.keras.callbacks import CSVLogger, EarlyStopping, ModelCheckpoint
from tensorflow.keras.models import Model
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Lambda, Concatenate
#import tensorflow_addons as tfa
from tensorflow.keras.utils import to_categorical
from RNAxtract.model import construct_model2

warnings.filterwarnings("ignore", category=FutureWarning)
# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)
"""
author = lianlin
date = 2023/6/26
email = linlian@hectobio.com

"""
__version__ = '0.0.1'


def find_mat_recursive(wk, ends='.fast5'):
    """
    wk:directory, which contain mat files\n
    auto find all file ends with .mat
    """
    mat_lst = []
    for root, filefolder, filelist in os.walk(wk):
        for mat in filelist:
            if mat.lower().endswith(ends):
                filename = os.path.join(root, mat)
                mat_lst.append(filename)
    return mat_lst


def construct_model(n_steps_in=512,
                    num_input_features=1,
                    num_classes=12,
                    dropout_rate=0.1,
                    training=True,
                    ratio=50):
    """
    model construct
    common hyper parameter may need ???
    note:
        dropout_rate does not use here
    """
    print('num_classes', num_classes)
    main_input = keras.layers.Input(shape=(n_steps_in, n_steps_in),
                                    name='raw_signal')
    print('main_input', main_input.shape)
    x = keras.layers.Reshape([n_steps_in,n_steps_in,1])(main_input)
    # d1 = keras.layers.Conv2D(32, 3, padding='same',
    #                          activation='relu')(x)
    # d1_pool = keras.layers.MaxPool2D(2, padding='same')(d1)
    # d2 = keras.layers.Conv2D(32, 3, padding='same',
    #                          activation='relu')(d1_pool)
    # d2_pool = keras.layers.MaxPool2D(2, padding='same')(d2)
    # d3 = keras.layers.Conv2D(32, 3, padding='same',
    #                          activation='relu')(d2_pool)
    # res_input = keras.layers.MaxPool2D(2, padding='same')(d3)
    # print('res input shape', res_input.shape)

    resout1 = resblock(x,
                       bn=True,
                       bn_method='batch',
                       strides=1,
                       name='res1',
                       training=training)
    resout2 = resblock(resout1,
                       bn=True,
                       bn_method='batch',
                       strides=1,
                       name='res2',
                       training=training)
    resout3 = resblock(resout2,
                       bn=True,
                       bn_method='batch',
                       strides=1,
                       name='res3',
                       training=training)
    feashape = resout3.get_shape().as_list()
    print('cnn_feature original shape', resout3.shape)
    # cnn_feature = keras.layers.Reshape([feashape[2], feashape[3]],
    #                                    name='cnn_feature')(resout3)
    flatten = keras.layers.Flatten()(resout3)
    print('flatten shape', flatten.shape)
    lasth = keras.layers.Dense(500, activation='relu')(flatten)
    #lasth = keras.layers.Dropout(0.2)(lasth)
    output = keras.layers.Dense(num_classes, name='o1',
                                activation='softmax')(lasth)
    print('output shape', output.shape)
    predict_model = Model(inputs=main_input, outputs=output)
    return predict_model


class DataSet():
    def __init__(self, x, y, x_len, batch_size, name='train', ratio=1):
        self.x = x
        self.y = y
        self.x_len = x_len
        self.batch_size = batch_size
        self.name = name
        self.ratio = ratio
        self.segment_number, *_ = x.shape
        assert self.segment_number >= self.batch_size
        print('{} has {} segments'.format(self.name, self.segment_number))

    def shuffle_data(self, x, inx):
        x = np.array([x[i] for i in inx])
        return x

    def data_generate(self):
        start = 0
        end = self.batch_size
        while True:
            tx = self.x[start:end]
            ty = self.y[start:end]
            seq_length = self.x_len[start:end]
            start = end
            end = start + self.batch_size
            tx = tx.reshape(self.batch_size, n_steps_in, -1)
            ty = to_categorical(ty, num_classes=NUM_CLASSES)
            seq_length = seq_length.reshape(self.batch_size, -1)
            yield (tx, ty)
            if end > self.segment_number:
                start = 0
                end = self.batch_size
                shuffle_inx = np.arange(self.segment_number)
                np.random.shuffle(shuffle_inx)
                self.x = self.shuffle_data(self.x, shuffle_inx)
                self.y = self.shuffle_data(self.y, shuffle_inx)
                self.x_len = self.shuffle_data(self.x_len, shuffle_inx)


def stack_bidirectional_dynamic_rnn(resnet, layers_cellsize,
                                    seq_len_mask_data):
    """
    output all timestep result
    # Difference between bidirectional_dynamic_rnn and stack_bidirectional_dynamic_rnn
    # https://stackoverflow.com/questions/49242266/difference-between-multirnncell-and-stack-bidirectional-dynamic-rnn-in-tensorflo
    # https://github.com/tensorflow/tensorflow/issues/33683
    args:
        resnet,layer output from upper
        layers_cellsize,[cell_size,cell_size,...]
        seq_len_mask_data,true input length,mask by layers.masking
    return:
        rnn net
    """
    #tfa.rnn.LayerNormLSTMCell
    #keras.layers.LSTMCell
    output = resnet
    states = None
    for hidden_neurons in layers_cellsize:
        result = keras.layers.Bidirectional(
            keras.layers.RNN(keras.layers.LSTMCell(hidden_neurons,
                                                   activation='tanh'),
                             return_state=True,
                             return_sequences=True))(output,
                                                     states,
                                                     mask=seq_len_mask_data)
        output, states = result[0], result[1:]
    return output[:, -1, :]


def bidirectional_dynamic_rnn(resnet, layers_cellsize, seq_len_mask_data):
    """
    see stack_bidirectional_dynamic_rnn
    """
    encoder_cells = []
    for hidden_neurons in layers_cellsize:
        encoder_cells.append(
            keras.layers.LSTMCell(hidden_neurons, activation='tanh'))
    lasth = keras.layers.Bidirectional(
        keras.layers.RNN(encoder_cells,
                         return_sequences=True))(resnet,
                                                 mask=seq_len_mask_data)
    return lasth


def resblock(indata,
             training=True,
             out_channel=32,
             name='res',
             strides=1,
             bn=True,
             bn_method='global',
             active=True):
    """
    common resnet structure,usually comtain two branchs,branch1 and branch2,detail can get from google or below code
    args:
        indata,input data with shape [batch_size,1,max_time_step,feature]
        strides=1 make sure output shape equal with input shape
        bn,branch 1 normalize too
        training,whether training mode and inference mode use batch mean and variance to normalize data
        out_channel,last dime depth
    return:
        normalized and activate with relu net
    """
    fea_shape = indata.get_shape().as_list()
    in_channel = fea_shape[-1]
    print("In channel {}".format(in_channel))
    x_shortcut = convnet(indata,
                         training=training,
                         out_channel=out_channel,
                         BN=bn,
                         bn_method=bn_method,
                         active=False,
                         kernel_size=[1, 1],
                         strides=strides,
                         name=name + 'conv1')
    conv_out1 = convnet(indata,
                        training=training,
                        out_channel=out_channel,
                        bn_method=bn_method,
                        active=True,
                        BN=True,
                        kernel_size=[1, 1],
                        name=name + 'conv2a')
    conv_out2 = convnet(conv_out1,
                        training=training,
                        out_channel=out_channel,
                        bn_method=bn_method,
                        active=True,
                        BN=True,
                        kernel_size=[1, 3],
                        name=name + 'conv2b')
    conv_out3 = convnet(conv_out2,
                        training=training,
                        out_channel=out_channel,
                        bn_method=bn_method,
                        active=False,
                        BN=True,
                        kernel_size=[1, 1],
                        strides=strides,
                        name=name + 'conv2c')
    out = keras.layers.Add()([x_shortcut, conv_out3])
    out = keras.layers.Activation('relu')(out)
    return out


def convnet(net,
            training=True,
            out_channel=256,
            BN=True,
            bn_method='global',
            active=False,
            kernel_size=[1, 1],
            use_bias=False,
            strides=1,
            name='convnet'):
    """

    """
    conv = keras.layers.Conv2D(out_channel,
                               kernel_size=kernel_size,
                               use_bias=use_bias,
                               padding='same',
                               data_format='channels_last',
                               name=name,
                               strides=strides)(net)
    if BN:
        if bn_method == 'global':
            #batch size and samples difference effect is huge,in inference suggest set training=True
            conv = GlobalNormalization()(conv, training=training)
        # elif bn_method == 'group':
        #     #batch independent
        #     conv = tfa.layers.GroupNormalization()(conv)
        else:
            #batch size and samples difference effect is huge,in inference suggest set training=True
            conv = keras.layers.BatchNormalization()(conv, training=training)

    if active:
        conv = keras.layers.Activation('relu')(conv)
    return conv


class GlobalNormalization(keras.layers.Layer):
    """
    global batch normalization 
    """
    def __init__(self, **kwargs):
        super(GlobalNormalization, self).__init__()

    def get_config(self):

        config = super().get_config().copy()
        config.update({
            'name': self.name,
        })
        return config

    def build(self, input_shape):
        ksize = [input_shape[-1]]
        self.scale = self.add_weight(
            shape=ksize,
            initializer=tf.keras.initializers.variance_scaling(),
            trainable=True,
            name=self.name + "_scale")
        self.offset = self.add_weight(
            shape=ksize,
            initializer=tf.keras.initializers.variance_scaling(),
            trainable=True,
            name=self.name + "_offset")
        self.pop_mean = self.add_weight(name=self.name + 'pop_mean',
                                        shape=ksize,
                                        initializer=tf.zeros_initializer(),
                                        trainable=False)
        self.pop_var = self.add_weight(name=self.name + 'pop_var',
                                       shape=ksize,
                                       initializer=tf.zeros_initializer(),
                                       trainable=False)

    def call(self, x, decay=0.9, epsilon=1e-5, training=True):
        batch_mean, batch_var = tf.nn.moments(x, [0, 1, 2])

        def population_statistics():
            return tf.nn.batch_normalization(x, self.pop_mean, self.pop_var,
                                             self.offset, self.scale, epsilon)

        self.add_update([
            K.moving_average_update(self.pop_mean, batch_mean, decay),
            K.moving_average_update(self.pop_var, batch_var, decay)
        ])
        outputs = tf.nn.batch_normalization(x, batch_mean, batch_var,
                                            self.offset, self.scale, epsilon)
        return K.in_train_phase(outputs,
                                population_statistics,
                                training=training)


def train(batch_size=512,
          max_steps=10000,
          n_steps_in=400,
          model_path=None,
          num_input_features=1,
          num_classes=12,
          dropout_rate=0.1,
          validation_freq=20,
          ratio=20):
    K.clear_session()
    model = construct_model2(n_steps_in=n_steps_in,
                            num_input_features=num_input_features,
                            num_classes=num_classes,
                            dropout_rate=dropout_rate,
                            ratio=ratio)
    if model_path != None:
        if os.path.exists((model_path)):
            try:
                hd = find_mat_recursive(model_path, ends='.hdf5')
                hd = [[f, int(os.path.basename(f).split('_')[1])] for f in hd]
                hd = sorted(hd, key=lambda x: x[1])[-1][0]
                model.load_weights(hd)
                print('model weights reload,retrain is True')
            except Exception as e:
                print(e)
                print('can not find model, anyway just init a new graph')
        else:
            print(
                f'{model_path} does not exist,reload failed,so train from the head'
            )

    boundaries = [
        int(max_steps * LR_BOUNDARY[0]),
        int(max_steps * LR_BOUNDARY[1])
    ]
    values = [init_rate * decay for decay in [1, LR_DECAY[0], LR_DECAY[1]]]
    learning_rate_fn = keras.optimizers.schedules.PiecewiseConstantDecay(
        boundaries, values)
    optimizer = keras.optimizers.Adam(learning_rate=learning_rate_fn)

    model.compile(loss={'o1': 'categorical_crossentropy'},
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    train_data_batch = DataSet(data_x,
                               data_y,
                               data_x_len,
                               batch_size,
                               name='train').data_generate()
    valid_data_batch = DataSet(test_data_x,
                               test_data_y,
                               test_data_x_len,
                               batch_size,
                               name='validation').data_generate()
    csv_logger = CSVLogger('training.log', separator=',', append=False)
    model_checkpoint_callback = ModelCheckpoint(
        filepath="test/checkpoint_{epoch}_val_accuracy{val_accuracy:.3f}.hdf5",
        monitor='val_accuracy',
        mode='max',
        save_best_only=True)
    model.fit(train_data_batch,
              callbacks=[model_checkpoint_callback, csv_logger],
              validation_data=valid_data_batch,
              validation_steps=len(test_data_x) / batch_size,
              steps_per_epoch=len(data_x) / batch_size,
              epochs=max_steps)



if __name__ == '__main__':
    policy = tf.keras.mixed_precision.Policy('mixed_float16')
    tf.keras.mixed_precision.set_global_policy(policy)
    alphabet = 'ATCG'
    base_dir = str(datetime.datetime.now())
    base_dir = base_dir.replace(' ', '_')
    base_dir = 'test'
    base_dir += "/"
    # if os.path.exists(base_dir):
    #     shutil.rmtree(base_dir)
    # os.mkdir(base_dir)
    LR_BOUNDARY = [0.66, 0.83]
    LR_DECAY = [1e-1, 1e-2]
    init_rate = 1e-3
    validation_freq = 20
    
    max_steps = 50
    batch_size = 128
    num_input_features = 1

    all_event_val_lst = np.load('./x_p.npy', allow_pickle=True)
    all_label_val_lst = np.load('./y_p.npy', allow_pickle=True)
    all_event_length_lst = np.load('./x_len.npy', allow_pickle=True)
    
    

    poem = np.arange(len(all_event_val_lst))
    np.random.seed(0)
    np.random.shuffle(poem)
    all_event_val_lst = np.array([all_event_val_lst[i] for i in poem])
    all_label_val_lst = np.array([all_label_val_lst[i] for i in poem])
    all_event_length_lst = np.array([all_event_length_lst[i] for i in poem])
    print('has', len(all_event_val_lst), 'samples')
    inx_split = int(len(all_event_val_lst) * 0.9)

      
    data_x, data_y, data_x_len = all_event_val_lst[:inx_split], all_label_val_lst[:inx_split], \
        all_event_length_lst[:inx_split]
    test_data_x, test_data_y, test_data_x_len = all_event_val_lst[inx_split:], all_label_val_lst[inx_split:], \
        all_event_length_lst[inx_split:]
        
    NUM_CLASSES = len(np.unique(all_label_val_lst))
    n_steps_in = all_event_val_lst.shape[1]
    print('category:',NUM_CLASSES)

    train(model_path='/mnt/raid5/lla/barcode_split/truth/src/test',
          dropout_rate=0.1,
          batch_size=batch_size,
          max_steps=max_steps,
          n_steps_in=n_steps_in,
          num_input_features=num_input_features,
          num_classes=NUM_CLASSES,
          validation_freq=validation_freq,ratio=10)
