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
    dane = pd.read_csv(sciezkaDoPliku, sep = ',')
    print(dane)

przyciskImportujCSV = tk.Button(text=" Importuj CSV ", 
                             command=getCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
przyciskImportujCSV.grid(column=1, row=0)

okno.mainloop()
#https://likegeeks.com/python-gui-examples-tkinter-tutorial/

#Dzielenie na 2 klasy
klasa_Acer = dane[0:176]
klasa_Quercus = dane[176:]

#Pozbycie sie wartosci nieliczbowych
klasa_Acer = klasa_Acer.drop(columns=["64"])
klasa_Quercus = klasa_Quercus.drop(columns=["64"])

#Srednia cech
srednia_Acer = klasa_Acer.mean(axis = 0)
srednia_Quercus = klasa_Quercus.mean(axis = 0)

sredniaA = np.array(srednia_Acer)
sredniaB = np.array(srednia_Quercus)

#Transponowanie
A = klasa_Acer.T
B = klasa_Quercus.T    

A = np.array(A)
B = np.array(B)

lc = 3 #Zadana liczba najlepszych cech

nX = np.size(A,0) #Liczba cech
nA = np.size(A,1) #Liczba probek
nB = np.size(B,1)

DZIELNIK_A = 1/nA
DZIELNIK_B = 1/nB

maks = 0

permutacja = list(permutations(np.arange(nX), lc))
permutacja = np.array(permutacja)

from time import perf_counter
t1_start = perf_counter() 

for iterator in permutacja:
    #Sledzenie postepu dla 3 najlepszych cech
    if lc==3:
        if iterator[0]==(iterator[1]-1)==(iterator[2]-2):
            print (iterator[0],"/",nX)
    licznik = 0
    macA = []
    macB = []

    for i in iterator:
        licznik = licznik + (pow(sredniaA[i] - sredniaB[i],2))
        for j in range(176):
            macA.append(A[i][j] - sredniaA[i])
        for j in range(608):
            macB.append(B[i][j] - sredniaB[i])
    licznik = math.sqrt(licznik)
        
    macA = np.array(macA)
    macB = np.array(macB)
        
    macA = macA.reshape(lc,176)
    macB = macB.reshape(lc,608)
    transA = macA.T
    resultA =  np.mat(macA) * np.mat(transA)
    
    przedDetA = DZIELNIK_A * resultA
    
    detA = np.linalg.det(przedDetA)

    transB = macB.T
    resultB =  np.mat(macB) * np.mat(transB)
    
    przedDetB = DZIELNIK_B * resultB
    detB = np.linalg.det(przedDetB)
    
    mianownik = detA + detB

    if mianownik != 0:
        wynik = licznik/mianownik
    else:
        wynik = 0

#    print(wynik)
        
    if wynik > maks:
        maks = wynik
        maks_cechy = iterator

print("Wynik: ", maks)
print("Najlepsze cechy to: ", maks_cechy)

t1_stop = perf_counter()
print("Elapsed time:", round(t1_stop - t1_start,2), "s")
