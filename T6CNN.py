# -*- coding: utf-8 -*-
# python T6CNN.py -p /home/hym/data/smb/20230302-T6SE/input/AAC_DPC_TPC/AAC_T6SEs_29.tsv -f /home/hym/data/smb/20230302-T6SE/input/add_T6SE_Test_29_c0.6_formatchange.fa -pr AAC -d cuda:0

#Author : Yueming Hu
#TIME:2023/03/30
import os
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
import torch
import torch.nn as nn
from torch.utils.data import DataLoader,Dataset
import torch.nn.functional as F
from torch.optim import Optimizer
import numpy as np
import pandas as pd
import argparse
import sys
import math
from Bio import SeqIO
from T6SECNN.model import T6CNN_single,T6CNN
from T6SECNN.dataset import load_data,TestdataSet
args = sys.argv

def Testing(kfold,X_test,prefix,device,fasta,batch_size=5):
    test, names=load_data(X_test,fasta,prefix)
    test = torch.from_numpy(test)
    label = None
    if label is not None:
        label = torch.tensor(label,dtype=torch.long)
    test_set=TestdataSet(test,label)
    test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=False)
    in_dim = test.shape[1]
    i=0
    # create model and load weights from checkpoint
    if prefix == "ps100" or prefix == "bpb100" or prefix =="DPC":
         net =  T6CNN_single(in_dim).to(device)  ### 实例化模型
    else:
        net =  T6CNN(in_dim).to(device)  ### 实例化模型
    allpredict = []
    allprobability = []
    for i in range(kfold):
        predict = []
        probability = []
        model_path="./model/"+prefix+"_k"+str(i+1)+"_model.ckpt"
        print(model_path)
        net.load_state_dict(torch.load(model_path))
        net.eval() # set the model to evaluation mode
        with torch.no_grad():
            for j, data in enumerate(test_loader):
                if label:
                    inputs, labels = data
                    inputs, labels = inputs.to(device), labels.to(device)
                else:
                    inputs = data
                    inputs = inputs.to(device)
                outputs  = net(inputs)
                outputs = F.softmax(outputs,dim=1)#softmax
                test_prob, test_pred = torch.max(outputs, 1) # get the index of the class with the highest probability
                for y in test_pred.cpu().numpy():
                    predict.append(y)
                for x,y in enumerate(test_prob.cpu().numpy()):
                    if test_pred.cpu().numpy()[x]==1:
                        probability.append(y)
                    else:
                        probability.append(1-y)
        if i == 0:
            allpredict=predict
            allprobability=probability
        elif i == 1:
            allpredict=[allpredict,predict]
            allprobability=[allprobability,probability]
        else:
            allpredict.append(predict)
            allprobability.append(probability)

    allpredict=list(map(list, zip(*allpredict)))
    data=pd.DataFrame(allpredict,columns=['k1', 'k2', 'k3', 'k4', 'k5'])
    data['vote']=data.mean(axis=1)
    data['vote'][data.vote>=0.5]=1
    data['vote'][data.vote<0.5]=0

    # data.to_csv('all_prediction.csv',sep='\t',index=True, index_label="id",header=True)
    allprobability=list(map(list, zip(*allprobability)))
    data1=pd.DataFrame(allprobability,columns=['k1', 'k2', 'k3', 'k4', 'k5'])
    data1['means']=data1.mean(axis=1)
    data1['vote']=data['vote']
    data1.insert(loc=0, column='id', value=names)
    data1.insert(loc=8, column='label', value=label)
    data1.to_csv(prefix+'_T6probability.csv',sep=',',index=False, header=True)

def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--T6SE', required=True)
    parser.add_argument('-f', '--fasta', required=False)
    parser.add_argument('-k', '--kfold', default=5)
    parser.add_argument('-pr', '--prefix', help='model prefix')
    parser.add_argument('-d', '--device', default='cuda:0')

    args = parser.parse_args()
    T6SE = args.T6SE
    prefix = args.prefix
    device = args.device
    kfold = args.kfold
    if prefix == "ps100" or prefix == "bpb100" or prefix == "AAC" or prefix == "DPC" or prefix == "TPC":
        fasta = None
    else:
        fasta = args.fasta
    Testing(int(kfold),T6SE,prefix,device,fasta)
    # torch.save(Net.state_dict(),outputfile)



if __name__ == '__main__':
    main(args)