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
lbl=Label(root, text=" Metody klasyfikacji: NN i kNN", font=("Arial",16))
lbl.grid(column=0,row=0)

def getCSV():
    global df
    import_file_path = filedialog.askopenfilename()
    df=pd.read_csv(import_file_path)
    print(df)

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
    
browseButton_CSV = tk.Button(text=" Import CSV File ", 
                             command=getCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
browseButton_CSV.grid(column=1, row=0)

lbl3=Label(root, text=" Liczba próbek treningowych: ", font=("Arial",12))
lbl3.grid(column=0,row=1)

combo2 = Combobox(root)
combo2['values']=(1,2,3,4,5,6,7,8,9,10,11,12,13)
combo2.current(7)
combo2.grid(column=1,row=1)

lbl3=Label(root, text=" Liczba próbek testowych: ", font=("Arial",12))
lbl3.grid(column=0,row=2)

combo3 = Combobox(root)
combo3['values']=(1,2,3,4,5)
combo3.current(1)
combo3.grid(column=1,row=2)

browseButton_input_trening = tk.Button(text=" Zatwierdź ", command=input_trening, bg='green', fg='white', font=('helvetica', 12, 'bold'))
browseButton_input_trening.grid(column=2, row=1)
browseButton_input_test = tk.Button(text=" Zatwierdź ", command=input_test, bg='green', fg='white', font=('helvetica', 12, 'bold'))
browseButton_input_test.grid(column=2, row=2)

lbl2=Label(root, text=" Wartość k dla metody kNN: \t", font=("Arial",12))
lbl2.grid(column=0,row=3)

combo = Combobox(root)
combo['values']=(1,2,3,4,5,6,7,8)
combo.current(2)
combo.grid(column=1,row=3)

browseButton_kNN = tk.Button(text=" Zatwierdź ", command=input_k, bg='green', fg='white', font=('helvetica', 12, 'bold'))
browseButton_kNN.grid(column=2, row=3)

root.mainloop()

listaNN=[[],[],[],[],[]]

for j in range(liczba_probek_testowych):
    for i in range(liczba_probek_treningowych):
        listaNN[j].append(math.sqrt(math.pow((df.iloc[i]["c1"]-df.iloc[j+liczba_probek_treningowych]["c1"]),2) + math.pow((df.iloc[i]["c2"]-df.iloc[j+liczba_probek_treningowych]["c2"]),2)+math.pow((df.iloc[i]["c3"]-df.iloc[j+liczba_probek_treningowych]["c3"]),2)))

min_index_NN=[]

for i in range(liczba_probek_testowych):
    min_index_NN.append((listaNN[i]).index(min(listaNN[i])))
    print(df.iloc[liczba_probek_treningowych + i])
    print("Szukany x dla metody NN należy do klasy: " + df.iloc[liczba_probek_treningowych + i]["klasa"])
    print("Według metody NN x należy do klasy: " + df.iloc[min_index_NN[i]]["klasa"])

    if df.iloc[min_index_NN[i]]["klasa"] is df.iloc[liczba_probek_treningowych + i]["klasa"]:
        print("Algorytm NN ma racje \n")
    else:
        print("Algorytm NN się pomylił \n")


#kNN k najbliższych sąsiadów

lista_kNN=[[],[],[],[],[]]

for j in range(liczba_probek_testowych):
    for i in range(liczba_probek_treningowych):
        lista_kNN[j].append(math.sqrt(math.pow((df.iloc[i]["c1"]-df.iloc[j+liczba_probek_treningowych]["c1"]),2) 
        + math.pow((df.iloc[i]["c2"]-df.iloc[j+liczba_probek_treningowych]["c2"]),2)
        + math.pow((df.iloc[i]["c3"]-df.iloc[j+liczba_probek_treningowych]["c3"]),2)))

odpowiedz_algorytmu_kNN = []

for odp in range(liczba_probek_testowych):

    slownik_kNN={}

    for j in range(liczba_probek_testowych):
        for i in range(liczba_probek_treningowych):
            klasa_probki = df.iloc[i]["klasa"]
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

for i in range(liczba_probek_testowych):
    print("Szukany x dla metody kNN należy do klasy: " + df.iloc[liczba_probek_treningowych + i]["klasa"])
    print("Według metody kNN x należy do klasy: " + odpowiedz_algorytmu_kNN[i])
    print("Dla k = ", wartosc_k)
    if odpowiedz_algorytmu_kNN[i] is df.iloc[liczba_probek_treningowych + i]["klasa"]:
        print("Algorytm kNN ma racje \n")
    else:
        print("Algorytm kNN się pomylił \n")
     
#https://likegeeks.com/python-gui-examples-tkinter-tutorial/