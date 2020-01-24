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
    global sciezkaDoPliku
    sciezkaDoPliku = filedialog.askopenfilename()
    dane = pd.read_csv(sciezkaDoPliku, sep = ',')
    print(dane)
    
def start():
    global fisher_lub_sfs
    fisher_lub_sfs = v.get()
    if fisher_lub_sfs == 1:
        print("Fisher")
        global lcf # Liczba cech Fisher
        lcf = combo1.get()
        lcf = int(lcf)
        print("Liczba cech: ", lcf)
    elif fisher_lub_sfs == 2:
        print("SFS")
        global liczbacech #Zadana liczba najlepszych cech (SFS)
        liczbacech = combo2.get()
        liczbacech = int(liczbacech)
        print("Liczba cech: ", liczbacech)
    else:
        print("Wybierz Fisher lub SFS")
        

przyciskImportujCSV = tk.Button(text=" Importuj CSV ", 
                             command=getCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
przyciskImportujCSV.grid(column=1, row=0)

start = tk.Button(text=" Start ", 
                             command=start, bg='green', fg='white', font=('helvetica', 12, 'bold'))
start.grid(column=1, row=3)


v = tk.IntVar()

r1 = tk.Radiobutton(okno, text="Fisher", font=("Arial",16), variable=v, value=1)
r2 = tk.Radiobutton(okno, text="SFS", font=("Arial",16), variable=v, value=2)

r1.grid(column = 0, row = 1)
r2.grid(column = 0, row = 2)

combo1 = Combobox(okno)
combo1['values']=(1,2,3)
combo1.current(1)
combo1.grid(column=1,row=1)

combo2 = Combobox(okno)
combo2['values']=(1,2,3,4,5,6,7,8)
combo2.current(6)
combo2.grid(column=1,row=2)

okno.mainloop()
#https://likegeeks.com/python-gui-examples-tkinter-tutorial/

#Dzielenie na 2 klasy
#Wersja przyspieszona dla Maple_Oak oraz wersja dluzsza dla pozostalych plikow (trening.csv)
if "Maple_Oak" in sciezkaDoPliku:
    klasa_Acer = dane[:176]
    klasa_Quercus = dane[176:]
    
    #Pozbycie sie wartosci nieliczbowych
    klasa_Acer = klasa_Acer.drop(columns=["64"])
    klasa_Quercus = klasa_Quercus.drop(columns=["64"])
    
elif "rece" in sciezkaDoPliku:
    klasa_Acer = dane[:12]
    klasa_Quercus = dane[12:]
    
    #Pozbycie sie wartosci nieliczbowych
    klasa_Acer = klasa_Acer.drop(columns=["64"])
    klasa_Quercus = klasa_Quercus.drop(columns=["64"])
    
else:
    klasa_Acer = pd.DataFrame()
    klasa_Quercus = pd.DataFrame()
    d = len(dane)
    for i in range(d):
        if "Acer" in dane["64"][i]:
            tren = dane.loc[i][1:]
            tren = np.array(tren, dtype='float')
            klasa_Acer.insert(0,i,tren)
        if "Quercus" in dane["64"][i]:
            tren = dane.loc[i][1:]
            tren = np.array(tren, dtype='float')
            klasa_Quercus.insert(0,i,tren)
    klasa_Acer = klasa_Acer.T.reset_index(drop=True).T  
    klasa_Quercus = klasa_Quercus.T.reset_index(drop=True).T
    
    
if "Maple_Oak" or "rece" in sciezkaDoPliku:
    #Srednia cech
    srednia_Acer = klasa_Acer.mean(axis = 0)
    srednia_Quercus = klasa_Quercus.mean(axis = 0)
else:
    srednia_Acer = klasa_Acer.mean(axis = 1)
    srednia_Quercus = klasa_Quercus.mean(axis = 1)
            

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


if "Maple_Oak" or "rece" in sciezkaDoPliku:
    odchylenie_std_Acer = odchylenie_std(klasa_Acer, srednia_Acer)
    odchylenie_std_Quercus = odchylenie_std(klasa_Quercus, srednia_Quercus)
else:
    odchylenie_std_Acer = odchylenie_std(klasa_Acer.T, srednia_Acer)
    odchylenie_std_Quercus = odchylenie_std(klasa_Quercus.T, srednia_Quercus)


wspolczynniki = []
for i in range(int(len(srednia_Acer))):
    licznik = abs(srednia_Acer[i] - srednia_Quercus[i])
    mianownik = (odchylenie_std_Acer[i] + odchylenie_std_Quercus[i])
    liczba = licznik / mianownik
    wspolczynniki.append(liczba)


najlepszaCecha = wspolczynniki.index(max(wspolczynniki))
print("najlepszaCecha Fisher dla jednej cechy to: ",najlepszaCecha)

from itertools import product, permutations

if "Maple_Oak" or "rece" in sciezkaDoPliku:
    #Transponowanie
    A = klasa_Acer.T
    B = klasa_Quercus.T
else:
    A = klasa_Acer
    B = klasa_Quercus

A = np.array(A)
B = np.array(B)

sredniaA = np.array(srednia_Acer)
sredniaB = np.array(srednia_Quercus)

nX = np.size(A,0) #Liczba cech
nA = np.size(A,1) #Liczba probek
nB = np.size(B,1)

DZIELNIK_A = 1/nA
DZIELNIK_B = 1/nB

def Fisher():
    permutacja = list(permutations(np.arange(nX), lcf))
    permutacja = np.array(permutacja)
    
    maks = 0
    
    from time import perf_counter
    t1_start = perf_counter() 
    
    for iterator in permutacja:
        #Sledzenie postepu dla 2 najlepszych cech
        if lcf==2:
            if iterator[0]==(iterator[1]-1):
                print (iterator[0],"/",nX)
        if lcf==3:
            if iterator[0]==(iterator[1]-1)==(iterator[2]-2):
                print (iterator[0],"/",nX)
        licznik = 0
        macA = []
        macB = []
    
        for i in iterator:
            licznik = licznik + (pow(sredniaA[i] - sredniaB[i],2))
            for j in range(nA):
                macA.append(A[i][j] - sredniaA[i])
            for j in range(nB):
                macB.append(B[i][j] - sredniaB[i])
        licznik = math.sqrt(licznik)
            
        macA = np.array(macA)
        macB = np.array(macB)
            
        macA = macA.reshape(lcf,nA)
        macB = macB.reshape(lcf,nB)
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
    print("Policzone metoda Fisher")
    return maks_cechy

def SFS():
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
                for j in range(nA):
                    macA.append(A[i][j] - sredniaA[i])
                for j in range(nB):
                    macB.append(B[i][j] - sredniaB[i])
                licznik = math.sqrt(licznik)
            
            macA = np.array(macA)
            macB = np.array(macB)
            
            macA = macA.reshape(lc,nA)
            macB = macB.reshape(lc,nB)
            
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
                        if "Maple_Oak" in sciezkaDoPliku:
                            if 63 in d: break
                        if "rece" in sciezkaDoPliku:
                            if 62 in d: break
                prod = e
    
    
    t1_stop = perf_counter()
    print("Elapsed time:", round(t1_stop - t1_start,2), "s")
    print("Policzone metoda SFS")
    return maks_cechy


if fisher_lub_sfs == 1:
    maks_cech = Fisher()

if fisher_lub_sfs == 2:
    maks_cech = SFS()


#Ograniczamy zbior treningowy tylko do najlepszych cech

print(maks_cech)
najlepsze = dane.iloc[:, [0]]
i = 0
for x in maks_cech:
    i = i + 1
    tren = dane.iloc[ : , [x] ]
    najlepsze.insert(i,x,tren)
    
if "Maple_Oak" in sciezkaDoPliku:
    najlepsze.to_csv("Maple_Oak_najlepsze.csv", index=False)
    print("Wygenerowano plik: Maple_Oak_najlepsze.csv")
    print("Wroc kros_lub_boot aby dokonac Kroswalidacji.")
else:
    najlepsze.to_csv("najlepsze.csv", index=False)
    print("Wygenerowano plik: najlepsze.csv")
    print("Wroc kros_lub_boot aby dokonac Kroswalidacji.")
    


