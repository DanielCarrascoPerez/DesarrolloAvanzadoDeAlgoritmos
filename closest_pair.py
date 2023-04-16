#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import json
import math
import time
import sys

def read_stars(file):
    with open(file) as inputfile:
       return json.load(inputfile)

def dist2(s1,s2):
    return math.sqrt((s2[0]-s1[0])**2 + (s2[1]-s1[1])**2 + (s2[2]-s1[2])**2)

def brute_force(P):
    b1, b2, min_distance = (-1, -1, math.inf)

    for i1,s1 in enumerate(P):
        for i2,s2 in enumerate(P):
            if (i1==i2):
                continue
            d = dist2(s1,s2)
            if (d < min_distance):
                (b1, b2, min_distance) = (i1, i2, d)  

    return min_distance, P[b1], P[b2]


def divide_and_conquer(P):
    X = sorted(P, key=lambda p : p[0])
    Y = sorted(P, key=lambda p : p[1])  
    return closest_pair(X,Y)

def closest_pair(X,Y):
    #Si el tamaño es 3, se usa la fuerza bruta
    if len(X) <= 3:
        return brute_force(X)

    #Calculamos la media de X, dividimos la lista en dos y creamos las listas vacias para dividir el eje Y también
    middle = len(X) // 2
    Qx = X[:middle]
    Rx = X[middle:]
    median = X[middle]
    Qy,Ry = [], []

    #Comprobamos en que lado está cada punto de Y y lo metemos en la lista correspondiente
    for point in Y:
        if point[0] < int(median[0]):
            Qy.append(point)
        else:
            Ry.append(point)

    #Dividimos recursivamente ambas listas hasta llegar a tener sólo 2-3 puntos en la lista
    min_distance_left = closest_pair(Qx,Qy)
    min_distance_right = closest_pair(Rx,Ry)
    #Calculamos la distancia minima entre los puntos de ambos lados
    min_distance = min(min_distance_left, min_distance_right)
    #Guardamos la coordenada X del punto central para tenerlo como eje centrar y comprobar aquellos puntos que están en ambos lados
    separator = Qx[-1][0]
    Sy = []

    #Guardamos los puntos del area central
    for y in Y:
        if separator - min_distance[0] < y[0] < separator + min_distance[0]:
            Sy.append(y)
    
    #Calculamos la distancia minima entre los puntos del area central
    for i in range(len(Sy) - 1):
        for j in range(i+1, min(i + 7, len(Sy))):
            P = Sy[i]
            Q = Sy[j]
            dist = dist2(P,Q)
            #Si encontramos un punto con menor distancia, actualizamos min_distance
            if dist < min_distance[0]:
                min_distance = (dist, P,Q)

    return min_distance

if (len(sys.argv)<2):
    print("Please, indicate the file with points as argument")
    sys.exit()

P = read_stars(sys.argv[1]) 
start = time.time()
brute_sol = brute_force(P)
end = time.time()
print("Brute force time: ", end - start)
start = time.time()
dc_sol = divide_and_conquer(P) 
end = time.time()
print("Divide and conquer time: ", end - start)