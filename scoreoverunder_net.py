#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 13:30:29 2021

@author: dalton
"""

import pandas as pd
import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

FOLDER_PATH = '/home/dalton/Desktop/betting/'


class scoreoverunder_net(nn.Module):
    
    def __init__(self):
        super(scoreoverunder_net, self).__init__()
        
        self.layer0 = nn.BatchNorm1d(21)
        self.layer1 = nn.Linear(21,42)
        self.layer2 = nn.Linear(42, 21)
        self.layer3 = nn.Linear(21,2)
        
    def forward(self, x):
        
        x = self.layer0(x)
        x = self.layer1(x)
        x = nn.functional.tanh(x)
        x = self.layer2(x)
        x = nn.functional.tanh(x)
        x = self.layer3(x)
        x = F.relu(x)
        return x
        