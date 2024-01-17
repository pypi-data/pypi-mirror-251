import warnings
import os
import time
from tensorflow import keras
import sys
import datetime
import tensorflow as tf
from tensorflow.python.ops import math_ops
from tensorflow.python.ops import array_ops
from tensorflow.python.framework import dtypes as dtypes_module
from keras.constraints import maxnorm
#import tensorflow_addons as tfa
from distutils.version import StrictVersion
from keras.utils.generic_utils import get_custom_objects
import numpy as np

# def glu(x):
#     cond = keras.backend.greater(x, 0)
#     return keras.backend.switch(cond, x, keras.backend.exp(x) - 1)

# get_custom_objects().update(
#     {'custom_activation': keras.layers.Activation(glu)})

# def get_padding(kernel_size, stride, dilation):
#     if stride > 1 and dilation > 1:
#         raise ValueError("Dilation and stride can not both be greater than 1")
#     return (kernel_size // 2) * dilation


def activation(x, dropout=0.05):
    x = keras.layers.Activation("swish")(x)
    x = keras.layers.Dropout(dropout)(x)
    return x


def convnet(
    x,
    out_channel=256,
    strides=1,
    kernel_size=1,
    bn_method="batch",
    dilation=1,
    active=True,
):
    x = keras.layers.Conv1D(out_channel,
                            kernel_size=kernel_size,
                            padding="same",
                            strides=strides)(x)
    x = keras.layers.BatchNormalization(axis=-1, momentum=0.1,
                                        epsilon=0.001)(x)
    if active:
        x = activation(x)
    return x


def DepthwiseConv1D(x, kernel_size=1):
    x = keras.layers.Lambda(lambda x: keras.backend.expand_dims(x, axis=1))(x)
    x = keras.layers.DepthwiseConv2D(kernel_size=[kernel_size, 1],
                                     padding="same")(x)
    x = keras.layers.Lambda(lambda x: keras.backend.squeeze(x, axis=1))(x)
    return x


def Conv1DTranspose(input_tensor,
                    filters,
                    kernel_size=1,
                    strides=1,
                    padding="same"):
    """
    input_tensor: tensor, with the shape (batch_size, time_steps, dims)
    filters: int, output dimension, i.e. the output tensor will have the shape of (batch_size, time_steps, filters)
    kernel_size: int, size of the convolution kernel
    strides: int, convolution step size
    padding: 'same' | 'valid'
    """
    x = keras.layers.Lambda(lambda x: keras.backend.expand_dims(x, axis=2))(
        input_tensor)
    x = keras.layers.Conv2DTranspose(
        filters=filters,
        kernel_size=(kernel_size, 1),
        strides=(strides, 1),
        padding=padding,
    )(x)
    x = keras.layers.Lambda(lambda x: keras.backend.squeeze(x, axis=2))(x)
    return x


def block1(x, config):
    in_channel = x.shape[-1]
    filter = config["filter"]
    kernel_size = config["kernel_size"]
    print(in_channel, config)
    shortcut = convnet(x,
                       out_channel=filter * 4,
                       strides=1,
                       kernel_size=1,
                       active=False)
    x2 = convnet(x, kernel_size=3, strides=3,
                 out_channel=filter * 4)  # downsampling
    print("downsampling x2", x2.shape)
    x2 = DepthwiseConv1D(x2, kernel_size=kernel_size)
    print("DepthwiseConv1D 1 shape", x2.shape)
    x2 = keras.layers.BatchNormalization(axis=-1, momentum=0.1,
                                         epsilon=0.001)(x2)
    x2 = activation(x2)
    for i in range(config["repeat"]):
        x2 = keras.layers.SeparableConv1D(filter * 4,
                                          kernel_size=kernel_size,
                                          padding="same")(x2)
        x2 = keras.layers.BatchNormalization(axis=-1,
                                             momentum=0.1,
                                             epsilon=0.001)(x2)
        x2 = activation(x2)
    x2 = DepthwiseConv1D(x2, kernel_size=kernel_size)
    print("DepthwiseConv1D 2 shape", x2.shape)
    x2 = Conv1DTranspose(x2, filter * 4, kernel_size=3,
                         strides=3)  # upsampling
    x2 = keras.layers.BatchNormalization(axis=-1, momentum=0.1,
                                         epsilon=0.001)(x2)
    out = keras.layers.Add()([shortcut, x2])
    out = activation(out)
    return out


def block2(x, config, dropout=0.05):
    in_channel = config["in_channel"] #x.shape[-1]
    filter = config["filter"]
    kernel_size = config["kernel_size"]
    print(in_channel, config)
    shortcut = convnet(x,
                       out_channel=filter,
                       strides=1,
                       kernel_size=1,
                       active=False)
    x2 = x
    for i in range(config["repeat"] - 1):
        x2 = keras.layers.SeparableConv1D(filter,
                                          kernel_size=kernel_size,
                                          padding="same")(x2)
        x2 = keras.layers.BatchNormalization(axis=-1,
                                             momentum=0.1,
                                             epsilon=0.001)(x2)
        x2 = activation(x2)
    x2 = keras.layers.SeparableConv1D(filter, kernel_size, padding="same")(x2)
    x2 = keras.layers.BatchNormalization(axis=-1, momentum=0.1,
                                         epsilon=0.001)(x2)
    out = keras.layers.Add()([shortcut, x2])
    out = activation(out)
    return out


def blockselect(x, config):
    if config["type"] == "heron":
        return block1(x, config)
    else:
        return block2(x, config)


def construct_model2(
    n_steps_in=1536,
    num_input_features=1,
    num_classes=4,
    dropout_rate=0.1,
    ratio=3,
    training=True,
    block_type="quartznet",
):
    max_step_length = int(n_steps_in / ratio)
    main_input = keras.layers.Input(shape=(n_steps_in, num_input_features),
                                    name="raw_signal")
    
    x = keras.layers.Conv1D(32, 9, padding='same',
                             activation='relu')(main_input)
    x = keras.layers.MaxPool1D(2, padding='same')(x)
    x = keras.layers.Conv1D(64, 9, padding='same',
                             activation='relu')(x)
    x = keras.layers.MaxPool1D(2, padding='same')(x)
    x = keras.layers.Conv1D(64, 3, padding='same',
                             activation='relu')(x)
    x = keras.layers.MaxPool1D(2, padding='same')(x)
    
    print("main_input", main_input.shape)
    #x = convnet(x, out_channel=344, kernel_size=9, strides=1)
    print("block input shape", x.shape)
    x = blockselect(x,
                    config={
                        "filter": 128,
                        "kernel_size": 3,
                        "repeat": 8,
                        "type": block_type,
                        "in_channel":344,
                    })
    x = blockselect(x,
                    config={
                        "filter": 64,
                        "kernel_size": 6,
                        "repeat": 8,
                        "type": block_type,
                        "in_channel":424,
                    })
    x = blockselect(x,
                    config={
                        "filter": 128,
                        "kernel_size": 12,
                        "repeat": 2,
                        "type": block_type,
                        "in_channel":464,
                    })
    x = blockselect(x,
                    config={
                        "filter": 64,
                        "kernel_size": 3,
                        "repeat": 8,
                        "type": block_type,
                        "in_channel":456,
                    })
    x = blockselect(x,
                    config={
                        "filter": 64,
                        "kernel_size": 12,
                        "repeat": 8,
                        "type": block_type,
                        "in_channel":440,
                    })

    

    x = keras.layers.SeparableConv1D(128, kernel_size=64, padding="same")(x)
    x = keras.layers.BatchNormalization(axis=-1, momentum=0.1,
                                        epsilon=0.001)(x)
    x = activation(x)
    x = convnet(x, out_channel=64, kernel_size=3, strides=4)
   
    print('flatten input shape',x.shape)
    x = keras.layers.Bidirectional(keras.layers.LSTM(32, return_sequences=False))(x)
    x = keras.layers.Flatten()(x)
    print('flatten shape', x.shape)
    x = keras.layers.Dense(512, activation='relu')(x)
    output = keras.layers.Dense(num_classes, name='o1',
                                activation='softmax',dtype='float32')(x)
    
    print('output shape', output.shape)
    predict_model = keras.models.Model(inputs=main_input, outputs=output)
    return predict_model


def k_ctc_lambda_func(args):
    """
    ctc compute,number_classes -1 as blank
    args:
        y_pred, labels, input_length, label_length = args
        input may need sure shape
    return:
        ctc loss
    """
    fl_gamma = 2
    y_pred, labels, input_length, label_length = args
    loss = keras.backend.ctc_batch_cost(labels, y_pred, input_length,
                                        label_length)
    if fl_gamma > 0:
        if StrictVersion(tf.__version__) >= StrictVersion("1.11.0"):
            loss = tf.math.pow(1 - tf.math.exp(-loss), fl_gamma) * loss
        else:
            loss = tf.pow(1 - tf.exp(-loss), fl_gamma) * loss
    loss = tf.reduce_mean(loss)
    return loss


def tf_ctc_lambda_func(args):
    """
    0 as blank index

    Args:
        args (_type_): _description_

    Returns:
        _type_: _description_
    """

    fl_gamma = 2
    logits, labels, logit_length, label_length = args
    label_length = math_ops.cast(array_ops.squeeze(label_length, axis=-1),
                                 dtypes_module.int32)
    logit_length = math_ops.cast(array_ops.squeeze(logit_length, axis=-1),
                                 dtypes_module.int32)
    labels = math_ops.cast(
        labels,
        dtypes_module.int32,
    )
    sparse_labels = math_ops.cast(
        keras.backend.ctc_label_dense_to_sparse(labels, label_length),
        dtypes_module.int32,
    )

    loss = tf.nn.ctc_loss(
        sparse_labels,
        logits,
        label_length=label_length,
        logit_length=logit_length,
        logits_time_major=False,
        blank_index=-1,
    )
    if fl_gamma > 0:
        if StrictVersion(tf.__version__) >= StrictVersion("1.11.0"):
            loss = tf.math.pow(1 - tf.math.exp(-loss), fl_gamma) * loss
        else:
            loss = tf.pow(1 - tf.exp(-loss), fl_gamma) * loss
    loss = tf.reduce_mean(loss)
    return loss


@tf.function()
def dense_to_sparse(dense):
    # Only elements not equal to zero will be present in the result
    sparse = tf.sparse.from_dense(dense)
    return sparse


def stack_bidirectional_dynamic_rnn(resnet, layers_cellsize,
                                    seq_len_mask_data):
    """
    output all timestep result
    # Difference between bidirectional_dynamic_rnn and stack_bidirectional_dynamic_rnn
    # https://stackoverflow.com/questions/49242266/difference-between-multirnncell-and-stack-bidirectional-dynamic-rnn-in-tensorflo

    args:
        resnet,layer output from upper
        layers_cellsize,[cell_size,cell_size,...]
        seq_len_mask_data,true input length,mask by layers.masking
    return:
        rnn net
    """
    # tfa.rnn.LayerNormLSTMCell
    # keras.layers.LSTMCell
    output = resnet
    states = None
    for hidden_neurons in layers_cellsize:
        result = keras.layers.Bidirectional(
            keras.layers.RNN(
                keras.layers.LSTMCell(hidden_neurons, activation="tanh"),
                return_state=True,
                return_sequences=True,
            ))(output, states, mask=seq_len_mask_data)
        output, states = result[0], result[1:]
    return output


def bidirectional_dynamic_rnn(resnet, layers_cellsize, seq_len_mask_data):
    """
    see stack_bidirectional_dynamic_rnn
    """
    encoder_cells = []
    for hidden_neurons in layers_cellsize:
        encoder_cells.append(
            keras.layers.LSTMCell(hidden_neurons, activation="tanh"))
    lasth = keras.layers.Bidirectional(
        keras.layers.RNN(encoder_cells,
                         return_sequences=True))(resnet,
                                                 mask=seq_len_mask_data)
    return lasth


class GlobalNormalization(keras.layers.Layer):
    """
    global batch normalization
    """

    def __init__(self, **kwargs):
        super(GlobalNormalization, self).__init__()

    def get_config(self):

        config = super().get_config().copy()
        config.update({
            "name": self.name,
        })
        return config

    def build(self, input_shape):
        ksize = [input_shape[-1]]
        self.scale = self.add_weight(
            shape=ksize,
            initializer=tf.keras.initializers.variance_scaling(),
            trainable=True,
            name=self.name + "_scale",
        )
        self.offset = self.add_weight(
            shape=ksize,
            initializer=tf.keras.initializers.variance_scaling(),
            trainable=True,
            name=self.name + "_offset",
        )
        self.pop_mean = self.add_weight(
            name=self.name + "pop_mean",
            shape=ksize,
            initializer=tf.zeros_initializer(),
            trainable=False,
        )
        self.pop_var = self.add_weight(
            name=self.name + "pop_var",
            shape=ksize,
            initializer=tf.zeros_initializer(),
            trainable=False,
        )

    def call(self, x, decay=0.9, epsilon=1e-5, training=True):
        batch_mean, batch_var = tf.nn.moments(x, [0, 1, 2])

        def population_statistics():
            return tf.nn.batch_normalization(x, self.pop_mean, self.pop_var,
                                             self.offset, self.scale, epsilon)

        self.add_update([
            K.moving_average_update(self.pop_mean, batch_mean, decay),
            K.moving_average_update(self.pop_var, batch_var, decay),
        ])
        outputs = tf.nn.batch_normalization(x, batch_mean, batch_var,
                                            self.offset, self.scale, epsilon)
        return K.in_train_phase(outputs,
                                population_statistics,
                                training=training)
