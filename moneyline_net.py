#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 22:16:35 2021

@author: dalton
"""

import pandas as pd
import numpy as np

import torch.nn as nn
import torch.functional as F
import torch.optim as optim


class moneyline_net(nn.Module):
    
    def __init__(self):
        super(moneyline_net, self).__init__()
        
        self.layer1 = nn.Linear(84,42)
        self.layer2 = nn.Linear(42, 42)
        self.layer3 = nn.Linear(42,1)
        
    def forward(self, x):
        
        x = self.layer1(x)
        x = F.relu(x)
        x = self.layer2(x)
        x = F.relu(x)
        x = self.layer3(x)
        x = F.sigmoid(x)
        return x
        
    def train(self, X, Y, learning_rate = 0.01, iterations = 10):
        
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam( self.parameters(), lr = learning_rate) 
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
        output = self.forward(X).numpy()
        return 1 - np.mean(np.abs(output - Y.numpy()))
    
    def compute_loss(self,X , Y):
        criterion = nn.CrossEntropyLoss()
        output = self.forward(X)
        loss = criterion(output, Y)
        return loss.item()
    
    def Train(self, X_train, Y_train, X_test, Y_test, learning_rate = 0.01, n_epoch = 10, iterations = 10):
        for epoch in range(n_epoch):
            train_loss, train_score = self.train( X_train, Y_train, learning_rate , iterations)
            test_loss = self.compute_loss(X_test, Y_test)
            test_score = self.score(X_test, Y_test)
            print('====> Epoch: {} train_loss: {:.4f}, train_score: {:.4f}, test_loss: {:.4f}, test_score: {:.4f}'.format(epoch, train_loss, train_score, test_loss, test_score ))

            
        
        
        


