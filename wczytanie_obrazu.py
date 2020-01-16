# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 16:57:03 2020

@author: Szymon
Wczytanie obrazu - OpenCV
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

from skimage.io import imread_collection

from tkinter import filedialog, Label
import tkinter as tk

okno = tk.Tk()
okno.title("SMPD lab Szymon Woyda 227458")
okno.geometry('640x480')
etykieta=Label(okno, text=" Wczytaj obraz: ", font=("Arial",16))
etykieta.grid(column = 0, row = 0)

def wczytaj():
    global img
    sciezkaDoPliku = filedialog.askopenfilename()
    img = cv2.imread(sciezkaDoPliku,0)
    
def wczytaj_all():
    global col
    col_dir = 'img_resize/*.jpg'
    col = imread_collection(col_dir)
    

przycisk_wczytaj = tk.Button(text=" Wczytaj ", 
                             command=wczytaj, bg='green', fg='white', font=('helvetica', 12, 'bold'))
przycisk_wczytaj.grid(column=2, row=0)

przycisk_wczytaj_all = tk.Button(text=" Wczytaj wszystkie ", 
                             command=wczytaj_all, bg='green', fg='white', font=('helvetica', 12, 'bold'))
przycisk_wczytaj_all.grid(column=2, row=1)

okno.mainloop()
#https://likegeeks.com/python-gui-examples-tkinter-tutorial/

edges = cv2.Canny(img,100,200)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()

unique, counts = np.unique(edges, return_counts=True)
print(dict(zip(unique, counts)))

reka_1 = col[0]
reka_1 = cv2.cvtColor(reka_1, cv2.COLOR_BGR2GRAY)
reka_1 = cv2.Canny(reka_1,100,200)

np.savetxt("foo.csv", reka_1, delimiter=",")

cv2.imshow('image',reka_1)
cv2.waitKey(0)
cv2.destroyAllWindows()

