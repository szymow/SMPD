# -*- coding: utf-8 -*-
"""
Create a GUI to import a CSV file into Python
"""

import tkinter as tk
from tkinter import filedialog
import pandas as pd
root=tk.Tk()

canvas1=tk.Canvas(root, width=300, height=300, bg='lightsteelblue2', relief='raised')
canvas1.pack()

def getCSV():
    global df
    
    import_file_path = filedialog.askopenfilename()
    df=pd.read_csv(import_file_path)
    print(df)
    
browseButton_CSV = tk.Button(text=" Import CSV File ", command=getCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 150, window=browseButton_CSV)

root.mainloop()

# Index -1 oznacza ostatni punkt w naszym przypadku X
import math

liczba_probek_treningowych = 8 #liczą od zera jest 0, ale taki jest wymóg funkcji range
index_probka_NN = 8
listaNN=[]

for i in range(liczba_probek_treningowych):
    listaNN.append(math.sqrt(math.pow((df.iloc[i]["c1"]-df.iloc[index_probka_NN]["c1"]),2) + math.pow((df.iloc[i]["c2"]-df.iloc[index_probka_NN]["c2"]),2)+math.pow((df.iloc[i]["c3"]-df.iloc[index_probka_NN]["c3"]),2)))

#Index punktu dla którego odległosc jest najniższą wartoscią
min_index_NN=(listaNN).index(min(listaNN))

print("x należy do klasy: " + df.iloc[index_probka_NN]["klasa"])
print("według metody NN x należy do klasy: " + df.iloc[min_index_NN]["klasa"])

odpowiedz_algorytmu_NN = df.iloc[min_index_NN]["klasa"]

if odpowiedz_algorytmu_NN is df.iloc[index_probka_NN]["klasa"]:
        print("\n Algorytm ma racje")
else:
     print("\n Algorytm się pomylił")
     
def printtext():
    global e
    string = e.get() 
    print(string)   

root2 = tk.Tk()

root2.title("kNN - k najbliższych sąsiadów")
canvas2=tk.Canvas(root2, width=300, height=300, bg='lightsteelblue2', relief='raised')
canvas2.pack()

e = tk.Entry(root2)
e.pack()
e.focus_set()

browseButton_kNN = tk.Button(text=" Zatwierdź ", command=printtext, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas2.create_window(150, 150, window=browseButton_CSV)
root.mainloop()

#kNN k najbliższych sąsiadów

index_probka_kNN = 9
lista_kNN=[]

for i in range(8):
    lista_kNN.append(math.sqrt(math.pow((df.iloc[i]["c1"]-df.iloc[index_probka_kNN]["c1"]),2) + math.pow((df.iloc[i]["c2"]-df.iloc[index_probka_kNN]["c2"]),2)+math.pow((df.iloc[i]["c3"]-df.iloc[index_probka_kNN]["c3"]),2)))

#Index punktu dla którego odległosc jest najniższą wartoscią
slownik_kNN={}

slownik_kNN['A0']=lista_kNN[0]
slownik_kNN['A1']=lista_kNN[1]
slownik_kNN['A2']=lista_kNN[2]
slownik_kNN['A3']=lista_kNN[3]
slownik_kNN['B0']=lista_kNN[4]
slownik_kNN['B1']=lista_kNN[5]
slownik_kNN['B2']=lista_kNN[6]
slownik_kNN['B3']=lista_kNN[7]

print(slownik_kNN)

posortowany_slownik_kNN={}

for key, value in sorted(slownik_kNN.items(), key=lambda item: item[1]):
    posortowany_slownik_kNN[key]=value

print(posortowany_slownik_kNN)

print("x należy do klasy: " + df.iloc[index_probka_kNN]["klasa"])
print("według metody NN x należy do klasy: " + df.iloc[min_index_NN]["klasa"])

odpowiedz_algorytmu_NN = df.iloc[min_index_NN]["klasa"]
