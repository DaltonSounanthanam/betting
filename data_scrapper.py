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
    
 
df.to_csv('/home/dalton/Desktop/betting/')    
 
'''
headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
rows = soup.findAll('tr')[1:]
date = [[th.getText() for th in rows[i].findAll('th')] for i in range(len(rows))]
schedule = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]

'''


'''
for line in rows:
    print([th.getText() for th in line.findAll('th')])
    if 'Date' in [th.getText() for th in line.findAll('th')]:
        print(1)
        
'''