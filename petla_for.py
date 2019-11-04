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

lista=[]

#Odejmujemy 1 ponieważ chcemy odrzucić ostatni wpis (punkt), który jest naszą szukaną
for i in range(len(df.index)-1):
    lista.append(math.sqrt(math.pow((df.iloc[i]["c1"]-df.iloc[-1]["c1"]),2) + math.pow((df.iloc[i]["c2"]-df.iloc[-1]["c2"]),2)+math.pow((df.iloc[i]["c3"]-df.iloc[-1]["c3"]),2)))

#Index punktu dla którego odległosc jest najniższą wartoscią
min_index=(lista).index(min(lista))

print("x należy do klasy: " + df.iloc[-1]["klasa"])
print("według metody NN x należy do klasy: " + df.iloc[min_index]["klasa"])

odpowiedz_algorytmu = df.iloc[min_index]["klasa"]

if odpowiedz_algorytmu is df.iloc[-1]["klasa"]:
        print("\n Algorytm ma racje")
else:
     print("\n Algorytm się pomylił")