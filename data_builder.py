#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 18:50:30 2021

@author: dalton
"""

import pandas as pd 
import numpy as np


### drop the nan value row and useless columns ### this task should be automatized
schedule = pd.read_csv('/home/dalton/Desktop/betting/schedule.csv')
schedule = schedule.drop(['Unnamed: 0', 'Notes'], axis = 1)
schedule = schedule.drop(index = 1230, axis = 0)


stats = pd.read_csv('/home/dalton/Desktop/betting/per100poss_team.csv')
stats = stats.drop(['G', 'MP', 'Unnamed: 0'], axis = 1)

stats2 = pd.read_csv('/home/dalton/Desktop/betting/per100poss_oppo.csv')
stats2 = stats2.drop(['G', 'MP', 'Unnamed: 0'], axis = 1)


target_list = []

for i in np.arange(schedule.shape[0]):
    tmp = schedule.iloc[i]
    visitor = int(tmp['PTS'])
    home = int(tmp['PTS.1'])
    if home > visitor:
        target_list.append(1.0)
    else:
        target_list.append(0.0)
    
schedule.to_csv('game_data.csv')

row_list = []

for i in np.arange(schedule.shape[0]):
    tmp = schedule.iloc[i]
    visitor = tmp['Visitor/Neutral']
    home = tmp['Home/Neutral']
    hstats_team = stats[(stats['Team'] == home) | (stats['Team'] == home+'*') ].drop(['Team'], axis = 1)
    hstats_oppo = stats2[(stats2['Team'] == home) | (stats2['Team'] == home+'*')].drop(['Team'], axis = 1)
    vstats_team = stats[(stats['Team'] == visitor) |  (stats['Team'] == visitor+'*')].drop(['Team'], axis = 1)
    vstats_oppo = stats2[(stats2['Team'] == visitor) |  (stats2['Team'] == visitor+'*')].drop(['Team'], axis = 1)
    hstats_team.reset_index(drop = True, inplace = True)
    hstats_oppo.reset_index(drop = True, inplace = True) 
    vstats_team.reset_index(drop = True, inplace = True) 
    vstats_oppo.reset_index(drop = True, inplace = True)
    result = pd.concat([hstats_team, hstats_oppo, vstats_team, vstats_oppo], axis = 1)
    row_list.append(result)
    
data = pd.concat(row_list, axis = 0 )    
data.to_csv('/home/dalton/Desktop/betting/features.csv')
    