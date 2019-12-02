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


def liczenie(zmienna1, zmienna2, klasa, srednia):
    macierz = np.array(klasa.loc[:, [zmienna2, zmienna1]])
    macierzSrednich = np.array(srednia.loc[[zmienna2, zmienna1]])
    przedTrans = np.mat(macierz) - np.mat(macierzSrednich)
    trans = przedTrans.T
        
    result = np.mat(trans) * np.mat(przedTrans)
    dzielnik = 1/len(macierz)
    przedDet = dzielnik * result
    det = np.linalg.det(przedDet)
        
    return det
    

wspolczynnikiF = pd.DataFrame()

for kolumny in klasa_Acer.columns:
    wspolczynnikiF[kolumny] = kolumny
    indeks = 0
    for wiersze in klasa_Acer.columns:
        licznik = math.sqrt(pow(srednia_Acer[kolumny] - srednia_Quercus[kolumny], 2) + pow(srednia_Acer[wiersze] - srednia_Quercus[wiersze], 2))
        
        detA = liczenie(wiersze, kolumny, klasa_Acer, srednia_Acer)
        detB = liczenie(wiersze, kolumny, klasa_Quercus, srednia_Quercus)
        
        mianownik = detA + detB
        
        if mianownik != 0:
            wspolczynnikiF.loc[indeks, kolumny] = (licznik / mianownik)
        else:
            wspolczynnikiF.loc[indeks, kolumny] = 0
            
        indeks = indeks + 1
        
najlepsze2Cechy_1 = max(wspolczynnikiF)
najlepsze2Cechy_2 = wspolczynnikiF[wspolczynnikiF[max(wspolczynnikiF)]==wspolczynnikiF[max(wspolczynnikiF)].max()].index.values.astype(int)[0] 
najlepsze2Cechy_2 = "c" + str(najlepsze2Cechy_2 + 1)

print("najlepsze2Cechy Fisher to: ",najlepsze2Cechy_1, " i ",najlepsze2Cechy_2)

licznik3 = math.sqrt(pow(srednia_Acer["c1"] - srednia_Quercus["c1"], 2) + 
                    pow(srednia_Acer["c2"] - srednia_Quercus["c2"], 2) +
                    pow(srednia_Acer["c3"] - srednia_Quercus["c3"], 2))

macierz3A = np.array(klasa_Acer.loc[:, ["c1", "c2", "c3"]])
macierzSrednich3A = np.array(srednia_Acer.loc[["c1", "c2", "c3"]])
przedTrans3A = np.mat(macierz3A) - np.mat(macierzSrednich3A)
trans3A = przedTrans3A.T
        
result3A = np.mat(trans3A) * np.mat(przedTrans3A)
dzielnik3A = 1/len(macierz3A)
przedDet3A = dzielnik3A * result3A
det3A = np.linalg.det(przedDet3A)

macierz3B = np.array(klasa_Quercus.loc[:, ["c1", "c2", "c3"]])
macierzSrednich3B = np.array(srednia_Quercus.loc[["c1", "c2", "c3"]])
przedTrans3B = np.mat(macierz3B) - np.mat(macierzSrednich3B)
trans3B = przedTrans3B.T
        
result3B = np.mat(trans3B) * np.mat(przedTrans3B)
dzielnik3B = 1/len(macierz3B)
przedDet3B = dzielnik3B * result3B
det3B = np.linalg.det(przedDet3B)

wspolczynnikiF3 = (licznik / mianownik)