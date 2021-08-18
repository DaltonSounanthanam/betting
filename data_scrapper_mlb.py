#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 16:19:36 2021

@author: dalton
"""

import json
import pandas as pd
import numpy as np
import time
import os


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

FOLDER_PATH = '/home/dalton/desktop/betting/'

DATE = '2021-08-03'




def scrap_daily_matchup( file_name ,date, plate_appearances = 3):
    
    url = 'https://baseballsavant.mlb.com/daily_matchups?date={}'.format(date)
    browser = webdriver.Firefox()
    browser.get(url)
    time.sleep(20)
    browser.find_element_by_xpath("//select[@id='ddlPA']/option[{}]".format(plate_appearances)).click()
    time.sleep(20)

    rows = browser.find_elements_by_xpath("//tr[contains(@id, 'leaderboard')]")
    header = browser.find_elements_by_xpath("//tr[contains(@class, 'tr-component')]")
    
    data = []
    for r in rows:
        tmp = [td.text for td in r.find_elements_by_tag_name('td')]
        data.append(tmp)
    df = pd.DataFrame(data, columns= header[0].text.split())
    df.to_csv( file_name, index = False)


def scrap_pitch_arsenals(year, Type = 'avg_spin', hand = '', minimum = 50 ):
    
    url = 'https://baseballsavant.mlb.com/leaderboard/pitch-arsenals?year={}&min={}&type={}&hand={}'.format(year, minimum, Type, hand )
    
    fp = webdriver.FirefoxProfile()
    
    fp.set_preference("browser.download.folderList",2)
    fp.set_preference("browser.download.manager.showWhenStarting",False)
    fp.set_preference("browser.download.dir", os.getcwd())
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
    
    browser = webdriver.Firefox(firefox_profile = fp)
    browser.get(url)
    
    browser.find_element_by_xpath("//button[@id = 'btnCSV']").click()








#url = 'https://baseballsavant.mlb.com/leaderboard/pitch-arsenal-stats?type=pitcher&pitchType=&year=2021&position=undefined&team=&min=10&sort=6&sortDir=asc'


#url = 'https://baseballsavant.mlb.com/leaderboard/expected_statistics?type=pitcher'