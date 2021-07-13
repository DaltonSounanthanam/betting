#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 22:16:35 2021

@author: dalton
"""

import pandas as pd
import numpy as np

import torch 




import nba_scraper.nba_scraper as ns

#ns.scrape_season(2019, data_format='csv', data_dir='home/dalton/Desktop')
ns.scrape_game([21800001, 21800002], data_format='csv', data_dir='/home/dalton/Desktop')