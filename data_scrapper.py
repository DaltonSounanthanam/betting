#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 19:27:59 2021

@author: dalton
"""

import json
import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
from urllib.request import urlopen


from datetime import datetime, timedelta

year = 2019

FOLDER_PATH = '/home/dalton/Desktop/betting/'


### Scrap the schedule and results of the regular season ###

# Due to the pandemic we need modify the code for the 2020 season, the season has been pushed back


def scrap_schedule(FOLDER_PATH = FOLDER_PATH, year = year):

    url = "https://www.basketball-reference.com/leagues/NBA_{}_games.html".format(year)

    date = []
    schedule = []
    headers = None

    for m in ['october', 'november', 'december', 'january', 'february', 'march', 'april', 'may', 'june']:

        url = "https://www.basketball-reference.com/leagues/NBA_{}_games-{}.html".format(year, m)
        html = urlopen(url)
        soup = BeautifulSoup(html)
        headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
        rows = soup.findAll('tr')[1:]
        date = date + [[th.getText() for th in rows[i].findAll('th')][0] for i in range(len(rows))]
        schedule = schedule +  [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]


    df = pd.DataFrame(schedule, columns = headers[1:])
    df['Date'] = date
    
 
    df.to_csv('{}schedule.csv'.format(FOLDER_PATH), index = False)    
 


### Scrapp the per 100 possessions stats ###

def scrap_per100poss(FOLDER_PATH = FOLDER_PATH, year = year):

    url2 = 'https://www.basketball-reference.com/leagues/NBA_{}.html#all_per_poss_team-opponent'.format(year+1)
    html2 = urlopen(url2)
    soup2 = BeautifulSoup(html2)
    alltab = soup2.findAll('table')
    tab2 = alltab[8]
    rows2 = tab2.findAll('tr')
    headers2 = [th.getText() for th in rows2[0].findAll('th')]
    stats2 = [[td.getText() for td in rows2[i].findAll('td')] for i in np.arange(1,len(rows2))]

    df2 = pd.DataFrame(stats2, columns = headers2[1:])
    df2.to_csv('{}per100poss_team.csv'.format(FOLDER_PATH), index = False)


    tab3 = alltab[9]
    rows3 = tab3.findAll('tr')
    headers3 = [th.getText() for th in rows3[0].findAll('th')]
    stats3 = [[td.getText() for td in rows3[i].findAll('td')] for i in np.arange(1,len(rows3))]

    df3 = pd.DataFrame(stats3, columns = headers3[1:])
    df3.to_csv('{}per100poss_oppo.csv'.format(FOLDER_PATH), index = False)




    ### Scrap shooting stats ###


    tab4 = alltab[11]
    rows4 = tab4.findAll('tr')
    headers4 = [th.getText() for th in rows4[1].findAll('th')]
    stats4 = [[td.getText() for td in rows4[i].findAll('td')] for i in np.arange(2,len(rows4)-1)]

    df4 = pd.DataFrame(stats4, columns = headers4[1:])
    df4.to_csv('{}shooting_team.csv'.format(FOLDER_PATH), index = False)


    tab5 = alltab[12]
    rows5 = tab5.findAll('tr')
    headers5 = [th.getText() for th in rows5[1].findAll('th')]
    stats5 = [[td.getText() for td in rows5[i].findAll('td')] for i in np.arange(2,len(rows5)-1)]

    df5 = pd.DataFrame(stats5, columns = headers5[1:])
    df5.to_csv('{}shooting_oppo.csv'.format(FOLDER_PATH), index =  False)


### Scrap player data ###


def scrap_players_data(FOLDER_PATH = FOLDER_PATH, year = year):
    
    url = 'https://www.basketball-reference.com/leagues/NBA_{}_per_poss.html'.format(year)
    html = urlopen(url)
    soup = BeautifulSoup(html)
    tab = soup.findAll('table')[0]
    rows = tab.findAll('tr')
    headers = [th.getText() for th in rows[0].findAll('th')]
    stats = [[td.getText() for td in rows[i].findAll('td')] for i in np.arange(1,len(rows))]
    stats = [ l for l in stats if l]

    df = pd.DataFrame(stats, columns= headers[1:])
    df.to_csv('{}players_stats.csv'.format(FOLDER_PATH), index  = False)


### Scrap schedule, score and details

def scrap_scores_date(m = 1, d = 1, y = 2021):
    
    url = 'https://www.basketball-reference.com/boxscores/?month={}&day={}&year={}'.format(m,d,y)
    html = urlopen(url)
    soup = BeautifulSoup(html)
    tabs = soup.findAll('div', { 'class' : 'game_summary expanded nohover' })
    game_scores = []
    for i in range(len(tabs)):
        boxes = tabs[i].findAll('table')
        game_score = [td.getText() for td in boxes[0].findAll('td')]
        quarter_score_line = boxes[1].findAll('tr')
        quarter_score_line_1 = [td.getText() for td in quarter_score_line[1].findAll('td', {'class' : 'center'})]
        quarter_score_line_2 = [td.getText() for td in quarter_score_line[2].findAll('td', {'class' : 'center'})]
        quarter_score_line_1 = quarter_score_line_1 + ['0' for i in range(8 - len(quarter_score_line_1)) ]
        quarter_score_line_2 = quarter_score_line_2 + ['0' for i in range(8 - len(quarter_score_line_2)) ]
        game_scores.append(game_score + quarter_score_line_1 + quarter_score_line_2)
    return game_scores


def scrap_scores(date_from, date_to, FOLDER_PATH = FOLDER_PATH):
    scores_list = []
    m1, d1, y1 =  [int(i) for i in date_from.split('/')]
    m2, d2, y2 =  [int(i) for i in date_to.split('/')]
    end_date = datetime(y2, m2, d2)
    current_date = datetime(y1, m1, d1)
    while current_date <= end_date:
        scores_list = scores_list + scrap_scores_date( current_date.month, current_date.day, current_date.year)
        current_date = current_date + timedelta(1)
    header = ['Away_team', 'Away_score', 'Status', 'Home_team', 'Home_score', 'OT', 'Away_1', 'Away_2', 'Away_3', 'Away_4', 'Away_5', 'Away_6', 'Away_7', 'Away_8', 'Home_1', 'Home_2', 'Home_3', 'Home_4', 'Home_5', 'Home_6', 'Home_7', 'Home_8'] 
    df = pd.DataFrame(scores_list, columns = header)
    df.to_csv( FOLDER_PATH + 'scores_' + date_from.replace('/','') + '_' + date_to.replace('/', '' ) + '.csv')
    return df


def scrap_player_split_stats( player = 'jamesle01',year = 2021):
    url = 'https://www.basketball-reference.com/players/{}/{}/splits/{}'.format(player[0], player, year)
    html = urlopen(url)
    soup = BeautifulSoup(html)
    rows = soup.findAll('tr')[1:]
    header = [th.getText() for th in rows[0].findAll('th')]
    tmp = [[td.getText() for td in rows[i].findAll('td')] for i in np.arange(1, len(rows))]
    tmp = [l for l in tmp if l]
    df = pd.DataFrame(tmp, columns = header[1:])
    df.to_csv(FOLDER_PATH + player + '_splits_stats.csv')
    return df

def scrap_player_gamelog():
    return None

tmp = scrap_player_split_stats()
    