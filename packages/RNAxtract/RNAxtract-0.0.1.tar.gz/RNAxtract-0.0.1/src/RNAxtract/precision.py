#config:utf_8

import os
import json
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score
import sys
import argparse
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt
import RNAxtract.constants as CONSTANTS
import pandas as pd
import seaborn as sns
"""
读取一个金标准，一个检测结果，计算匹配结果中的precision,recall,f1值

"""

#python precision.py --true ../test_label.txt --predict uti.txt -n 24

def get_args():
    parser = argparse.ArgumentParser(description='signal demultiplexing')
    parser.add_argument('--true', '-t', help='true data', required=True)
    parser.add_argument('--predict', '-p', help='predict data', required=True)
    parser.add_argument('--num_classes',
                        '-n',
                        help='tag number',
                        default=24,
                        type=int,
                        required=False)
    args = parser.parse_args()
    return args


def get_data(file, test=False, cutoff=0.1):
    result = {}
    prob = []
    total = 0
    up = 0
    with open(file, 'rt') as f:
        f.readline()
        for inx,i in enumerate(f):
            total += 1
            line = i.strip().split()
            if len(line) != 0:
                if test:
                    read_id = line[1]
                    tax = line[2]
                    label_prob = line[4:]
                    label_prob = list(map(float, label_prob))
                    nan_indices = np.isnan(label_prob)
                    cm = float(line[3])
                    if cm < cutoff or sum(nan_indices) > 0:continue
                    up += 1
                    result[read_id] = np.argmax(label_prob)
                    prob.append(label_prob)
                else:
                    read_id = line[1]
                    tax = line[2]
                    if tax not in CONSTANTS.CHAR_TO_INT:continue
                    result[read_id] = CONSTANTS.CHAR_TO_INT[tax] # 因为我们用的是deeplexicon的解码工具

    recovery = None
    if test:
        recovery = up / total
        print(f'高于{cutoff}比例：', recovery)
    return result, prob, recovery


def evaluation(pred_data, true_data, prob=None):
    y_true = []
    y_pred = []
    y_pred_probs = []
    for inx, read_id in enumerate(pred_data):
        if read_id in true_data:
            y_true.append(true_data[read_id])
            y_pred.append(pred_data[read_id])
            if prob != None:
                y_pred_probs.append(prob[inx])
        else:
            pass
            #print(read_id)
    assert len(y_true) != 0, 'data not match'

    # y_true = [CONSTANTS.DEEPLEXICONCHAR_TO_INT[i] for i in y_true]
    # y_pred = [CONSTANTS.DEEPLEXICONCHAR_TO_INT[i] for i in y_pred]
    y_true_reserve = set(y_true) - set(y_pred)
    y_pred_reserve = set(y_pred) - set(y_true)

    print('真实集独有：', len(y_true_reserve), y_true_reserve)
    print('验证集独有：', len(y_pred_reserve), y_pred_reserve)
    if len(y_true_reserve) != 0:
        print('警告！标签不对应！！！模型准确性不好')



    conf_matrix = confusion_matrix(y_true, y_pred, labels=range(num_classes))
    weighted_accuracy, weighted_fp = multi_level_test(conf_matrix)
    np.save('./conf_matrix.npy', conf_matrix)
    assert prob != None, 'prob is not None'
    fpr, tpr, auc = auc_plot(
        to_categorical(y_true, num_classes=num_classes).ravel(),
        np.array(y_pred_probs).ravel())
    cumulative_prob(y_pred_probs)

    return weighted_accuracy,weighted_fp, auc


def multi_level_test(conf_matrix):
    labels = range(num_classes)
    labels = [CONSTANTS.INT_TO_CHAR[i] for i in labels]
    conf_matrix = pd.DataFrame(conf_matrix, index=labels, columns=labels)

    plt.figure(figsize=(15, 6))
    plt.title('confusion matrix')
    sns.heatmap(conf_matrix, annot=True)
    plt.tight_layout()
    plt.savefig('conf_matrix.png')
    plt.clf()

    recall = conf_matrix.apply(lambda s: round(s / sum(s), 2), axis=1)
    plt.figure(figsize=(8, 6))
    plt.title('recall')
    sns.heatmap(recall, annot=True)
    plt.tight_layout()
    plt.savefig('recall.png')
    plt.clf()

    precision = conf_matrix.apply(lambda s: round(s / sum(s), 2), axis=0)
    plt.figure(figsize=(8, 6))
    plt.title('precision')
    sns.heatmap(precision, annot=True)
    plt.tight_layout()
    plt.savefig('precision.png')
    plt.clf()

    metrics = {}
    for label in recall.index:
        recall_val = recall.loc[label, label]
        precision_val = precision.loc[label, label]
        f = 2 * recall_val * precision_val / (recall_val + precision_val)
        tp = conf_matrix.loc[label, label]
        fn = sum(conf_matrix.loc[label, :]) - tp
        fp = sum(conf_matrix.loc[:, label]) - tp
        tn = 0
        support = tp + fn + tn
        accuracy = (tp + tn) / (tp + fp + tn + fn)
        fpr = (fp) / (tp + fp + tn + fn)
        metrics[label] = [precision_val, recall_val, accuracy, f, support, fpr, fn]

    classification_reports = pd.DataFrame.from_dict(metrics).T
    classification_reports.columns = [
        'precision', 'recall', 'accuracy', 'f1-score', 'support','fpr','fn'
    ]
    #print(classification_reports)
    classification_reports = classification_reports.fillna(0)
    #print(classification_reports)
    # 8-rta21 16-rta32 18-rta35 23-rta45
    plt.figure(figsize=(8, 6))
    
    weighted_accuracy = sum(
        classification_reports['accuracy'] * classification_reports['support']
    ) / classification_reports['support'].sum()
    
    
    weighted_fp = sum(
        classification_reports['fpr'] * classification_reports['support']
    ) / classification_reports['support'].sum()
    
    sns.heatmap(
        classification_reports[['precision', 'recall', 'accuracy',
                                'f1-score']],
        annot=True)
    plt.tight_layout()
    plt.savefig('classification_reports.png')
    plt.clf()
    print('weighted_accuracy', weighted_accuracy)
    return weighted_accuracy, weighted_fp


def auc_plot(y, prob, model='cnn'):
    """
    y:真实标签，one-hot类型
    prob:各个分类标签的概率
    备注：
    用来画auc曲线，计算每个分类下的auc，然后取平均值


    """
    
    # ROC CURVE 

    # nan_indices = np.isnan(prob)
    # print(sum(nan_indices))
    
    fpr, tpr, thresholds = metrics.roc_curve(y, prob)
    auc = metrics.auc(fpr, tpr)
    plt.plot(fpr, tpr, c='r', lw=2, alpha=0.7, label=u'AUC=%.3f' % auc)
    plt.plot((0, 1), (0, 1), c='#808080', lw=1, ls='--', alpha=0.7)
    plt.xlim((-0.01, 1.02))
    plt.ylim((-0.01, 1.02))
    plt.xticks(np.arange(0, 1.1, 0.1))
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.xlabel('Specificity', fontsize=13)
    plt.ylabel('Sensitivity', fontsize=13)
    plt.grid(b=True, ls=':')
    plt.legend(loc='lower right', fancybox=True, framealpha=0.8, fontsize=12)
    plt.tight_layout()
    plt.savefig('{}_roc.png'.format(model), dpi=400)
    plt.close()
    
    # PRC CURVE
    precision, recall, thresholds = metrics.precision_recall_curve(y, prob)
    auc = metrics.auc(recall,precision)
    plt.plot(recall,precision, c='r', lw=2, alpha=0.7, label=u'AUC=%.3f' % auc)
    plt.plot((0, 1), (0, 1), c='#808080', lw=1, ls='--', alpha=0.7)
    plt.xlim((-0.01, 1.02))
    plt.ylim((-0.01, 1.02))
    plt.xticks(np.arange(0, 1.1, 0.1))
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.xlabel('Recall', fontsize=13)
    plt.ylabel('Precision', fontsize=13)
    plt.grid(b=True, ls=':')
    plt.legend(loc='lower right', fancybox=True, framealpha=0.8, fontsize=12)
    plt.tight_layout()
    plt.savefig('{}_prc.png'.format(model), dpi=400)
    plt.close()
    return fpr, tpr, auc


def cumulative_prob(prob, model='cnn'):
    prob = np.max(prob, 1)
    plt.hist(prob, cumulative=True, histtype='step', density=True)
    #plt.vlines(0.95, 0, 1, colors='red')
    plt.xlabel('probability')
    plt.ylabel('percent(%)')
    plt.title('classification probability cumulative plot')
    plt.savefig('{}_prob_cumulative.png'.format(model), dpi=400)
    plt.close()

def fstat(args):
    
    pred_data = args.predict
    true_data = args.true
    num_classes = args.num_classes
    context = []
    for c in np.linspace(0, 1, 10):
        
        pred_data_, prob, recovery = get_data(pred_data, test=True,cutoff=c)
        true_data_, *_ = get_data(true_data)
        #print(pred_data_)
        weighted_accuracy,fpr, auc = evaluation(pred_data_, true_data_, prob=prob)
        context.append([c, recovery, weighted_accuracy,fpr,auc])
        
    context = np.array(context)
    np.save('./context.npy',context)
    
    context[:,1] = 1 - context[:,1]
    df = pd.DataFrame(context)
    df.columns = ['cufoff','unclassified reads','accuracy', 'false positive rate', 'AUC']
    df = df.round(3)
    best_cutoff, best_accuracy, best_recovery = get_best_cutoff(df)
    df.to_csv('table.csv',index=False,sep='\t')
    print('best_cutoff:{:2f} best_accuracy:{:2f} best_recovery:{:2f}'.format(best_cutoff, best_accuracy, best_recovery))
    return best_cutoff, best_accuracy, best_recovery
  
def get_best_cutoff(df):
    z1 = np.polyfit(df['cufoff'].values, df['accuracy'].values,5)
    p1 = np.poly1d(z1)
    z2 = np.polyfit(df['cufoff'].values, 1 - df['unclassified reads'].values,5)
    p2 = np.poly1d(z2)

    x = np.linspace(0,1,1000)
    y1 = p1(x)
    y2 = p2(x)
    d = []
    for inx,(a1,a2) in enumerate(zip(y1,y2)):
        d.append(np.abs(a1 - a2))
    
    best_cutoff = x[np.argmin(d)]  
    
    best_accuracy, best_recovery = p1(best_cutoff), p2(best_cutoff)
    
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(x, y1, 'g-', lw=2, alpha=0.7, label='sfilt')
    ax1.set_xlabel('Cutoff', fontsize=13)
    ax1.set_ylabel('Sensitivity', color='g',fontsize=13)
    ax1.tick_params('y', colors='g')
    ax1.grid(b=True, ls=':')

    ax2.plot(x, y2, 'b-', lw=2, alpha=0.7, label='rfilt')
    ax2.set_ylabel('Recovery', color='b',fontsize=13)
    ax2.tick_params('y', colors='b')

    ax3 = ax1.twiny()
    ax3.plot(df['cufoff'].values, df['accuracy'].values, 'g--', lw=2, alpha=0.7,label='sraw')


    ax4 = ax2.twiny()
    ax4.plot(df['cufoff'].values, 1 - df['unclassified reads'].values, 'b--', lw=2, alpha=0.7,label='rraw')

    #plt.scatter(best_cutoff, best_accuracy, marker='*', color='r')
    #plt.scatter(best_cutoff, best_recovery, marker='o', color='r')

    plt.tight_layout()
    plt.savefig('performance.png', dpi=400)
    plt.close()
    
    # fig, ax1 = plt.subplots()
    # ax2 = ax1.twinx()
    # ax1.plot(df['cufoff'].values, df['accuracy'].values, 'g-', lw=2, alpha=0.7, )
    # ax1.set_xlabel('Cutoff', fontsize=13)
    # ax1.set_ylabel('Sensitivity', color='g',fontsize=13)
    # ax1.tick_params('y', colors='g')
    # ax1.grid(b=True, ls=':')
    
    # ax2.plot(df['cufoff'].values, 1 - df['unclassified reads'].values, 'b-')
    # ax2.set_ylabel('Recovery', color='b',fontsize=13)
    # ax2.tick_params('y', colors='b')

    # plt.scatter(best_cutoff, best_accuracy, marker='*', color='r')
    # plt.scatter(best_cutoff, best_recovery, marker='o', color='r')
    
    # plt.savefig('performance.png', dpi=400)
    # plt.close()
    
    return best_cutoff, best_accuracy, best_recovery

if __name__ == '__main__':
    print('metrics test')
    args = get_args()
    pred_data = args.predict
    true_data = args.true
    num_classes = args.num_classes
    best_cutoff, best_accuracy, best_recovery = fstat(args)
    
    pred_data, prob,recovery = get_data(pred_data, test=True,cutoff=0)
    true_data, *_ = get_data(true_data)
    print("pass reads:", len(pred_data))
    evaluation(pred_data, true_data, prob=prob)
