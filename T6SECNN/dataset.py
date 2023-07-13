import numpy as np
import torch
from Bio import SeqIO
from torch.utils.data import Dataset
def openfasta(fasta_file):
    seq_name = []
    for record in SeqIO.parse(fasta_file, "fasta"):
        description = record.description.split("|")
        if description[0]=="gi":
            name=description[3]
        elif description[0]=="sp":
            name=description[1]
        else:
            name=description[0]
        seq_name.append(name)
    return seq_name
########k折划分############        
def load_data(T6SE,T6SEfasta,prefix):  ###此过程主要是步骤（1）
    if prefix == "ps100" or prefix == "bpb100" :
        T6SE_file =np.loadtxt(T6SE,delimiter=',',dtype=str)
        names = T6SE_file[:,0]
        T6SE_file = T6SE_file[:,1:].astype(np.float32)
    elif prefix == "AAC" or prefix == "DPC" or prefix == "TPC":
        T6SE_file =np.loadtxt(T6SE,delimiter='\t',dtype=str,skiprows=1)
        names = T6SE_file[:,0]
        T6SE_file = T6SE_file[:,1:].astype(np.float32)
    elif prefix == "ESM-2":
        T6SE_dir=os.listdir(T6SE)
        T6SE_file = []
        for name in T6SE_dir:
            t6temp=torch.load(T6SE+"/"+name)['mean_representations'][33].unsqueeze(0)
            T6SE_file.append(t6temp)
        T6SE_file = torch.cat(T6SE_file,dim=0).numpy()
        names = np.array(T6SE_dir) 
    else:
        T6SE_file =np.loadtxt(T6SE,delimiter=',',dtype=np.float32)
        names = openfasta(T6SEfasta)
        names = np.array(names)
    T6SE_file[np.isposinf(T6SE_file)] = 9999
    T6SE_file[np.isneginf(T6SE_file)] = -9999
    T6SE_file[np.isnan(T6SE_file)] = 0 

    return T6SE_file,names

##########定义dataset##########
class TestdataSet(Dataset):
    def __init__(self,train_features,train_labels):
        self.x_data = train_features
        if train_labels is not None:
            self.y_data = train_labels
        else:
            self.y_data = None
        self.len = len(train_features)
    
    def __getitem__(self,index):
        if self.y_data is not None:
            return self.x_data[index],self.y_data[index]
        else:
            return self.x_data[index]
    def __len__(self):
        return self.len
