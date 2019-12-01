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

def input_kNM():
    global liczbaPodklas
    liczbaPodklas = combo3.get()
    liczbaPodklas = int(liczbaPodklas)
    print("liczbaPodklas = ", liczbaPodklas)

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

etykieta4=Label(okno, text=" Liczba podklas k dla metody kNM: \t", font=("Arial",12))
etykieta4.grid(column=0,row=4)

combo3 = Combobox(okno)
combo3['values']=(1,2,3,4,5,6,7,8)
combo3.current(2)
combo3.grid(column=1,row=4)

przyciskWybierzKNM = tk.Button(text=" Zatwierdź ", command=input_kNM, bg='green', fg='white', font=('helvetica', 12, 'bold'))
przyciskWybierzKNM.grid(column=2, row=4)

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

probki_klasy_A_NM = []
probki_klasy_B_NM = []

probki_klasy_A_NM_c = []
srednia_klasy_A_NM = []

probki_klasy_B_NM_c = []
srednia_klasy_B_NM = []

for i in range(LPTrening):
    klasa_probki = dane.iloc[i]["klasa"]
    if klasa_probki is "A":
        for j in range(LiczbaCech): 
            probki_klasy_A_NM.append(dane.iloc[i][j])
    if klasa_probki is "B":
        for j in range(LiczbaCech):
            probki_klasy_B_NM.append(dane.iloc[i][j])

for i in range(LiczbaCech):
    #pobieramy kolejne wartosci z listy co Liczbę Cech
    for j in range(int(len(probki_klasy_A_NM)/LiczbaCech)):
        probki_klasy_A_NM_c.append(probki_klasy_A_NM[i + LiczbaCech * j])
    srednia_klasy_A_NM.append(Srednia(probki_klasy_A_NM_c))
    probki_klasy_A_NM_c = []
    
for i in range(LiczbaCech):
    for j in range(int(len(probki_klasy_B_NM)/LiczbaCech)):
        probki_klasy_B_NM_c.append(probki_klasy_B_NM[i + LiczbaCech * j])
        if(len(probki_klasy_B_NM_c) is not 0):
            srednia_klasy_B_NM.append(Srednia(probki_klasy_B_NM_c))
    probki_klasy_B_NM_c = []

print("srednia_klasy_A_NM = ",srednia_klasy_A_NM)
print("srednia_klasy_B_NM = ",srednia_klasy_B_NM)

NM_tak = 0
NM_nie = 0

for kolejny in range(LPTest):
    aktualny = LPTrening + kolejny
    szukany_x = dane.iloc[aktualny]
    DsAx = math.sqrt(math.pow(srednia_klasy_A_NM[0]-szukany_x[0],2) + math.pow(srednia_klasy_A_NM[1]-szukany_x[1],2) + math.pow(srednia_klasy_A_NM[2]-szukany_x[2],2))
    DsBx = math.sqrt(math.pow(srednia_klasy_B_NM[0]-szukany_x[0],2) + math.pow(srednia_klasy_B_NM[1]-szukany_x[1],2) + math.pow(srednia_klasy_B_NM[2]-szukany_x[2],2))

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

#Metoda kNM k najbliższych srednich
global probki_klasy_A_kNM
probki_klasy_A_kNM = pd.DataFrame(columns=["c1", "c2", "c3"])

for i in range(int(len(dane))):
    klasa_probki = dane.iloc[i]["klasa"]
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
    
    
def main():
    global probki_klasy_A_kNM
    global podzielone_probki    
    global wartosci_srednie
    
    print(probki_klasy_A_kNM)
    kolejny_df = oblicz_kNM(probki_klasy_A_kNM)
    efekt = porownanie_dopasowania(probki_klasy_A_kNM, kolejny_df)
    print(efekt)
    while True:
        jeszcze_kolejny_df = oblicz_kNM(kolejny_df)
        efekt = porownanie_dopasowania(kolejny_df, jeszcze_kolejny_df)
        print(efekt)
        if efekt is True:
            break
        jeszcze_2_kolejny_df = oblicz_kNM(jeszcze_kolejny_df)
        efekt = porownanie_dopasowania(jeszcze_kolejny_df, jeszcze_2_kolejny_df)
        print(efekt)
        if efekt is True:
            break
        jeszcze_3_kolejny_df = oblicz_kNM(jeszcze_2_kolejny_df)
        efekt = porownanie_dopasowania(jeszcze_2_kolejny_df, jeszcze_3_kolejny_df)
        print(efekt)
        if efekt is True:
            break
        

        