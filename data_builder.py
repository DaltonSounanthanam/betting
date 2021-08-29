#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 18:50:30 2021

@author: dalton
"""

import pandas as pd 
import numpy as np

FOLDER_PATH = '/home/dalton/Desktop/betting/'

'''
### drop the nan value row and useless columns ### this task should be automatized
schedule = pd.read_csv('{}schedule.csv'.format(FOLDER_PATH))
schedule = schedule.drop(['Notes'], axis = 1)
schedule = schedule.drop(index = 1230, axis = 0)


stats = pd.read_csv('{}per100poss_team.csv'.format(FOLDER_PATH))
stats = stats.drop(['G', 'MP'], axis = 1)

stats2 = pd.read_csv('{}per100poss_oppo.csv'.format(FOLDER_PATH))
stats2 = stats2.drop(['G', 'MP'], axis = 1)


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
target = pd.DataFrame(target_list, columns = ['home_team_win'] )
index = np.random.permutation(len(target))
target = target.iloc[index].reset_index(drop =  True)
target.to_csv('{}targets3.csv'.format(FOLDER_PATH), index = False)

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
    #result = pd.concat([hstats_team , vstats_team, hstats_oppo , vstats_oppo], axis = 1)
    result = hstats_team - vstats_team
    row_list.append(result)
    
data = pd.concat(row_list, axis = 0 )
data = data.iloc[index].reset_index(drop = True)    
data.to_csv('{}features3.csv'.format(FOLDER_PATH), index = False)
'''

def compute_total_score(filename):
    scores = pd.read_csv(FOLDER_PATH + filename)
    a = scores['Home_score']
    b = scores['Away_score']
    t = a + b

    a1 = scores['Away_1']
    b1 = scores['Home_1']
    t1 = a1 + b1

    a2 = scores['Away_2']
    b2 = scores['Home_2']
    t2 = a2 + b2

    a3 = scores['Away_3']
    b3 = scores['Home_3']
    t3 = a3 + b3

    a4 = scores['Away_4']
    b4 = scores['Home_4']
    t4 = a4 + b4
    
    scores['T'] = t
    scores['T1'] = t1
    scores['T2'] = t2
    scores['T3'] = t3
    scores['T4'] = t4
    scores.to_csv(FOLDER_PATH + 'process_' + filename , index = False)