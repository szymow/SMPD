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
    dane = pd.read_csv(sciezkaDoPliku)
    #Losowanie kolejnosci próbek
    dane = dane.sample(frac=1)
    print(dane)

#Dane modyfikowane przez użytkownika    
def input_k():
    global wartosc_k
    wartosc_k = combo.get()
    wartosc_k = int(wartosc_k)
    print("wartosc_k = ", wartosc_k)
    
def input_trening():
    global procent_probek_treningowych
    procent_probek_treningowych = combo2.get()
    procent_probek_treningowych = int(procent_probek_treningowych)
    global liczba_probek_treningowych
    liczba_probek_treningowych = procent_probek_treningowych * (1/100) * len(dane)
    liczba_probek_treningowych = int(liczba_probek_treningowych)
    print("liczba_probek_treningowych = ", liczba_probek_treningowych)
    global liczba_probek_testowych
    liczba_probek_testowych = len(dane) - liczba_probek_treningowych
    liczba_probek_testowych = int(liczba_probek_testowych)
    print("liczba_probek_testowych = ", liczba_probek_testowych)

przyciskImportujCSV = tk.Button(text=" Importuj polosowany CSV ", 
                             command=getCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
przyciskImportujCSV.grid(column=1, row=0)

etykieta3=Label(okno, text=" Procent próbek treningowych: [%]", font=("Arial",12))
etykieta3.grid(column=0,row=1)

combo2 = Combobox(okno)
combo2['values']=(10,20,30,40,50,60,70,80,90)
combo2.current(7)
combo2.grid(column=1,row=1)

przyciskWybierzTrening = tk.Button(text=" Zatwierdź ", command=input_trening, bg='green', fg='white', font=('helvetica', 12, 'bold'))
przyciskWybierzTrening.grid(column=2, row=1)

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
listaNN=[]

for kolejny in range(LPTest):
    for i in range(LPTrening):
        aktualny = LPTrening + kolejny
        listaNN.append(math.sqrt(math.pow(dane.iloc[i]["c1"]-dane.iloc[aktualny]["c1"],2)
        + math.pow(dane.iloc[i]["c2"]-dane.iloc[aktualny]["c2"],2)
        + math.pow(dane.iloc[i]["c3"]-dane.iloc[aktualny]["c3"],2)))

min_index_NN=[]

NN_tak = 0
NN_nie = 0

for i in range(LPTest):
    #0:8; 8:16; 16:32 itd.
    min_index_NN.append((listaNN[(LPTrening*i):(LPTrening*(i+1))]).index(min(listaNN[(LPTrening*i):(LPTrening*(i+1))])))
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

lista_kNN=[]

for kolejny in range(LPTest):
    for i in range(LPTrening):
        aktualny = LPTrening + kolejny
        lista_kNN.append(math.sqrt(math.pow(dane.iloc[i]["c1"]-dane.iloc[aktualny]["c1"],2) 
        + math.pow(dane.iloc[i]["c2"]-dane.iloc[aktualny]["c2"],2)
        + math.pow(dane.iloc[i]["c3"]-dane.iloc[aktualny]["c3"],2)))

odpowiedz_algorytmu_kNN = []

for odp in range(LPTest):

    slownik_kNN={}

    for j in range(LPTest):
        for i in range(LPTrening):
            klasa_probki = dane.iloc[i]["klasa"]
            #0 -> 13; 13 -> 26
            slownik_kNN[klasa_probki,i]=lista_kNN[LPTrening*j+i]
            
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

LiczbaCech = 3

probki_klasy_A = []
probki_klasy_B = []

probki_klasy_A_c = []
srednia_klasy_A = []

probki_klasy_B_c = []
srednia_klasy_B = []

for i in range(LPTrening):
    klasa_probki = dane.iloc[i]["klasa"]
    if klasa_probki is "A":
        for j in range(LiczbaCech): 
            probki_klasy_A.append(dane.iloc[i][j])
    if klasa_probki is "B":
        for j in range(LiczbaCech):
            probki_klasy_B.append(dane.iloc[i][j])

for i in range(LiczbaCech):
    #pobieramy kolejne wartosci z listy co Liczbę Cech
    for j in range(int(len(probki_klasy_A)/LiczbaCech)):
        probki_klasy_A_c.append(probki_klasy_A[i + LiczbaCech * j])
    srednia_klasy_A.append(Srednia(probki_klasy_A_c))
    probki_klasy_A_c = []
    
for i in range(LiczbaCech):
    for j in range(int(len(probki_klasy_B)/LiczbaCech)):
        probki_klasy_B_c.append(probki_klasy_B[i + LiczbaCech * j])
    srednia_klasy_B.append(Srednia(probki_klasy_B_c))
    probki_klasy_B_c = []

print("srednia_klasy_A = ",srednia_klasy_A)
print("srednia_klasy_B = ",srednia_klasy_B)

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

print("probki_klasy_A = ",probki_klasy_A)

#Metoda kNM k najbliższych srednich

listOfc1 =  [probki_klasy_A[0], probki_klasy_A[3], probki_klasy_A[6]]
listOfc2   =  [probki_klasy_A[1], probki_klasy_A[4], probki_klasy_A[7]]
listOfc3  =  [probki_klasy_A[2], probki_klasy_A[5], probki_klasy_A[8]]
listOfPodklasa = ['A1','A2','A3']

zippedList =  list(zip(listOfc1, listOfc2, listOfc3,listOfPodklasa))

dfObj = pd.DataFrame(zippedList, columns = ['c1' , 'c2', 'c3', 'podklasa'])