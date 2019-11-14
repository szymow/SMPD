# -*- coding: utf-8 -*-
"""
Create a GUI to import a CSV file into Python
"""
#Biblioteki GUI
import tkinter as tk
from tkinter import filedialog, Label
from tkinter.ttk import Combobox
import pandas as pd
import math

okno=tk.Tk()
okno.title("SMPD lab Szymon Woyda 227458")
okno.geometry('640x480')
etykieta=Label(okno, text=" Metody klasyfikacji: NN i kNN", font=("Arial",16))
etykieta.grid(column = 0, row = 0)

def getCSV():
    global dane
    sciezkaDoPliku = filedialog.askopenfilename()
    dane=pd.read_csv(sciezkaDoPliku)
    print(dane)

#Dane modyfikowane przez użytkownika    
def input_k():
    global wartosc_k
    wartosc_k = combo.get()
    wartosc_k = int(wartosc_k)
    print("wartosc_k = ", wartosc_k)
    
def input_trening():
    global liczba_probek_treningowych
    liczba_probek_treningowych = combo2.get()
    liczba_probek_treningowych = int(liczba_probek_treningowych)
    print("liczba_probek_treningowych = ", liczba_probek_treningowych)

def input_test():
    global liczba_probek_testowych
    liczba_probek_testowych = combo3.get()
    liczba_probek_testowych = int(liczba_probek_testowych)
    print("liczba_probek_testowych = ", liczba_probek_testowych)
    
przyciskImportujCSV = tk.Button(text=" Importuj CSV ", 
                             command=getCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
przyciskImportujCSV.grid(column=1, row=0)

etykieta3=Label(okno, text=" Liczba próbek treningowych: ", font=("Arial",12))
etykieta3.grid(column=0,row=1)

combo2 = Combobox(okno)
combo2['values']=(1,2,3,4,5,6,7,8,9,10,11,12,13)
combo2.current(7)
combo2.grid(column=1,row=1)

etykieta3=Label(okno, text=" Liczba próbek testowych: ", font=("Arial",12))
etykieta3.grid(column=0,row=2)

combo3 = Combobox(okno)
combo3['values']=(1,2,3,4,5)
combo3.current(1)
combo3.grid(column=1,row=2)

przyciskWybierzTrening = tk.Button(text=" Zatwierdź ", command=input_trening, bg='green', fg='white', font=('helvetica', 12, 'bold'))
przyciskWybierzTrening.grid(column=2, row=1)
przyciskWybierzTest = tk.Button(text=" Zatwierdź ", command=input_test, bg='green', fg='white', font=('helvetica', 12, 'bold'))
przyciskWybierzTest.grid(column=2, row=2)

etykieta2=Label(okno, text=" Wartość k dla metody kNN: \t", font=("Arial",12))
etykieta2.grid(column=0,row=3)

combo = Combobox(okno)
combo['values']=(1,2,3,4,5,6,7,8)
combo.current(2)
combo.grid(column=1,row=3)

przyciskWybierzK = tk.Button(text=" Zatwierdź ", command=input_k, bg='green', fg='white', font=('helvetica', 12, 'bold'))
przyciskWybierzK.grid(column=2, row=3)

okno.mainloop()
#https://likegeeks.com/python-gui-examples-tkinter-tutorial/

LPTest = liczba_probek_testowych
LPTrening = liczba_probek_treningowych

#Metoda NN najbliższy sąsiad
listaNN=[[],[],[],[],[]]

for kolejny in range(LPTest):
    for i in range(LPTrening):
        aktualny = LPTrening + kolejny
        listaNN[kolejny].append(math.sqrt(math.pow(dane.iloc[i]["c1"]-dane.iloc[aktualny]["c1"],2)
        + math.pow(dane.iloc[i]["c2"]-dane.iloc[aktualny]["c2"],2)
        + math.pow(dane.iloc[i]["c3"]-dane.iloc[aktualny]["c3"],2)))

min_index_NN=[]

NN_tak = 0
NN_nie = 0

for i in range(LPTest):
    min_index_NN.append((listaNN[i]).index(min(listaNN[i])))
    aktualny = LPTrening + i
    print(dane.iloc[aktualny])
    print("Szukany x dla metody NN należy do klasy: " + dane.iloc[aktualny]["klasa"])
    print("Według metody NN x należy do klasy: " + dane.iloc[min_index_NN[i]]["klasa"])

    if dane.iloc[min_index_NN[i]]["klasa"] is dane.iloc[aktualny]["klasa"]:
        print("Algorytm NN ma racje \n")
        NN_tak = NN_tak + 1
    else:
        print("Algorytm NN się pomylił \n")
        NN_nie = NN_nie + 1
        
print("Skutecznosc NN = ", (NN_tak/(NN_tak + NN_nie)*100), "% \n")


#Metoda kNN k najbliższych sąsiadów

lista_kNN=[[],[],[],[],[]]

for kolejny in range(LPTest):
    for i in range(LPTrening):
        aktualny = LPTrening + kolejny
        lista_kNN[kolejny].append(math.sqrt(math.pow(dane.iloc[i]["c1"]-dane.iloc[aktualny]["c1"],2) 
        + math.pow(dane.iloc[i]["c2"]-dane.iloc[aktualny]["c2"],2)
        + math.pow(dane.iloc[i]["c3"]-dane.iloc[aktualny]["c3"],2)))

odpowiedz_algorytmu_kNN = []

for odp in range(LPTest):

    slownik_kNN={}

    for j in range(LPTest):
        for i in range(LPTrening):
            klasa_probki = dane.iloc[i]["klasa"]
            slownik_kNN[klasa_probki,i]=lista_kNN[j][i]
            
    posortowany_slownik_kNN={}
            
    for key, value in sorted(slownik_kNN.items(), key=lambda item: item[1]):
        posortowany_slownik_kNN[key]=value

    klucze_kNN = [k for k, v in posortowany_slownik_kNN.items()]
    klucze_kNN_sum=list(sum(klucze_kNN[:wartosc_k],()))
    klucze_kNN_join=''.join(str(klucze_kNN_sum_e) for klucze_kNN_sum_e in klucze_kNN_sum)

    if klucze_kNN_join.count('A') > klucze_kNN_join.count('B'):
        odpowiedz = 'A'
    else:
        odpowiedz = 'B'
    
    odpowiedz_algorytmu_kNN.append(odpowiedz)
    
kNN_tak = 0
kNN_nie = 0

for i in range(LPTest):
    aktualny = LPTrening + i
    print("Szukany x dla metody kNN należy do klasy: " + dane.iloc[aktualny]["klasa"])
    print("Według metody kNN x należy do klasy: " + odpowiedz_algorytmu_kNN[i])
    print("Dla k = ", wartosc_k)
    if odpowiedz_algorytmu_kNN[i] is dane.iloc[aktualny]["klasa"]:
        print("Algorytm kNN ma racje \n")
        kNN_tak = kNN_tak + 1
    else:
        print("Algorytm kNN się pomylił \n")
        kNN_nie = kNN_nie + 1

print("Skutecznosc kNN = ", (kNN_tak/(kNN_tak + kNN_nie)*100), "% \n")
     
  
#Metoda NM najbliższych srednich
        
def Srednia(lst): 
    return sum(lst) / len(lst) 

probki_klasy_A_c1 = []
probki_klasy_A_c2 = []
probki_klasy_A_c3 = []
probki_klasy_B_c1 = []
probki_klasy_B_c2 = []
probki_klasy_B_c3 = []

for i in range(LPTrening):
    klasa_probki = dane.iloc[i]["klasa"]
    if klasa_probki is "A":
        probki_klasy_A_c1.append(dane.iloc[i]["c1"])
        probki_klasy_A_c2.append(dane.iloc[i]["c2"])
        probki_klasy_A_c3.append(dane.iloc[i]["c3"])
    if klasa_probki is "B":
        probki_klasy_B_c1.append(dane.iloc[i]["c1"])
        probki_klasy_B_c2.append(dane.iloc[i]["c2"])
        probki_klasy_B_c3.append(dane.iloc[i]["c3"])

srednia_klasy_A = [Srednia(probki_klasy_A_c1),Srednia(probki_klasy_A_c2),Srednia(probki_klasy_A_c3)]
srednia_klasy_B = [Srednia(probki_klasy_B_c1),Srednia(probki_klasy_B_c2),Srednia(probki_klasy_B_c3)]

NM_tak = 0
NM_nie = 0

for kolejny in range(LPTest):
    aktualny = LPTrening + kolejny
    szukany_x = dane.iloc[aktualny]
    DsAx = math.sqrt(math.pow(srednia_klasy_A[0]-szukany_x[0],2) + math.pow(srednia_klasy_A[1]-szukany_x[1],2) + math.pow(srednia_klasy_A[2]-szukany_x[2],2))
    DsBx = math.sqrt(math.pow(srednia_klasy_B[0]-szukany_x[0],2) + math.pow(srednia_klasy_B[1]-szukany_x[1],2) + math.pow(srednia_klasy_B[2]-szukany_x[2],2))

    print("DsAx = ",DsAx)
    print("DsBx = ",DsBx)
    
    if DsAx < DsBx:
        odpowiedz = 'A'
    else:
        odpowiedz = 'B'
    
    print("Szukany x dla metody kNN należy do klasy: " + dane.iloc[aktualny]["klasa"])
    print("Według metody NM x należy do klasy: " + odpowiedz)
    if odpowiedz is dane.iloc[aktualny]["klasa"]:
        print("Algorytm NM ma racje \n")
        NM_tak = NM_tak + 1
    else:
        print("Algorytm NM się pomylił \n")
        NM_nie = NM_nie + 1
        
print("Skutecznosc NM = ", (NM_tak/(NM_tak + NM_nie)*100), "% \n")