#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 22:16:35 2021

@author: dalton
"""

import pandas as pd
import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

FOLDER_PATH = '/home/dalton/Desktop/betting/'

class moneyline_net(nn.Module):
    
    def __init__(self):
        super(moneyline_net, self).__init__()
        
        self.layer0 = nn.BatchNorm1d(84)
        self.layer1 = nn.Linear(84,42)
        self.layer2 = nn.Linear(42, 42)
        self.dropout = nn.Dropout(p = 0.5)
        self.layer3 = nn.Linear(42,1)
        
    def forward(self, x):
        
        x = self.layer0(x)
        x = self.layer1(x)
        x = nn.functional.relu(x)
        x = self.dropout(x)
        x = self.layer2(x)
        x = nn.functional.relu(x)
        x = self.layer3(x)
        x = torch.sigmoid(x)
        return x
        
    def train(self, X, Y, learning_rate = 0.01, iterations = 10):
        
        criterion = nn.BCELoss()
        optimizer = optim.Adam( self.parameters(), lr = learning_rate, weight_decay = 0.001) 
        loss = 0
        for i in range(iterations):
            optimizer.zero_grad()
            output = self.forward(X)
            loss = criterion(output, Y)
            loss.backward()
            optimizer.step()
        score = self.score(X, Y)
        return loss.item(), score

    def score(self, X, Y):
        output = (self.forward(X).detach().numpy() > 0.5)*1.0
        return np.sum(output == Y.numpy())/Y.shape[0]
    
    def compute_loss(self,X , Y):
        criterion = nn.BCELoss()
        output = self.forward(X)
        loss = criterion(output, Y)
        return loss.item()
    
    def Train(self, X_train, Y_train, X_test, Y_test, learning_rate = 0.01, n_epoch = 10, iterations = 10):
        for epoch in range(n_epoch):
            train_loss, train_score = self.train( X_train, Y_train, learning_rate , iterations)
            test_loss = self.compute_loss(X_test, Y_test)
            test_score = self.score(X_test, Y_test)
            print('====> Epoch: {} train_loss: {:.4f}, train_score: {:.4f}, test_loss: {:.4f}, test_score: {:.4f}'.format(epoch, train_loss, train_score, test_loss, test_score ))

            
targets = pd.read_csv('{}targets.csv'.format(FOLDER_PATH)).values
Y_train = torch.tensor(targets[:1000]).float()
Y_test = torch.tensor(targets[1000:]).float()

features = pd.read_csv('{}features.csv'.format(FOLDER_PATH)).values
X_train = torch.tensor(features[:1000]).float()
X_test = torch.tensor(features[1000:]).float()
        
net = moneyline_net()


net.Train(X_train, Y_train, X_test, Y_test, 0.01, 50, 10)


        


