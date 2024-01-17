from tensorflow.keras.models import load_model, Model
import numpy as np
import os
import h5py
from tensorflow import keras
import tensorflow as tf
from tensorflow.keras import backend as K
import time
import RNAxtract.constants as CONSTANTS
from ont_fast5_api.fast5_interface import get_fast5_file
from RNAxtract.train_data import read_signal,get_rta
from multiprocessing import Pool 
from RNAxtract.model import construct_model2
import argparse
import RNAxtract
import warnings
warnings.filterwarnings("ignore")

physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("fast5_directory", help="directory containing fast5 files")
    parser.add_argument("--threshold", type=float, help="threshold value", default=0)
    parser.add_argument("--batch_size", type=int, default=512, help="batch size (default: 512)")
    parser.add_argument("--max_signal_length", type=int, default=10000, help="maximum signal length (default: 10000)")
    return parser.parse_args()



def get_fast5_file2(fast5_filepath, scale=False):
    
    def get_scale(channel_info,raw, scale=True):
        if scale:
            digi = channel_info['digitisation']
            parange = channel_info['range']
            offset = channel_info['offset']
            scaling = parange / digi
            # python slice syntax allows None, https://docs.python.org/3/library/functions.html#slice
            raw = np.array(scaling * (raw + offset), dtype=np.float32)
        return raw

    def fast5v(fast5_filepath):
        with h5py.File(fast5_filepath,'r') as h5:
            for read in h5:
                if read.startswith('read_'):
                    return 1 
                else: 
                    return 0
                
    def parse(fast5_filepath, scale=False):
        c = fast5v(fast5_filepath)
        if c:
            with h5py.File(fast5_filepath,'r') as h5:
                for read in h5:
                    try:
                        read_id = read.replace('read_','')
                        raw = h5[read]
                        raw = raw['Raw/Signal']
                        channel_info = h5[read]['channel_id'].attrs
                        raw = get_scale(channel_info, raw, scale=scale) 
                    except :continue
                    yield read_id, raw
        else:
            with h5py.File(fast5_filepath,'r') as h5:
                read = list(h5["Raw/Reads"].values())[0]
                read_id = read.attrs['read_id'].decode()
                raw = read["Signal"]
                channel_info = h5['UniqueGlobalKey/channel_id'].attrs
                raw = get_scale(channel_info, raw, scale=scale) 
                yield read_id, raw
                
    return parse(fast5_filepath, scale=scale)

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


def load_read_data(fast5_filepath, max_signal_length=10000):
    """
    #awesomely here,use normalize=True,I am not sure why it does not use median normalization

    Args:
        read_file ([type]): [description]
        platform (str, optional): [description]. Defaults to 'kq'.

    Returns:
        [type]: [description]
    """
    filename = os.path.basename(fast5_filepath)
    x = []
    try:
        # with get_fast5_file(fast5_filepath, mode="r") as f5:
            
        #     for read in f5.get_reads():
                
        #         #raw_data = read.get_raw_data(scale=True)
        #         read_id = read.read_id

        #         success,rta = get_rta(read,max_signal_length)
        #         if not success: continue
        #         rta = read_signal(rta)
        #         x.append([True, filename,read_id,rta])
        
        for read_id, raw in get_fast5_file2(fast5_filepath):
            success, rta = get_rta(read_id, raw, max_signal_length)
            if not success: continue
            rta = read_signal(rta)
            #print(len(rta))
            x.append([True, filename,read_id,rta])
        
    except Exception as e:
        print(e)
        return x #.append([False,1,1,1])
    return x     
    



def flatten(items):
    for x in items:
        # 终止条件，检验是否为可迭代对象
        if hasattr(x, '__iter__'):
            yield from flatten(x)
        else:
            yield x


def basecall(x_lst, fo):
    try:
        
        filename_lst = x_lst[:,0]
        read_id_lst = x_lst[:, 1]
        data = x_lst[:, 2]
        samples = len(data)
        batch_data = np.array(
            [data[i:i + batch_size] for i in range(0, samples, batch_size)],dtype=object)
        batch_read_id_lst = np.array([
            read_id_lst[i:i + batch_size]
            for i in range(0, samples, batch_size)
        ],dtype=object)
        
        batch_filename_lst = np.array([
            filename_lst[i:i + batch_size]
            for i in range(0, samples, batch_size)
        ],dtype=object)
        assert len(batch_data) == len(batch_read_id_lst)
        for inx, batch_input in enumerate(batch_data):
            fast5 = batch_filename_lst[inx]
            batch_id = batch_read_id_lst[inx]
            batch_label, batch_prob = predict(batch_input)
            
            for inx, read_id in enumerate(batch_id):
                label = batch_label[inx]
                cm = confidence_margin(batch_prob[inx])
                if np.max(batch_prob[inx]) < threshold: label = 'unknown'
                prob = [str(i) for i in batch_prob[inx]]
                prob = '\t'.join(prob)
                print(f'{fast5[inx]}\t{read_id}\t{label}\t{cm}\t{prob}', file=fo)

    except Exception as e:
        print(e)
        return


def predict(data):

    x2 = keras.preprocessing.sequence.pad_sequences(data,
                                                    maxlen=n_steps_in,
                                                    value=CONSTANTS.PAD,
                                                    padding='post',
                                                    dtype='float32')
    batch_prob = model.predict(x2, batch_size=batch_size)
    batch_label = np.argmax(batch_prob, axis=1)
    batch_label = np.array(
        [CONSTANTS.INT_TO_DEEPLEXICONCHAR[label] for label in batch_label])
    return batch_label, batch_prob


def model_load():
    package_path = os.path.dirname(os.path.abspath(RNAxtract.__file__))
    model_path = os.path.join(package_path, "model/ont.RNA.r94.hdf5")
    print(model_path)
    model = keras.models.load_model(model_path)
    model.summary()
    return model


def confidence_margin(npa):
    sorted = np.sort(npa)[::-1]    #return sort in reverse, i.e. descending
    # sorted = np.sort(npa)   #return sort in reverse, i.e. descending
    d = sorted[0] - sorted[1]
    return(d)

def main():
    fo = open('./predict.txt', 'w')
    all_fast5 = find_mat_recursive(fast5_directory)
    poem = np.arange(len(all_fast5))
    all_fast5 = [all_fast5[i] for i in poem]
    
    start = time.time()
    c = 0
    
    x_lst = []
    pool = Pool(32)
    results = []
    for fast5 in all_fast5:
        print(fast5)
        result = pool.apply_async(load_read_data,args=(fast5,max_signal_length,))
        results.append(result)
        #break
    pool.close()
    pool.join()
    for r in results:
        x = r.get()
        if len(x) == 0:continue
        for success, filename, read_id, data in x:
            if success:
                c += 1
                x_lst.append([filename, read_id, data])
    x_lst = np.array(x_lst, dtype=object)        
    np.save('./thirdsam.npy',x_lst)
    
    #x_lst = np.load('./thirdsam.npy',allow_pickle=True)    
    #x_lst = np.load('./24sam.npy',allow_pickle=True) 

    print("{}\t{}\t{}\t{}\t{}".format("fast5", "ReadID", "Barcode", "Confidence Interval", "\t".join(["P_bc_{}".format(i) for i in range(1, len(CONSTANTS.CHAR_TO_INT)+1)])), file=fo)
    x_lst = np.array(x_lst, dtype=object)
    if len(x_lst) != 0:
        basecall(x_lst, fo)
    fo.close()
    end = time.time()
    print('cost time', end - start)
    print('total passed reads', c)
    print('classy speed (n/s)', c / (end - start))
    


if __name__ == "__main__":
    K.set_floatx('float16')
    args = get_args()
    fast5_directory = args.fast5_directory
    threshold = args.threshold
    batch_size = args.batch_size
    max_signal_length = n_steps_in = args.max_signal_length
    model = model_load()
    main()
    print(__file__)
