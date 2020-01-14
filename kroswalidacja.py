# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 18:51:58 2020

@author: Szymon
"""

import pandas as pd
import numpy as np

dane = pd.read_csv('new4.csv')

#Kroswalidacja

n_k = 4 # Na ile zbiorow dzielimy
m_k = 5 # Ile razy powatarzamt dzielenie

lp_k = len(dane) # Liczba probek
lc_k = np.size(dane,1) - 1 # Liczba cech

d_k = int(lp_k/n_k) # Dzielnik

#Dzielenie na zbior treningowy i testowy

dane = dane.sample(frac=1) # Mieszanie kolejnosci


dane = np.array(dane)

dane_k = [] # Dane podzielone
for i in range(n_k):
    dane_k.append(dane[0 + i*d_k : d_k + i*d_k])
    
test_k = dane_k[0]
trening_k = dane_k[1:4]

test_k = test_k.reshape(test_k.size)
test_k = test_k.tolist()

while 'A' in test_k : test_k.remove('A')
while 'B' in test_k : test_k.remove('B')

test_k = np.array(test_k)

lptest_k = int(test_k.size/lc_k)

test_k = test_k.reshape(lptest_k,lc_k)


#Bootstrap

n_b = 1/5 # Jaki [%] procent zbioru bierzemy do testu
m_b = 5 # Ile razy powatarzamt dzielenie


