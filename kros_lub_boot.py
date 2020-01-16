# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 18:20:17 2020

@author: Szymon

Kroswalidacja i Bootstrap
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
etykieta=Label(okno, text=" Trening / Test", font=("Arial",16))
etykieta.grid(column = 0, row = 0)

def getCSV():
    global dane
    sciezkaDoPliku = filedialog.askopenfilename()
    dane = pd.read_csv(sciezkaDoPliku, sep = ',')
    print(dane)
    
def start():
    global kros_lub_boot
    kros_lub_boot = v.get()
    if kros_lub_boot == 1:
        print("Kroswalidacja")
        global lck # Liczba czesci Kroswalidacja
        global lpk # Liczba powtorzen Kroswalidacja
        lck = combo1.get()
        lpk = combo2.get()
        lck = int(lck)
        lpk = int(lpk)
        print("Liczba czesci: ", lck)
        print("Liczba powtorzen: ", lpk)
    elif kros_lub_boot == 2:
        print("Bootstrap")
        global pcb # Procent cech Bootstrap
        global lpb # Liczba powtorzen Bootstrap
        pcb = combo3.get()
        lpb = combo4.get()
        pcb = int(pcb)
        lpb = int(lpb)
        print("Prcent cech: ", pcb)
        print("Liczba powtorzen: ", lpb)
    else:
        print("Wybierz Kroswalidacja lub Bootstrap")
        

przyciskImportujCSV = tk.Button(text=" Importuj CSV ", 
                             command=getCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
przyciskImportujCSV.grid(column=2, row=0)

start = tk.Button(text=" Start ", 
                             command=start, bg='green', fg='white', font=('helvetica', 12, 'bold'))
start.grid(column=2, row=3)


v = tk.IntVar()

r1 = tk.Radiobutton(okno, text="Kroswalidacja", font=("Arial",16), variable=v, value=1)
r2 = tk.Radiobutton(okno, text="Bootstrap", font=("Arial",16), variable=v, value=2)

r1.grid(column = 0, row = 1)
r2.grid(column = 0, row = 2)

combo1 = Combobox(okno)
combo1['values']=(3,4,5)
combo1.current(1)
combo1.grid(column=1,row=1)

combo2 = Combobox(okno)
combo2['values']=(1,2,3,4,5)
combo2.current(1)
combo2.grid(column=2,row=1)

combo3 = Combobox(okno)
combo3['values']=(10,20,30,40,50)
combo3.current(1)
combo3.grid(column=1,row=2)

combo4 = Combobox(okno)
combo4['values']=(1,2,3,4,5)
combo4.current(1)
combo4.grid(column=2,row=2)

okno.mainloop()
#https://likegeeks.com/python-gui-examples-tkinter-tutorial/

'''
#Dzielenie na 2 klasy
klasa_Acer = dane[0:176]
klasa_Quercus = dane[176:]

#Pozbycie sie wartosci nieliczbowych
klasa_Acer = klasa_Acer.drop(columns=["64"])
klasa_Quercus = klasa_Quercus.drop(columns=["64"])

#Srednia cech
srednia_Acer = klasa_Acer.mean(axis = 0)
srednia_Quercus = klasa_Quercus.mean(axis = 0)

#Transponowanie
A = klasa_Acer.T
B = klasa_Quercus.T

A = np.array(A)
B = np.array(B)
'''

lck = 3 # Liczba czesci Kroswalidacja
lpk = 5 # Liczba powtorzen Kroswalidacja

pcb = 20 # Procent cech Bootstrap
lpb = 3 # Liczba powtorzen Bootstrap

dane = dane.sample(frac=1)
z = int(len(dane)/lck)
test = dane[:z]
trening = dane[z:]

test = test.reset_index(drop=True)

test_odp = test["64"]
test_odp = test_odp.reset_index(drop=True)
for x in range(int(len(test_odp))):
    if "Acer" in test_odp[x]:
        test_odp[x] = 'A'
    if "Quercus" in test_odp[x]:
        test_odp[x] = 'Q'
test_odp = list(test_odp)
    

test = test.drop(columns=["64"])

test = test.T


#Dzielenie na klasy treningu

trening = trening.reset_index(drop=True)

trening = trening.T

klasa_Acer = pd.DataFrame()
klasa_Quercus = pd.DataFrame()


for i in range(int(len(trening.columns))):
    klasa_probki = trening[i][0]
    if "Acer" in klasa_probki:
        tren = trening[i][1:]
        tren = np.array(tren, dtype='float')
        klasa_Acer.insert(0,i,tren)
    if "Quercus" in klasa_probki:
        tren = trening[i][1:]
        tren = np.array(tren, dtype='float')
        klasa_Quercus.insert(0,i,tren)


klasa_Acer = klasa_Acer.T.reset_index(drop=True).T  
klasa_Quercus = klasa_Quercus.T.reset_index(drop=True).T      

lc = len(klasa_Acer) # Liczba cech

# Klasyfikacja NN

def klasNN():
    
    t = int(len(test.columns))
    a = int(len(klasa_Acer.columns))
    q = int(len(klasa_Quercus.columns))

    suma_A_k = []
    suma_Q_k = []    

    suma_A = []
    suma_Q = []
    

    for k in range(t):
        for j in range(a):
            suma = 0
            for i in range(lc):
                suma = suma + pow(klasa_Acer[j][i] - test[k][i],2)
            suma = math.sqrt(suma)
            suma_A.append(suma)
        suma_A_k.append(suma_A)
        suma_A = []
        for j in range(q):
            suma = 0
            for i in range(lc):
                suma = suma + pow(klasa_Quercus[j][i] - test[k][i],2)
            suma = math.sqrt(suma)
            suma_Q.append(suma)
        suma_Q_k.append(suma_Q)
        suma_Q = []
        

    obl_A = pd.DataFrame(data=np.array(suma_A_k).reshape(a,t))
    obl_Q = pd.DataFrame(data=np.array(suma_Q_k).reshape(q,t))
    
    odp = []
    for x in range(t):
        if min(obl_A[x]) < min(obl_Q[x]):
            odp.append('A')
        else:
            odp.append('Q')
    print(odp)
    print(test_odp)

    # Python code to find the index at which the  
    # element of two list match. 
      
    # List initialisation 
    Input1 = test_odp
    Input2 = odp
      
    # Using list comprehension and zip  
    Output = [Input2.index(y) for x, y in
           zip(Input1, Input2) if y == x] 
      
    # Printing output
    print("Skutecznosc: ", len(Output)/t * 100, "%")

