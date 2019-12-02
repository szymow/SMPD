# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 17:41:10 2019

@author: Szymon
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

from time import perf_counter

#Liczenie najlepszych dwoch cech

def liczenie(lista, klasa, srednia):
    macierz = np.array(klasa.loc[:, lista])
    macierzSrednich = np.array(srednia.loc[lista])
    przedTrans = np.mat(macierz) - np.mat(macierzSrednich)
    trans = przedTrans.T
        
    result = np.mat(trans) * np.mat(przedTrans)
    dzielnik = 1/len(macierz)
    przedDet = dzielnik * result
    det = np.linalg.det(przedDet)
        
    return det
    
maksymalny = 1
nazwy = klasa_Acer.columns
lista_k = [1,1]

t1_start = perf_counter() 
for k1 in nazwy:
    print (lista_k)
    for k2 in nazwy:
        if k1 != k2:
            lista_k = [k1, k2]
        else:
            continue
        
        licznik = math.sqrt(pow(srednia_Acer[k1] - srednia_Quercus[k1], 2) + pow(srednia_Acer[k2] - srednia_Quercus[k2], 2))
        
        detA = liczenie(lista_k, klasa_Acer, srednia_Acer)
        detB = liczenie(lista_k, klasa_Quercus, srednia_Quercus)
        
        mianownik = detA + detB
        
        if mianownik != 0:
            wspolczynnikF = (licznik / mianownik)
        else:
            wspolczynnikF = 0
        
        if wspolczynnikF > maksymalny:
            maksymalny = wspolczynnikF
            maksC1 = lista_k[0]
            maksC2 = lista_k[1]

t1_stop = perf_counter()
print("najlepsze2Cechy Fisher to: ",maksC1, " i ",maksC2)

print("Elapsed time:", round(t1_stop - t1_start,2), "s")

#Liczenie najlepszych trzech cech
maksymalny = 1
t2_start = perf_counter()
for k1 in nazwy:
    print (lista_k)
    for k2 in nazwy:
        for k3 in nazwy:           
            if k1 != k2 and k1 != k3 and k2 != k3:
                lista_k = [k1, k2, k3]
            else:
                continue
            licznik3 = math.sqrt(pow(srednia_Acer[k1] - srednia_Quercus[k1], 2) + 
                    pow(srednia_Acer[k2] - srednia_Quercus[k2], 2) +
                    pow(srednia_Acer[k3] - srednia_Quercus[k3], 2))
            
            detA = liczenie(lista_k, klasa_Acer, srednia_Acer)
            detB = liczenie(lista_k, klasa_Quercus, srednia_Quercus)
            
            mianownik3 = detA + detB
            
            if mianownik != 0:
                wspolczynnikF = (licznik3 / mianownik3)
            else:
                wspolczynnikF = 0
            
            if wspolczynnikF > maksymalny:
                maksymalny = wspolczynnikF
                maksC1 = lista_k[0]
                maksC2 = lista_k[1]
                maksC3 = lista_k[2]

t2_stop = perf_counter()
print("najlepsze3Cechy Fisher to: ",maksC1, " i ",maksC2, " i ",maksC3)
print("Elapsed time:", round(t2_stop - t2_start,2), "s")

#Liczenie najlepszych czterech cech
maksymalny = 1
for k4 in nazwy:   
    lista_k = [maksC1, maksC2, maksC3]
    lista_k.append(k4)   
    licznik3 = 0   
    for k in lista_k:
        licznik3 = licznik3 + pow(srednia_Acer[k] - srednia_Quercus[k], 2)   
    licznik3 = math.sqrt(licznik3)               
    detA = liczenie(lista_k, klasa_Acer, srednia_Acer)
    detB = liczenie(lista_k, klasa_Quercus, srednia_Quercus)               
    mianownik = detA + detB               
    if mianownik != 0:
        wspolczynnikF = (licznik / mianownik)
    else:
        wspolczynnikF = 0               
    if wspolczynnikF > maksymalny:
        maksymalny = wspolczynnikF
        maksC4 = lista_k.pop()

print("najlepsze4Cechy Fisher to: ",maksC1, " i ",maksC2, " i ",maksC3, " i ",maksC4)

#Liczenie najlepszych pieciu cech
maksymalny = 1
for k5 in nazwy:   
    lista_k = [maksC1, maksC2, maksC3, maksC4]
    if k5 not in lista_k:
        lista_k.append(k5)   
    licznik3 = 0   
    for k in lista_k:
        licznik3 = licznik3 + pow(srednia_Acer[k] - srednia_Quercus[k], 2)   
    licznik3 = math.sqrt(licznik3)               
    detA = liczenie(lista_k, klasa_Acer, srednia_Acer)
    detB = liczenie(lista_k, klasa_Quercus, srednia_Quercus)               
    mianownik = detA + detB               
    if mianownik != 0:
        wspolczynnikF = (licznik / mianownik)
    else:
        wspolczynnikF = 0               
    if wspolczynnikF > maksymalny:
        maksymalny = wspolczynnikF
        maksC5 = lista_k.pop()

lista_k = [maksC1, maksC2, maksC3, maksC4, maksC5]
wynik = ""
for k in lista_k:
    wynik = wynik + k + "; "

print("najlepsze ",len(lista_k) ," cech Fisher to: ", wynik)