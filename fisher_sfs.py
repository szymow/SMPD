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

liczbacech = 6 #Zadana liczba najlepszych cech

A = np.array(klasa_Acer)
B = np.array(klasa_Quercus)

sredniaA = np.array(srednia_Acer)
sredniaB = np.array(srednia_Quercus)

nX = np.size(A,0) #Liczba cech
nA = np.size(A,1) #Liczba probek
nB = np.size(B,1)

DZIELNIK_A = 1/nA
DZIELNIK_B = 1/nB

a = range(najlepszaCecha,najlepszaCecha+1)
b = range(1,64+1)
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
        resultA =  np.mat(odejmacierzA) * np.mat(transA)
        
        przedDetA = DZIELNIK_A * resultA
        
        detA = np.linalg.det(przedDetA)
    
        transB = odejmacierzB.T
        resultB =  np.mat(odejmacierzB) * np.mat(transB)
        
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
        
        c = list(prod)
        
        e = []
        for d in c:
            if len(d) == len(set(d)):
                e.append(d)
                if 64 in d: break
        prod = e


t1_stop = perf_counter()
print("Elapsed time:", round(t1_stop - t1_start,2), "s")
print("Policzone metoda SFS")


