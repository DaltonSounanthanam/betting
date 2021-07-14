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

year = 2019


### Scrap the schedule and results of the regular season ###

# Due to the pandemic we need modify the code for the 2020 season, the season has been pushed back

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
    
 
df.to_csv('/home/dalton/Desktop/betting/schedule.csv')    
 


### Scrapp the per 100 possessions stats ###

url2 = 'https://www.basketball-reference.com/leagues/NBA_{}.html#all_per_poss_team-opponent'.format(year+1)
html2 = urlopen(url2)
soup2 = BeautifulSoup(html2)
alltab = soup2.findAll('table')
tab2 = alltab[8]
rows2 = tab2.findAll('tr')
headers2 = [th.getText() for th in rows2[0].findAll('th')]
stats2 = [[td.getText() for td in rows2[i].findAll('td')] for i in np.arange(1,len(rows2))]

df2 = pd.DataFrame(stats2, columns = headers2[1:])
df2.to_csv('/home/dalton/Desktop/betting/per100poss_team.csv')


tab3 = alltab[9]
rows3 = tab3.findAll('tr')
headers3 = [th.getText() for th in rows3[0].findAll('th')]
stats3 = [[td.getText() for td in rows3[i].findAll('td')] for i in np.arange(1,len(rows3))]

df3 = pd.DataFrame(stats3, columns = headers3[1:])
df3.to_csv('/home/dalton/Desktop/betting/per100poss_oppo.csv')




### Scrap shooting stats ###


tab4 = alltab[11]
rows4 = tab4.findAll('tr')
headers4 = [th.getText() for th in rows4[1].findAll('th')]
stats4 = [[td.getText() for td in rows4[i].findAll('td')] for i in np.arange(2,len(rows4)-1)]

df4 = pd.DataFrame(stats4, columns = headers4[1:])
df4.to_csv('/home/dalton/Desktop/betting/shooting_team.csv')


tab5 = alltab[12]
rows5 = tab5.findAll('tr')
headers5 = [th.getText() for th in rows5[1].findAll('th')]
stats5 = [[td.getText() for td in rows5[i].findAll('td')] for i in np.arange(2,len(rows5)-1)]

df5 = pd.DataFrame(stats5, columns = headers5[1:])
df5.to_csv('/home/dalton/Desktop/betting/shooting_oppo.csv')
