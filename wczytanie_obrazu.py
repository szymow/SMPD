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

import csv

okno = tk.Tk()
okno.title("SMPD lab Szymon Woyda 227458")
okno.geometry('640x480')
etykieta=Label(okno, text=" Wczytaj obraz: ", font=("Arial",16))
etykieta.grid(column = 0, row = 0)



def wczytaj():
    global img
    global jedno
    jedno = True
    sciezkaDoPliku = filedialog.askopenfilename()
    img = cv2.imread(sciezkaDoPliku,0)
    
def wczytaj_all():
    global col
    global jedno
    jedno = False
    col_dir = 'img_resize_rename/*.jpg'
    col = imread_collection(col_dir)
    

przycisk_wczytaj = tk.Button(text=" Wczytaj ", 
                             command=wczytaj, bg='green', fg='white', font=('helvetica', 12, 'bold'))
przycisk_wczytaj.grid(column=2, row=0)

przycisk_wczytaj_all = tk.Button(text=" Wczytaj wszystkie ", 
                             command=wczytaj_all, bg='green', fg='white', font=('helvetica', 12, 'bold'))
przycisk_wczytaj_all.grid(column=2, row=1)

okno.mainloop()
#https://likegeeks.com/python-gui-examples-tkinter-tutorial/

if jedno:
    edges = cv2.Canny(img,100,200)

    plt.subplot(121),plt.imshow(img,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    plt.show()

    unique, counts = np.unique(edges, return_counts=True)
    print(dict(zip(unique, counts)))
else:
    export_csv = []
    i = 0
    j = 30
    for reka in col:
        i = i + 1
        j = j + 1
        cv2.imshow(str(i), reka)
        reka_x = cv2.cvtColor(reka, cv2.COLOR_BGR2GRAY)
        reka_x = cv2.Canny(reka,100,200)
        
        orb = cv2.ORB_create(nfeatures=64)
        keypoints, descriptors = orb.detectAndCompute(reka_x, None)
        
        reka_x = cv2.drawKeypoints(reka_x, keypoints, None)
        
        descriptors_mean = descriptors.mean(axis=1)
        cv2.imshow(str(j), reka_x)
        
        export_csv.append(descriptors_mean)
        
    b = open("reka.csv", "w")
    a = csv.writer(b)
    a.writerows(export_csv)
    b.close()

    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

