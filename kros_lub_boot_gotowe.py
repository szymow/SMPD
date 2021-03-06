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
    
def potwierdz():
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

def potwierdz2():
    global klasyfi
    global liczba_k
    global podklasa
    global liczbaPodklas
    klasyfi = v1.get()
    if klasyfi == 1:
        print("NN")
    elif klasyfi == 2:
        print("kNN")
        liczba_k = combo5.get()
        liczba_k = int(liczba_k)
        print("Liczba k: ", liczba_k)
    elif klasyfi == 3:
        print("NM")
    elif klasyfi == 4:
        print("kNM")
        liczbaPodklas = combo5.get()
        liczbaPodklas = int(liczbaPodklas)
        liczba_k = liczbaPodklas
        podklasa = combo6.get()
        print("Liczba k: ", liczbaPodklas)
        print("Podklasa: ", podklasa)
    else:
        print("Wybierz NN / kNN / NM / kNM")
        

przyciskImportujCSV = tk.Button(text=" Importuj CSV ", 
                             command=getCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
przyciskImportujCSV.grid(column=2, row=0)

potwierdz = tk.Button(text=" Potwierdz ", 
                             command=potwierdz, bg='green', fg='white', font=('helvetica', 12, 'bold'))
potwierdz.grid(column=2, row=3)

potwierdz2 = tk.Button(text=" Potwierdz ", 
                             command=potwierdz2, bg='green', fg='white', font=('helvetica', 12, 'bold'))
potwierdz2.grid(column=2, row=8)


v = tk.IntVar()

r1 = tk.Radiobutton(okno, text="Kroswalidacja", font=("Arial",16), variable=v, value=1)
#r2 = tk.Radiobutton(okno, text="Bootstrap", font=("Arial",16), variable=v, value=2)

r1.grid(column = 0, row = 1)
#r2.grid(column = 0, row = 2)

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
#combo3.grid(column=1,row=2)

combo4 = Combobox(okno)
combo4['values']=(1,2,3,4,5)
combo4.current(1)
#combo4.grid(column=2,row=2)

etykieta2=Label(okno, text=" Klasyfikacja ", font=("Arial",16))
etykieta2.grid(column = 0, row = 4)

v1 = tk.IntVar()

r3 = tk.Radiobutton(okno, text="NN", font=("Arial",16), variable=v1, value=1)
r4 = tk.Radiobutton(okno, text="kNN", font=("Arial",16), variable=v1, value=2)
r5 = tk.Radiobutton(okno, text="NM", font=("Arial",16), variable=v1, value=3)
r6 = tk.Radiobutton(okno, text="kNM", font=("Arial",16), variable=v1, value=4)

r3.grid(column = 0, row = 5)
r4.grid(column = 1, row = 5)
r5.grid(column = 0, row = 6)
r6.grid(column = 1, row = 6)


etykieta3=Label(okno, text=" Wybierz k [kNN/kNM]: ", font=("Arial",12))
etykieta3.grid(column = 0, row = 7)

combo5 = Combobox(okno)
combo5['values']=(1,2,3,4,5,6,7,8,9,10)
combo5.current(1)
combo5.grid(column=1,row=7)

combo6 = Combobox(okno)
combo6['values']=('A','Q')
combo6.current(0)
combo6.grid(column=2,row=6)

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

#lck = 3 # Liczba czesci Kroswalidacja
#lpk = 5 # Liczba powtorzen Kroswalidacja

#pcb = 20 # Procent cech Bootstrap
#lpb = 3 # Liczba powtorzen Bootstrap

def dzielenie_test_trening():
    global dane
    global test
    global trening
    global test_odp
    global klasa_Acer
    global klasa_Quercus
    
    dane = dane.sample(frac=1)
    z = int(len(dane)/lck)
    test = dane[:z]
    trening = dane[z:]
    
    test = test.reset_index(drop=True)
    
    test_odp = test["64"]
    test_odp = test_odp.reset_index(drop=True)
    for x in range(int(len(test_odp))):
        if ("Acer" or "otwarta") in test_odp[x]:
            test_odp[x] = 'A'
        if ("Quercus" or "zamknieta") in test_odp[x]:
            test_odp[x] = 'Q'
    test_odp = list(test_odp)
        
    
    test = test.drop(columns=["64"])
    
    test = test.T
    
    
    #Dzielenie na klasy treningu
    
    trening = trening.reset_index(drop=True)
    
    trening.to_csv("trening.csv", index=False)
    
    print("Wygenerowano plik: trening.csv")
    print("Dokonaj Fishera lub SFS aby wybrac najlepsze cechy.")
    print("Wroc tutaj aby przeprowadzic Kroswalidacje na pliku trening_naj.csv")
    
    trening = trening.T
    
    
    klasa_Acer = pd.DataFrame()
    klasa_Quercus = pd.DataFrame()
    
    tc = len(trening.columns)
    
    for i in range(tc):
        klasa_probki = trening[i][0]
        if ("Acer" or "otwarta") in klasa_probki:
            tren = trening[i][1:]
            tren = np.array(tren, dtype='float')
            klasa_Acer.insert(0,i,tren)
        if ("Quercus" or "zamknieta") in klasa_probki:
            tren = trening[i][1:]
            tren = np.array(tren, dtype='float')
            klasa_Quercus.insert(0,i,tren)
    
    
    klasa_Acer = klasa_Acer.T.reset_index(drop=True).T  
    klasa_Quercus = klasa_Quercus.T.reset_index(drop=True).T      


# Klasyfikacja kNN
def klasyfikacja_kNN():
    lc = len(klasa_Acer) # Liczba cech
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
    
    # Klasyfikacja kNN    
    
    keys_a = ["A{}".format(i) for i in obl_A.index]
    keys_q = ["Q{}".format(i) for i in obl_Q.index]
    
    dict_a = []
    for x in obl_A.columns:
        values_a = list(obl_A[x])
        dict_a.append(dict(zip(keys_a, values_a)))
        
    dict_q = []
    for x in obl_Q.columns:
        values_q = list(obl_Q[x])
        dict_q.append(dict(zip(keys_q, values_q)))
    
    dict_w = dict_a.copy()
    for i in range(t):
        dict_w[i].update(dict_q[i])
        
# Sortowanie

    dict_w_sort = []
    dict_w_sorted = []
    dict_w_sorted_c = []
    dict_w_sorted_c_w = []
    odp_kNN = []
    
    for i in range(t):
        dict_w_sort.append({k: v for k, v in sorted(dict_w[i].items(), 
                                                    key=lambda item: item[1])})
    for i in range(t):    
        dict_w_sorted.append(list(np.array(list(dict_w_sort[i].items())).flatten()))
        
        
    for i in range(t):
        j = 0
        for j in list(range(0,(np.size(dict_w_sorted,1)),2)):
            dict_w_sorted_c.append(dict_w_sorted[i][j])
    
    dict_w_sorted_c = np.array(dict_w_sorted_c).reshape(t,a+q)
    
    for i in range(t):
        dict_w_sorted_c_w.append(dict_w_sorted_c[i][:liczba_k])
        
    for i in range(t):
        if list(dict_w_sorted_c_w[i]).count('A') > list(dict_w_sorted_c_w[i]).count('Q'):
            odp_kNN.append('A')
        else:
            odp_kNN.append('Q')
            
    Input1 = test_odp
    Input3 = odp_kNN
      
    # Using list comprehension and zip  
    Output3 = [Input1.index(y) for x, y in
               zip(Input3, Input1) if y == x]
    
    # Printing output
    print("Klasyfikacja kNN ")
    print("Liczba k: ", liczba_k)
    print("Skutecznosc: ", len(Output3)/t * 100, "%")


# Klasyfikacja NN
def klasyfikacja_NN():
    
    lc = len(klasa_Acer) # Liczba cech
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
    #print(odp)
    #print(test_odp)

    # Python code to find the index at which the  
    # element of two list match. 
      
    # List initialisation 
    Input1 = test_odp
    Input2 = odp
      
    # Using list comprehension and zip  
    Output = [Input2.index(y) for x, y in
           zip(Input1, Input2) if y == x] 
    

    # Printing output
    print("Klasyfikacja NN ")
    print("Skutecznosc: ", len(Output)/t * 100, "%")
    

def klasyfikacja_NM():
    lc = len(klasa_Acer) # Liczba cech
    t = int(len(test.columns))
    
    srednia_klas_A = klasa_Acer.mean(axis=1)
    srednia_klas_Q = klasa_Quercus.mean(axis=1)
    
    odp_NM_a = []
    odp_NM_q = []
    
    for k in range(t):
        suma = 0
        for i in range(lc):
            suma = suma + pow(srednia_klas_A[i] - test[k][i], 2)
        suma = math.sqrt(suma)
        odp_NM_a.append(suma)
        
        suma = 0
        for i in range(lc):
            suma = suma + pow(srednia_klas_Q[i] - test[k][i], 2)
        suma = math.sqrt(suma)
        odp_NM_q.append(suma)
        
    odp_NN = []
    for i in range(lc):
        if odp_NM_a[i] < odp_NM_q[i]:
            odp_NN.append('A')
        else:
            odp_NN.append('Q')
            
    # List initialisation
    Input1 = test_odp
    Input4 = odp_NN
      
    # Using list comprehension and zip  
    Output4 = [Input4.index(y) for x, y in
           zip(Input1, Input4) if y == x] 
    

    # Printing output
    print("Klasyfikacja NM ")
    print("Skutecznosc: ", len(Output4)/t * 100, "%")
    

def klasyfikacja_kNM():
    global probki_klasy_A_kNM
    probki_klasy_A_kNM = pd.DataFrame(columns=["c1", "c2", "c3"])
    
    for i in range(int(len(dane))):
        klasa_probki = dane.iloc[i]["64"]
        if klasa_probki is "A":
            probki_klasy_A_kNM.loc[i] = dane.iloc[i]
    
    probki_klasy_A_kNM = probki_klasy_A_kNM.reset_index(drop=True)        
    probki_klasy_A_kNM["podklasa"] = ""
    
    #liczbaPodklas = 3
    index = liczbaPodklas + 1
    
    podklasy = ["A{}".format(i) for i in range(1, index)]
    
    for i in range(liczbaPodklas):      
        probki_klasy_A_kNM.loc[i]["podklasa"] = podklasy[i]
    
    for i in range(int((len(probki_klasy_A_kNM)) - liczbaPodklas)):
        odleglosc_od_podklasy = []
        
        for j in range(liczbaPodklas):
            DsAjx = math.sqrt(math.pow(probki_klasy_A_kNM.iloc[j]["c1"] - 
                                       probki_klasy_A_kNM.iloc[liczbaPodklas + i]["c1"],2) 
                + math.pow(probki_klasy_A_kNM.iloc[j]["c2"] - probki_klasy_A_kNM.iloc[liczbaPodklas + i]["c2"],2) 
                + math.pow(probki_klasy_A_kNM.iloc[j]["c3"] - probki_klasy_A_kNM.iloc[liczbaPodklas + i]["c3"],2))
            odleglosc_od_podklasy.append(DsAjx)
    
        index_min_odleglosc = odleglosc_od_podklasy.index(min(odleglosc_od_podklasy))
        podklasa = probki_klasy_A_kNM.iloc[index_min_odleglosc]["podklasa"]
        
        probki_klasy_A_kNM.loc[liczbaPodklas + i]["podklasa"] = podklasa
    
    def przypisywanie_do_podklas(probki,srednie):
        for i in range(int(len(probki))):
            odleglosc = []      #odleglosc_od_podklasy
        
            for j in range(liczbaPodklas):
                DsAjx = math.sqrt(math.pow(srednie.iloc[j]["c1"] - probki.iloc[i]["c1"],2) 
                    + math.pow(srednie.iloc[j]["c2"] - probki.iloc[i]["c2"],2) 
                    + math.pow(srednie.iloc[j]["c3"] - probki.iloc[i]["c3"],2))
                odleglosc_od_podklasy.append(DsAjx)
    
            indeks = odleglosc.index(min(odleglosc))   #index_min_odleglosc
            podklasa = srednie.iloc[indeks]["podklasa"]
        
            probki.loc[i]["podklasa"] = podklasa
        return probki
    
    import itertools
    
    def dzielenie_na_podklasy(probki):
        
        podklasa_A123 = []
        
        for wartosc_podklasy in podklasy:
            temp_df = probki_klasy_A_kNM.loc[probki_klasy_A_kNM.podklasa == wartosc_podklasy, "c1":"c3"]
            temp = temp_df.values.tolist()
            # Zmiana multidimentional list na one dimentional
            temp_list = list(itertools.chain(*temp))
            podklasa_A123.append(temp_list)
            podklasa_A123.append(wartosc_podklasy)
        
        return podklasa_A123
    
    def obliczenie_wartosci_srednich(podzielone):
    
        srednie = pd.DataFrame(columns=["c1", "c2", "c3", "podklasa"]) #wartosci_srednie_kNM
        indeks = 0
        
        for element in podzielone:
        
            if type(element) is list:
                probki = []     #probki_podklasy_kNM_c
                srednia = []    #srednia_podklasy_kNM
            
                for i in range(LiczbaCech):
                    #pobieramy kolejne wartosci z listy co Liczbę Cech
                    for j in range(int(len(element)/LiczbaCech)):
                        probki.append(element[i + LiczbaCech * j])
                    if(len(probki) is not 0):
                        srednia.append(Srednia(probki))
                    else:
                        srednia.append(0)
                    probki = []
        
            if type(element) is str:
                srednia.append(element)    
                srednie.loc[indeks] = srednia
                indeks = indeks + 1
                
        return srednie
    
    def kolejny_krok_obliczen(probki, srednie):
    
        kolejny = pd.DataFrame(columns=["c1", "c2", "c3", "podklasa"]) #kolejny_df_kNM
    
        for i in range(int(len(probki))):
            odleglosc = [] #odleglosc_od_podklasy
        
            for j in range(liczbaPodklas):
                DsAjx = math.sqrt(math.pow(srednie.iloc[j]["c1"] - probki.iloc[i]["c1"],2) + 
                                  math.pow(srednie.iloc[j]["c2"] - probki.iloc[i]["c2"],2) + 
                                  math.pow(srednie.iloc[j]["c3"] - probki.iloc[i]["c3"],2))
                odleglosc.append(DsAjx)
    
            indeks = odleglosc.index(min(odleglosc)) #index_min_odleglosc
            podklasa = srednie.iloc[indeks]["podklasa"]
    
            kolejny.loc[i] = [probki.iloc[i]["c1"], probki.iloc[i]["c2"], probki.iloc[i]["c3"], podklasa]
            
        return kolejny
        
    def porownanie_dopasowania(poprzedni,kolejny):
        return sum(poprzedni["podklasa"] == kolejny["podklasa"]) == len(kolejny["podklasa"])
    
    def oblicz_kNM(poprzedni):
        podzielone_probki = dzielenie_na_podklasy(poprzedni)
        print(podzielone_probki)
        wartosci_srednie = obliczenie_wartosci_srednich(podzielone_probki)
        print(wartosci_srednie)
        nastepny = kolejny_krok_obliczen(poprzedni, wartosci_srednie)
        print(nastepny)
        return nastepny


if klasyfi == 1:
    for i in range(lpk):
        dzielenie_test_trening()
        klasyfikacja_NN()

if klasyfi == 2:
    for i in range(lpk):
        dzielenie_test_trening()
        klasyfikacja_kNN()
    
if klasyfi == 3:
    for i in range(lpk):
        dzielenie_test_trening()
        klasyfikacja_NM()

if klasyfi == 4:
    for i in range(lpk):
        dzielenie_test_trening()
        klasyfikacja_kNN()
