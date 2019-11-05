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

print("Szukany x dla metody NN należy do klasy: " + df.iloc[index_probka_NN]["klasa"])
print("Według metody NN x należy do klasy: " + df.iloc[min_index_NN]["klasa"])

odpowiedz_algorytmu_NN = df.iloc[min_index_NN]["klasa"]

if odpowiedz_algorytmu_NN is df.iloc[index_probka_NN]["klasa"]:
        print("\n Algorytm NN ma racje")
else:
     print("\n Algorytm NN się pomylił")
     
def printtext():
    global e
    global wartosc_k
    wartosc_k = e.get()
    wartosc_k = int(wartosc_k)
    print(wartosc_k,'\n')

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

for i in range(0,4):
    slownik_kNN['A',i]=lista_kNN[i]
  
for i in range(4,8):
    slownik_kNN['B',i]=lista_kNN[i]

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

#Index punktu dla którego odległosc jest najniższą wartoscią
min_index_NN=(listaNN).index(min(listaNN))

print("Szukany x dla metody kNN należy do klasy: " + df.iloc[index_probka_kNN]["klasa"])

print("Dla k = ", wartosc_k)
if odpowiedz_algorytmu_kNN is df.iloc[index_probka_kNN]["klasa"]:
        print(" Algorytm kNN ma racje")
else:
     print(" Algorytm kNN się pomylił")