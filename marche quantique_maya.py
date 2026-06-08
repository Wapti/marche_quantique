#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 15:54:49 2026

@author: maya
"""


import matplotlib.pyplot as plt
import numpy as np


#fct = [{a,pos,vect},...)   vect = [0,1] ou [1,0]
#exemples : fonction = [{"a" : 1/np.sqrt(2),  "pos" : 1, "vect" : [1,0]} , {} , ...]


    
def hadamar(f):
    n_fct=[]
    for i in range(len(f)):
        d = f[i]
        if d["vect"][0] == 1 : # si le vecteur (dans le dictionnaire qui est dans la fonction d'onde) est pile
        
           n_fct.append({"a" : d["a"]*1/np.sqrt(2) , "pos" : d["pos"] , "vect" : [1,0] })   
           n_fct.append({"a" : d["a"]*1/np.sqrt(2) , "pos" : d["pos"] , "vect" : [0,1] })
           
        else :
            
            n_fct.append({"a" : d["a"]*1/np.sqrt(2) , "pos" : d["pos"] , "vect" : [1,0] })   
            n_fct.append({"a" : d["a"]*(-1)/np.sqrt(2) , "pos" : d["pos"] , "vect" : [0,1] })
            
    return n_fct



    
def shift(f):
    nv_fct = []
    for i in range(len(f)) :
        d = f[i]
        if d["vect"][0] == 1 :
            nv_fct.append({"a" : d["a"] , "pos" : d["pos"]+1 , "vect" : [1,0]})
        else :
            nv_fct.append({"a" : d["a"] , "pos" : d["pos"]-1 , "vect" : [0,1]})
    return nv_fct    
        


def somme_vect_etat(f):  
    
    somme = {}
    
    for d in f:
        
        ref = (d["pos"], tuple(d["vect"]))
        
        if ref in somme:
            somme[ref] += d["a"]
        else:
            somme[ref] = d["a"]
            
    
    nv_fc = []
    for (pos, vect_tuple), a in somme.items():
        if a != 0: # On ignore les probabilités nulles
            nv_fc.append({"a": a, "pos": pos, "vect": list(vect_tuple)})
            
    return nv_fc
    
def nvlle_fct_onde(f):
    n_fct=hadamar(f)
    n_fct=shift(n_fct)
    n_fct=somme_vect_etat(n_fct)
    return n_fct        
        
def marche_quantique(f,N):
    fct_onde_finale = f
    for i in range(N):
        fct_onde_finale = nvlle_fct_onde(fct_onde_finale)
    return fct_onde_finale
        
def calculer_probabilites(fct_onde_finale, N):
    
    probabilites = [0.0] * (2 * N + 1)
    positions = list(range(-N, N + 1)) 
    
    for i in range(len(fct_onde_finale)):
        d=fct_onde_finale[i]
        pos = d["pos"]
        a = d["a"]
        prob_etat = abs(a)**2
        
        probabilites[pos + N] += prob_etat
        
    return positions, probabilites



#VISUALISATION 

fct_initiale = [{"a": 1/np.sqrt(2), "pos": 0, "vect": [0, 1]},{"a": 1j/np.sqrt(2), "pos": 0, "vect": [1, 0]} ]


NB_ETAPES = 500
resultat_marche = marche_quantique(fct_initiale, NB_ETAPES)


positions, probabilites = calculer_probabilites(resultat_marche, NB_ETAPES)


plt.bar(positions, probabilites, color='blue', alpha=0.9)


plt.title(f"Distribution de probabilité - Marche Quantique ({NB_ETAPES} étapes)", fontsize=14)
plt.xlabel("Position", fontsize=12)
plt.ylabel("Probabilité", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)



plt.show()
  
    
        
       
    
    

    