import torch
import torch.nn as nn
import torch.nn.functional as F
######网络结构##########
class T6CNN_single(nn.Module):
    #定义T6CNN
    def __init__(self,in_dim: int):
        super(T6CNN_single, self).__init__() 
        self.in_dim = in_dim
        self.max_dim = 10
        if self.in_dim >800:
            self.max_dim = 100
            self.in_dim = self.in_dim//10
            
        self.conv1   = nn.Sequential(nn.Conv1d(in_channels=1,out_channels=10,kernel_size=3,padding=1),
                        nn.BatchNorm1d(10),
                        nn.ReLU(),
                        nn.Dropout(0.20),
                        nn.MaxPool1d(self.max_dim)
            )
        self.conv2   = nn.Sequential(nn.Conv1d(in_channels=1,out_channels=10,kernel_size=6,padding=3),
                        nn.BatchNorm1d(10),
                        nn.ReLU(),
                        nn.Dropout(0.25),
                        nn.MaxPool1d(self.max_dim)
            )
        self.conv3   = nn.Sequential(nn.Conv1d(in_channels=1,out_channels=10,kernel_size=9,padding=9//2),
                        nn.BatchNorm1d(10),
                        nn.ReLU(),
                        nn.Dropout(0.35),
                        nn.MaxPool1d(self.max_dim)
            )
        self.mlp = nn.Sequential(nn.Flatten(),
                        nn.Linear(self.in_dim*3, 64),
                        nn.ReLU(),
                        nn.Dropout(0.35),
                        nn.Linear(64, 2))
  
    def forward(self, x):
        x = x.unsqueeze(1)

        x1 = self.conv1(x)
        x2 = self.conv2(x)
        x3 = self.conv3(x)
        x = self.mlp(torch.cat([x1,x2,x3],1))
        return x
class T6CNN(nn.Module):
    #定义T6CNN
    def __init__(self,in_dim: int):
        super(T6CNN, self).__init__() 
        self.in_dim = in_dim
        if self.in_dim >800:
            self.in_dim = 800
        self.conv1   = nn.Sequential(nn.Conv1d(in_channels=1,out_channels=10,kernel_size=3,padding=1),
                        nn.BatchNorm1d(10),
                        nn.ReLU(),
                        nn.Dropout(0.25),
                        nn.Conv1d(in_channels=10,out_channels=self.in_dim,kernel_size=3,padding=1),
                        nn.BatchNorm1d(self.in_dim),
                        nn.ReLU(),
                        nn.Dropout(0.25),
                        nn.MaxPool1d(in_dim)
            )
        self.conv2   = nn.Sequential(nn.Conv1d(in_channels=1,out_channels=10,kernel_size=6,padding=3),
                        nn.BatchNorm1d(10),
                        nn.ReLU(),
                        nn.Dropout(0.25),
                        nn.Conv1d(in_channels=10,out_channels=self.in_dim,kernel_size=6,padding=3),
                        nn.BatchNorm1d(self.in_dim),
                        nn.ReLU(),
                        nn.Dropout(0.25),
                        nn.MaxPool1d(in_dim)
            )
        self.conv3   = nn.Sequential(nn.Conv1d(in_channels=1,out_channels=10,kernel_size=9,padding=9//2),
                        nn.BatchNorm1d(10),
                        nn.ReLU(),
                        nn.Dropout(0.25),
                        nn.Conv1d(in_channels=10,out_channels=self.in_dim,kernel_size=9,padding=9//2),
                        nn.BatchNorm1d(self.in_dim),
                        nn.ReLU(),
                        nn.Dropout(0.25),
                        nn.MaxPool1d(in_dim)
            )
        self.mlp = nn.Sequential(nn.Flatten(),
                        nn.Linear(self.in_dim*3, 64),
                        nn.ReLU(),
                        nn.Dropout(0.25),
                        nn.Linear(64, 2))
  
    def forward(self, x):
        x = x.unsqueeze(1)

        x1 = self.conv1(x)
        x2 = self.conv2(x)
        x3 = self.conv3(x)
        x = self.mlp(torch.cat([x1,x2,x3],1))
        return x
class T6CNN_pLM(nn.Module):
    #定义T6CNN_pLM
    def __init__(self,in_dim: int):
        super(T6CNN_pLM, self).__init__() 
        self.in_dim = in_dim
        self.max_dim = 10
        if self.in_dim >800:
            self.max_dim = 100
            self.in_dim = self.in_dim//100
        else:
            self.in_dim = in_dim//10
            
        self.conv1   = nn.Sequential(nn.Conv1d(in_channels=1,out_channels=10,kernel_size=3,padding=1),
                        nn.BatchNorm1d(10),
                        nn.ReLU(),
                        nn.Dropout(0.20),
                        nn.MaxPool1d(self.max_dim)
            )
        self.conv2   = nn.Sequential(nn.Conv1d(in_channels=1,out_channels=10,kernel_size=6,padding=3),
                        nn.BatchNorm1d(10),
                        nn.ReLU(),
                        nn.Dropout(0.25),
                        nn.MaxPool1d(self.max_dim)
            )
        self.conv3   = nn.Sequential(nn.Conv1d(in_channels=1,out_channels=10,kernel_size=9,padding=9//2),
                        nn.BatchNorm1d(10),
                        nn.ReLU(),
                        nn.Dropout(0.35),
                        nn.MaxPool1d(self.max_dim)
            )
        self.mlp = nn.Sequential(nn.Flatten(),
                        nn.Linear(self.in_dim*30, 2))
  
    def forward(self, x):
        x = x.unsqueeze(1)

        x1 = self.conv1(x)
        x2 = self.conv2(x)
        x3 = self.conv3(x)
        x = self.mlp(torch.cat([x1,x2,x3],1))
        return x
