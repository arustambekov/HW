#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 08:22:04 2018

@author: artemrustambekov
"""
import numpy as np

class Means:
    
    def __init__(self, x,y):
        self.arrayX = x
        self.arrayY = y
        self.values = np.array(list(set(self.arrayX))) #находим множество элементов и записываем в список
        self.means = np.array([self.mean(i) for i in self.values])
        self.stderrs = np.array([self.stderr(i) for i in self.values])
        
    def mean(self,number):  # находит среднии значения
        sumY = 0
        for i in range(len(self.arrayX)):
           if number == self.arrayX[i]:
               sumY += self.arrayY[i]
        nX = list(self.arrayX).count(number)
        return sumY/nX
    
    def stderr(self,number): #находим стандартную ошибку среднего
        sumY=0
        for i in range(len(self.arrayX)):
            if number == self.arrayX[i]:
                sumY += (self.arrayY[i]-self.mean(number))**2
        nX = list(self.arrayX).count(number)
        der = (1/(nX**0.5))*((sumY/(nX-1))**0.5)
        return der