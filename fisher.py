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


wspolczynniki = pd.DataFrame()

for j in klasa_Acer.columns:
    wspolczynniki[j] = j
    index = 0
    for i in klasa_Acer.columns:
        licznik = math.sqrt(pow(srednia_Acer[j] - srednia_Quercus[j], 2) + pow(srednia_Acer[i] - srednia_Quercus[i], 2))
        
        macierzA = np.array(klasa_Acer.loc[:, [j, i]])
        macierzSrednichA = np.array(srednia_Acer.loc[[j, i]])
        przedTransA = np.mat(macierzA) - np.mat(macierzSrednichA)
        transA = przedTransA.T
        
        resultA = np.mat(transA) * np.mat(przedTransA)
        dzielnikA = 1/len(macierzA)
        przedDetA = dzielnikA * resultA
        detA = np.linalg.det(przedDetA)
        
        macierzB = np.array(klasa_Quercus.loc[:, [j, i]])
        macierzSrednichB = np.array(srednia_Quercus.loc[[j, i]])
        przedTransB = np.mat(macierzB) - np.mat(macierzSrednichB)
        transB = przedTransB.T
        
        resultB = np.mat(transB) * np.mat(przedTransB)
        dzielnikB = 1/len(macierzB)
        przedDetB = dzielnikB * resultB
        detB = np.linalg.det(przedDetB)
        
        mianownik = detA + detB
        
        if mianownik != 0:
            wspolczynniki.loc[index, j] = (licznik / mianownik)
        else:
            wspolczynniki.loc[index, j] = 0
            
        index = index + 1
