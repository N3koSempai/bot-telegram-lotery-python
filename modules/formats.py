# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 00:02:24 2021

@author: n3ko
"""


def add_simbol(data):
    lista = []
    newdata = []
    for i in data:
        if type(i[1]) == float:
            i[1] = i[1].replace( ".", "x")
            m = i[2]
            i[2] = (f"${m}",format (m))
            lista.append(i)
        elif type(i) == int:
            i[1] = int(i[1])
            m = i[2]
            i[2] = (f"${m}",format (m))
            lista.append(i)
        else:
            lista.append(i)
        newdata.append(lista)
            
    return newdata        
        
    
    