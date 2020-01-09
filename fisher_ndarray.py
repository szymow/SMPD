# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 20:43:13 2020

@author: Szymon
"""

import numpy as np
from itertools import permutations
import math

#Biblioteki GUI
import tkinter as tk
from tkinter import filedialog, Label
import pandas as pd

okno=tk.Tk()
okno.title("SMPD lab Szymon Woyda 227458")
okno.geometry('640x480')
etykieta=Label(okno, text=" Wybieranie najlepszej cechy metoda Fishera", font=("Arial",16))
etykieta.grid(column = 0, row = 0)

def getCSV():
    global dane
    sciezkaDoPliku = filedialog.askopenfilename()
    dane = pd.read_csv(sciezkaDoPliku, sep = ';')
    print(dane)

przyciskImportujCSV = tk.Button(text=" Importuj CSV ", 
                             command=getCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
przyciskImportujCSV.grid(column=1, row=0)

okno.mainloop()
#https://likegeeks.com/python-gui-examples-tkinter-tutorial/

#Dzielenie na 2 klasy

liczba_kolumn = len(dane.columns)
klasy = ["c{}".format(i) for i in range(0, liczba_kolumn)]

klasa_Acer = pd.DataFrame(columns = klasy)
klasa_Quercus = pd.DataFrame(columns= klasy)

for i in range(int(len(dane))):
    klasa_probki = dane.iloc[i]["klasa"]
    if klasa_probki == "Acer":
        klasa_Acer.loc[i] = dane.loc[i]
    if klasa_probki == "Quercus":
        klasa_Quercus.loc[i] = dane.loc[i]

#Pozbycie sie wartosci nieliczbowych
klasa_Acer = klasa_Acer.drop(columns=["c0"])
klasa_Quercus = klasa_Quercus.drop(columns=["c0"])

A = np.array(klasa_Acer)
B = np.array(klasa_Quercus)

#Transponowwanie danych z pliku
A = A.T
B = B.T

#A = np.random.uniform(0,1, size=(64, 176))
#B = np.random.uniform(0,1, size=(64, 608))

'''
A = np.array([[4, 6, 1, 0],
              [7, 0, 1, 8],
              [8, 4, 7, 4],
              [3, 5, 4, 6]])

B = np.array([[0, 7, 4],
              [6, 0, 2],
              [8, 3, 8],
              [8, 8, 7]])
'''

lc = 3 #Liczba Cech

print(A)
print(B)

sredniaA = A.mean(axis=1) #Srednia wierszy
sredniaB = B.mean(axis=1)

print(sredniaA)
print(sredniaB)

nX = np.size(A,0) #Liczba wierszy
nA = np.size(A,1) #Liczba kolumn
nB = np.size(B,1)

DZIELNIK_A = 1/nA
DZIELNIK_B = 1/nB

maks = 0

permutacja = list(permutations(np.arange(nX)+1, lc))
permutacja = np.array(permutacja)

from time import perf_counter
t1_start = perf_counter() 

for iterator in permutacja:
    print (iterator)
    licznik = 0
    odejmacierzA = np.array([])
    odejmacierzB = np.array([])
    for i in iterator:
        licznik = licznik + (pow(sredniaA[i-1] - sredniaB[i-1],2))
        odejmacierzA = np.concatenate([odejmacierzA, A[i-1] - sredniaA[i-1]])
        odejmacierzB = np.concatenate([odejmacierzB, B[i-1] - sredniaB[i-1]])
    licznik = math.sqrt(licznik)
    odejmacierzA = odejmacierzA.reshape(lc,nA) #Sklejenie podmacierzy
    odejmacierzB = odejmacierzB.reshape(lc,nB)
    transA = odejmacierzA.T
    resultA = np.mat(transA) * np.mat(odejmacierzA)
    
    przedDetA = DZIELNIK_A * resultA
    detA = np.linalg.det(przedDetA)

    transB = odejmacierzB.T
    resultB = np.mat(transB) * np.mat(odejmacierzB)
    
    przedDetB = DZIELNIK_B * resultB
    detB = np.linalg.det(przedDetB)
    
    mianownik = detA + detB
    if mianownik != 0:
        wynik = licznik/mianownik
    else:
        wynik = 0
        
    print(wynik)
        
    if wynik > maks:
        maks = wynik
        maks_cechy = iterator
        
print("Najlepsze cechy to: ", maks_cechy)

t1_stop = perf_counter()
print("Elapsed time:", round(t1_stop - t1_start,2), "s")