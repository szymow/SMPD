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

dA1x=math.sqrt(math.pow((df.iloc[0]["c1"]-df.iloc[-1]["c1"]),2) + math.pow((df.iloc[0]["c2"]-df.iloc[-1]["c2"]),2)+math.pow((df.iloc[0]["c3"]-df.iloc[-1]["c3"]),2))
dA2x=math.sqrt(math.pow((df.iloc[1]["c1"]-df.iloc[-1]["c1"]),2) + math.pow((df.iloc[1]["c2"]-df.iloc[-1]["c2"]),2)+math.pow((df.iloc[1]["c3"]-df.iloc[-1]["c3"]),2))
dA3x=math.sqrt(math.pow((df.iloc[2]["c1"]-df.iloc[-1]["c1"]),2) + math.pow((df.iloc[2]["c2"]-df.iloc[-1]["c2"]),2)+math.pow((df.iloc[2]["c3"]-df.iloc[-1]["c3"]),2))
dA4x=math.sqrt(math.pow((df.iloc[3]["c1"]-df.iloc[-1]["c1"]),2) + math.pow((df.iloc[3]["c2"]-df.iloc[-1]["c2"]),2)+math.pow((df.iloc[3]["c3"]-df.iloc[-1]["c3"]),2))
dB1x=math.sqrt(math.pow((df.iloc[4]["c1"]-df.iloc[-1]["c1"]),2) + math.pow((df.iloc[4]["c2"]-df.iloc[-1]["c2"]),2)+math.pow((df.iloc[4]["c3"]-df.iloc[-1]["c3"]),2))
dB2x=math.sqrt(math.pow((df.iloc[5]["c1"]-df.iloc[-1]["c1"]),2) + math.pow((df.iloc[5]["c2"]-df.iloc[-1]["c2"]),2)+math.pow((df.iloc[5]["c3"]-df.iloc[-1]["c3"]),2))
dB3x=math.sqrt(math.pow((df.iloc[6]["c1"]-df.iloc[-1]["c1"]),2) + math.pow((df.iloc[6]["c2"]-df.iloc[-1]["c2"]),2)+math.pow((df.iloc[6]["c3"]-df.iloc[-1]["c3"]),2))
dB4x=math.sqrt(math.pow((df.iloc[7]["c1"]-df.iloc[-1]["c1"]),2) + math.pow((df.iloc[7]["c2"]-df.iloc[-1]["c2"]),2)+math.pow((df.iloc[7]["c3"]-df.iloc[-1]["c3"]),2))

#Index punktu, który przyjmuje najniższą wartosc
min_index=(dA1x,dA2x,dA3x,dA4x,dB1x,dB2x,dB3x,dB4x).index(min((dA1x,dA2x,dA3x,dA4x,dB1x,dB2x,dB3x,dB4x)))

print("x należy do klasy: " + df.iloc[-1]["klasa"])
print("według metody NN x należy do klasy: " + df.iloc[min_index]["klasa"])

odpowiedz_algorytmu = df.iloc[min_index]["klasa"]

if odpowiedz_algorytmu is df.iloc[-1]["klasa"]:
        print("Algorytm ma racje")
else:
     print("Algorytm się pomylił")