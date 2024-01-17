from ont_fast5_api.fast5_interface import get_fast5_file
import os
import sys
import numpy as np
import pandas as pd
import h5py
import RNAxtract.constants as CONSTANTS
from multiprocessing import Pool
from collections import defaultdict
import ruptures as rpt 
import scipy 


# bar = {}
# with open('../barcode.txt','r') as f:
#     for i in f:
#         barcode,seq = i.strip().split()
#         bar[barcode] = seq
        
        
def find_mat_recursive(wk, ends='.mat'):
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


def read_signal(signal, normalize="median"):
    signal = np.asarray(signal)
    if len(signal) == 0:
        return signal.tolist()
    if normalize == "mean":
        signal = (signal - np.mean(signal)) / float(np.std(signal))
    elif normalize == "median":
        #signal = (signal - np.median(signal)) / float(robust.mad(signal))
        value_m = np.median(signal)
        mad = np.median(np.abs(signal - value_m)) * 1.4826 + 1e-6
        signal = (signal - value_m) / mad
        #if mad == 0:print(value_m,mad)
    return signal.tolist()



def dRNA_segmenter(readID, signal, w):
    '''
    segment signal/s and return coords of cuts
    '''
    def _scale_outliers(squig):
        ''' Scale outliers to within m stdevs of median '''
        k = (squig > 0) & (squig < 1200)
        return squig[k]


    sig = _scale_outliers(np.array(signal, dtype=int))

    s = pd.Series(sig)
    t = s.rolling(window=w).mean()
    # This should be done better, or changed to median and benchmarked
    # Currently trained on mean segmented data
    # Make it an argument for user to choose in training/dmux and config
    mn = t.mean()
    std = t.std()
    # Trained on 0.5
    bot = mn - (std*0.5)

    # main algo
    # TODO: add config for these for users to fiddle with
    begin = False
    # max distance for merging 2 segs
    seg_dist = 1500
    # max length of a seg
    hi_thresh = 200000
    # min length of a seg
    lo_thresh = 2000

    start = 0
    end = 0
    segs = []
    count = -1
    for i in t:
        count += 1
        if i < bot and not begin:
            start = count
            begin = True
        elif i < bot:
            end = count
        elif i > bot and begin:
            if segs and start - segs[-1][1] < seg_dist:
                segs[-1][1] = end
            else:
                segs.append([start, end])
            start = 0
            end = 0
            begin = False
        else:
            continue

    # offset = -1050
    # buff = 150
    # half the window - probs should be offset = w / 2
    offset = -1000
    buff = 0

    x, y = 0, 0

    for a, b in segs:
        if b - a > hi_thresh:
            continue
        if b - a < lo_thresh:
            continue
        x, y = a, b

        # to be modified in next major re-training
        return [x+offset-buff, y+offset+buff]
        break
    return 0

def get_rta(read_id,raw_data, max_signal_length):
    
    
    
    # #1 find polyA
    # try:
    #     polya_p = read.get_analysis_attributes('Segmentation_000/Summary/segmentation')['first_sample_template']
    #     if polya_p < 2000 or polya_p > 20000: 
    #         print(polya_p)
    #         return False, ''
    # except KeyError:
    #     result,_ = scipy.signal.find_peaks(raw_data, 100, width=100)
    #     if len(result) == 0: return False, ''
    #     try:
    #         polya_p = result[(result > 2000) & (result < 20000)][0]
    #     except IndexError:
    #         return False, ''
    
    seg = dRNA_segmenter(read_id, raw_data, 2000)
    if not seg:
        print('no seg',read_id)
        return False, ''
    
    #2 get adaptor+barcode
    rta = raw_data[seg[0]:seg[1]]

    
    #3 only barcode
    rta = rta[int(0.50*len(rta)):][:max_signal_length]
    
    
    # if len(rta) > max_signal_length: 
    #     if len(rta) > max_signal_length :print("long",len(rta))
    #     return False, ''
         
    #4 smooth
    #rta = scipy.signal.medfilt(rta,9)
    
    return True, rta

def print_all_raw_data(fast5_filepath, read_id_mapped, max_signal_length=10000):
    event_lst = []
    event_length_lst = []
    label_lst = []
    with get_fast5_file(fast5_filepath, mode="r") as f5:
        for read in f5.get_reads():
            
            raw_data = read.get_raw_data(scale=True)
            read_id = read.read_id

            
            try:
                label = read_id_mapped[read_id]
            except KeyError:
                continue

            success, rta = get_rta(read,max_signal_length)
            if not success: continue
            
            rta = read_signal(rta)
            signal_length = len(rta)
            
            try:
                rta = np.pad(rta, [0, max_signal_length - signal_length],
                                constant_values=[CONSTANTS.PAD])
            except ValueError:
                print('rta signal length',len(rta))
                

            event_lst.append(rta)
            event_length_lst.append(signal_length)
            label_lst.append(label)
    if len(event_length_lst) == 0:
        success = False
    else:
        success = True
    return success, event_lst, event_length_lst, label_lst


def label_data(CHAR_TO_INT=CONSTANTS.CHAR_TO_INT):
    mapping = {}
    label_count = defaultdict(int)
    
    with open(label_path, 'r') as f:

        for inx,i in enumerate(f):
            if inx == 0:continue
            gene,read_id, label,name,width = i.strip().split()
            #print(CHAR_TO_INT)
            if label not in CHAR_TO_INT:continue
            try:
                if label_count[label] < 1e4:
                    label_count[label] += 1
                    mapping[read_id] = CHAR_TO_INT[label]
            except Exception as e:
                print(e)
                continue
    print('label number:',len(label_count))
    print(label_count)
    return mapping


def main(wk):
    mat_lst = find_mat_recursive(wk, ends='.fast5')
    read_id_mapped = label_data()
    #return
    x, x_len, y = [], [], []
    results = []
    pool = Pool(32)
    for fast5_path in mat_lst:
        # success,event_lst, event_length_lst, label_lst = print_all_raw_data(
        #     fast5_path, read_id_mapped)
        result = pool.apply_async(print_all_raw_data,
                                  args=(
                                      fast5_path,
                                      read_id_mapped,
                                  ))
        results.append(result)
    pool.close()
    pool.join()
    for r in results:
        success, event_lst, event_length_lst, label_lst = r.get()
        if success:
            x += event_lst
            x_len += event_length_lst
            y += label_lst
    x = np.array(x)
    x_len = np.array(x_len)
    y = np.array(y)
    np.save('./x_p.npy', x)
    np.save('./x_len.npy', x_len)
    np.save('./y_p.npy', y)
    print('x shape:', x.shape)
    print('unique:', np.unique(y, return_counts=True))


if __name__ == '__main__':
    #contain barcode,2020
    #no barcode or same barcode,2021
    wk = sys.argv[1]
    label_path = sys.argv[2]
    main(wk)
