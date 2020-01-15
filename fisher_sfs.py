# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 13:31:40 2020

@author: Szymon

Fisher SFS
"""

#Biblioteki GUI
import tkinter as tk
from tkinter import filedialog, Label
from tkinter.ttk import Combobox
import pandas as pd
import numpy as np
import math


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


def odchylenie_std(klasa, srednia):
    odchylenie = []
    liczba_kolumn = int(len(klasa.columns))
    for i in range(liczba_kolumn):
        suma = 0
        for j in range(int(len(klasa.index))):
            x = math.pow(klasa.iloc[j][i] - srednia[i],2)
            suma = suma + x
        suma = suma / liczba_kolumn
        suma = math.sqrt(suma)
        odchylenie.append(suma)
    return odchylenie
        

odchylenie_std_Acer = odchylenie_std(klasa_Acer, srednia_Acer)
odchylenie_std_Quercus = odchylenie_std(klasa_Quercus, srednia_Quercus)

wspolczynniki = []
for i in range(int(len(srednia_Acer))):
    licznik = abs(srednia_Acer[i] - srednia_Quercus[i])
    mianownik = (odchylenie_std_Acer[i] + odchylenie_std_Quercus[i])
    liczba = licznik / mianownik
    wspolczynniki.append(liczba)


najlepszaCecha = wspolczynniki.index(max(wspolczynniki))
print("najlepszaCecha Fisher dla jednej cechy to: ",najlepszaCecha)

from itertools import product

liczbacech = 8 #Zadana liczba najlepszych cech

#Transponowanie
A = klasa_Acer.T
B = klasa_Quercus.T

A = np.array(A)
B = np.array(B)

sredniaA = np.array(srednia_Acer)
sredniaB = np.array(srednia_Quercus)

nX = np.size(A,0) #Liczba cech
nA = np.size(A,1) #Liczba probek
nB = np.size(B,1)

DZIELNIK_A = 1/nA
DZIELNIK_B = 1/nB

a = range(najlepszaCecha,najlepszaCecha+1)
b = range(64)
prod = product(a,b) #Produkt kartezjanski

from time import perf_counter
t1_start = perf_counter() 

for lc in range(2,liczbacech+1):
     
    maks = 0
    
    for iterator in prod:
        print (iterator)
        
        #Pomijaj gdy numer cech sie powtarzaja
        if len(iterator) != len(set(iterator)):
            continue
        
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
    
        print(wynik)
            
        if wynik > maks:
            maks = wynik
            maks_cechy = iterator
    
    print("Wynik: ", maks)
    print("Najlepsze ", lc, " cechy to: ", maks_cechy)
    
    a = maks_cechy
    
    if lc == 2:
        prod = product(a,a,b)
        c = list(prod)
        c = c[64:128]
        prod = c
    else:
        if lc == 3:
            prod = product(a,a,a,b)
        if lc == 4:
            prod = product(a,a,a,a,b)
        if lc == 5:
            prod = product(a,a,a,a,a,b)
        if lc == 6:
            prod = product(a,a,a,a,a,a,b)
        if lc == 7:
            prod = product(a,a,a,a,a,a,a,b)
        if lc == 8:
            prod = product(a,a,a,a,a,a,a,a,b)
        if lc == 9:
            prod = product(a,a,a,a,a,a,a,a,a,b)
        if lc == 10:
            prod = product(a,a,a,a,a,a,a,a,a,a,b)
        
        if lc < liczbacech:
            c = list(prod)
            
            e = []
            for d in c:
                if len(d) == len(set(d)):
                    e.append(d)
                    if 63 in d: break
            prod = e


t1_stop = perf_counter()
print("Elapsed time:", round(t1_stop - t1_start,2), "s")
print("Policzone metoda SFS")


