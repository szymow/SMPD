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

root=tk.Tk()
root.title("SMPD lab Szymon Woyda 227458")
root.geometry('640x480')
lbl=Label(root, text="\t Metody klasyfikacji: NN i kNN \t", font=("Arial",16))
lbl.grid(column=0,row=0)

def getCSV():
    global df
    
    import_file_path = filedialog.askopenfilename()
    df=pd.read_csv(import_file_path)
    print(df)
    
def printtext():
    global e
    global wartosc_k
    wartosc_k = combo.get()
    wartosc_k = int(wartosc_k)
    print(wartosc_k,'\n')
    
browseButton_CSV = tk.Button(text=" Import CSV File ", command=getCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
browseButton_CSV.grid(column=1, row=0)

lbl2=Label(root, text=" Wybierz wartość k dla metody kNN: \t", font=("Arial",12))
lbl2.grid(column=0,row=1)

combo = Combobox(root)
combo['values']=(1,2,3,4,5,6,7,8)
combo.current(2)
combo.grid(column=1,row=1)

browseButton_kNN = tk.Button(text=" Zatwierdź ", command=printtext, bg='green', fg='white', font=('helvetica', 12, 'bold'))
browseButton_kNN.grid(column=2, row=1)

root.mainloop()

#Dane modyfikowane przez użytkownika
liczba_probek_treningowych = 8

liczba_probek_testowych = 2


listaNN=[[],[],[],[],[]]

for j in range(liczba_probek_testowych):
    for i in range(liczba_probek_treningowych):
        listaNN[j].append(math.sqrt(math.pow((df.iloc[i]["c1"]-df.iloc[j+liczba_probek_treningowych]["c1"]),2) + math.pow((df.iloc[i]["c2"]-df.iloc[j+liczba_probek_treningowych]["c2"]),2)+math.pow((df.iloc[i]["c3"]-df.iloc[j+liczba_probek_treningowych]["c3"]),2)))

#Index punktu dla którego odległosc jest najniższą wartoscią
min_index_NN=[]

for i in range(liczba_probek_testowych):
    min_index_NN.append((listaNN[i]).index(min(listaNN[i])))
    print("Szukany x dla metody NN należy do klasy: " + df.iloc[liczba_probek_treningowych + i]["klasa"])
    print("Według metody NN x należy do klasy: " + df.iloc[min_index_NN[i]]["klasa"])

    if df.iloc[min_index_NN[i]]["klasa"] is df.iloc[liczba_probek_treningowych + i]["klasa"]:
        print("Algorytm NN ma racje \n")
    else:
        print("Algorytm NN się pomylił \n")


#kNN k najbliższych sąsiadów

lista_kNN=[[],[]]

for j in range(liczba_probek_testowych):
    for i in range(liczba_probek_treningowych):
        lista_kNN[j].append(math.sqrt(math.pow((df.iloc[i]["c1"]-df.iloc[j+liczba_probek_treningowych]["c1"]),2) + math.pow((df.iloc[i]["c2"]-df.iloc[j+liczba_probek_treningowych]["c2"]),2)+math.pow((df.iloc[i]["c3"]-df.iloc[j+liczba_probek_treningowych]["c3"]),2)))

#Index punktu dla którego odległosc jest najniższą wartoscią
slownik_kNN={}

for j in range(liczba_probek_testowych):
    for i in range(liczba_probek_treningowych):
        klasa_probki = df.iloc[i]["klasa"]
        slownik_kNN[klasa_probki,i]=lista_kNN[j][i]

#print(slownik_kNN)
posortowany_slownik_kNN={}

for key, value in sorted(slownik_kNN.items(), key=lambda item: item[1]):
    posortowany_slownik_kNN[key]=value

#print(posortowany_slownik_kNN)
klucze_kNN = [k for k, v in posortowany_slownik_kNN.items()]

klucze_kNN_sum=list(sum(klucze_kNN[:wartosc_k],()))
#print(klucze_kNN_sum)

klucze_kNN_join=''.join(str(klucze_kNN_sum_e) for klucze_kNN_sum_e in klucze_kNN_sum)

if klucze_kNN_join.count('A') > klucze_kNN_join.count('B'):
    print("Według metody kNN x należy do klasy: A")
    odpowiedz_algorytmu_kNN = 'A'
else:
    print("Według metody kNN x należy do klasy: B")
    odpowiedz_algorytmu_kNN = 'B'


for i in range(liczba_probek_testowych):
    print("Szukany x dla metody kNN należy do klasy: " + df.iloc[liczba_probek_treningowych + i]["klasa"])
    print("Dla k = ", wartosc_k)
    if odpowiedz_algorytmu_kNN is df.iloc[liczba_probek_treningowych + i]["klasa"]:
        print("Algorytm kNN ma racje \n")
    else:
        print("Algorytm kNN się pomylił \n")
     
#https://likegeeks.com/python-gui-examples-tkinter-tutorial/