#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 21:24:07 2021

@author: dalton
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.special import comb



def expected_unit_earning(c,p):
    if p > 1:
        raise ValueError
    return c*p - 1*(1-p)

def unit_earning(c,p):
    np.random.seed()
    if np.random.uniform() < p:
        return c
    else:
        return -1


def sim_earning(c, p, T, seed = -1):
    total_earning = 0
    if seed < 0:
        np.random.seed()
    else:
        np.random.seed(seed)
    outcome = np.random.binomial(1, p, T)
    total_earning = c*np.sum(outcome) - T + np.sum(outcome)
    return total_earning




def prob_negative_earning(c,p,T):
    i = 0
    prob = 0
    while i < T/(c + 1):
        prob = prob + comb(T,i)*p**i*(1 - p)**(T-i)
        i = i + 1
    return prob

def prob_positive_earning(c, p, T):
    return 1 - prob_negative_earning(c, p, T)


def Odd_to_probabilty(Odd):
    return 1/(Odd + 1)


def prob_bankruptcy(c, p, T, b, cash):
    i = 0
    prob = 0
    while i < (b*T - cash)/(c*b + b):
        prob = prob + comb(T,i)*p**i*(1 - p)**(T-i)
        i = i + 1
    return prob


def money_vs_time(c, p, T, b, cash):
    return (T*b*(c*p - (1-p))/cash) + 1

#### create a heatmap

arr = np.zeros(shape = (20,11))


for c in range(1,21):
    for p in range(0,11):
        arr[c-1,p] = expected_unit_earning(c, p/10)

fig, ax = plt.subplots()
im = ax.imshow(arr, cmap='plasma')
ax.set_xticks(np.arange(0,11,2.5))
ax.set_yticks(np.arange(0,20))

ax.set_xticklabels(np.arange(0,1.1,0.25))
ax.set_yticklabels(np.arange(1,21))
#ax.xlabel('Probility')
#ax.ylabel('Odd')
'''
for i in range(arr.shape[0]):
    for j in range(arr.shape[1]):
        text = ax.text(j, i, arr[i,j], ha="center", va="center", color="w")
'''        
cbar = ax.figure.colorbar(im, ax=ax)
cbar.ax.set_ylabel('', rotation=-90, va="bottom")

ax.set_title('Average earning (Odd/Probability)')
fig.tight_layout()
#plt.show()


#### What the Odd means in probability, convert Odd to probabi

arr2 = np.zeros(30)

for i in range(30):
    arr2[i] = Odd_to_probabilty(i+1)

fig2, ax2 = plt.subplots()
ax2.plot( np.arange(1,31),arr2, c = 'r')
ax2.set_ylabel('Probability')
ax2.set_xlabel('Odd')
ax2.set_title('Odd to probability')
#plt.show()


### How much money should I bet ? 

# Bankruptcy, bet too high lead to bankruptcy

fig3, ax3 = plt.subplots()

for j in np.arange(1.1, 3.1, 0.1 ):
    pb = np.zeros(100)
    for i in np.arange(100):
        pb[i] = prob_bankruptcy(j, 0.5, 100, i + 1, 100)
    ax3.plot(pb, ls = 'solid')

ax3.set_title('Bankruptcy probability')
ax3.set_xlabel('bet')
ax3.set_ylabel('probability')
    
# Time, bet too low you dont make money during your lifetime

fig4, ax4 = plt.subplots()


for i in range(10):
    pbt = np.zeros(100)
    for t in np.arange(1, 100 + 1):
        pbt[t - 1] = money_vs_time(1.5, 0.5, t, i + 1, 100)
    ax4.plot(pbt, ls = 'solid')

ax4.set_xlabel('Number of bet')
ax4.set_ylabel('Ratio Payroll/InitialCash (Returns)')
ax4.set_title('Returns vs time')
### How to identify good betting value ?


### Pari interessant ###
# remontada du champion, equipe mene reviens au score
# combine stats joueur et nb de points, nb de goal
# offset bet, two bet are winnable and offset each other when there is a lost

