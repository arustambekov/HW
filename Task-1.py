#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 09:08:11 2018

@author: artemrustambekov
"""
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns; sns.set(color_codes=True)
from scipy.stats import norm
from scipy.stats import chi2
#плотность стандартного нормального распределения
fig, ax = plt.subplots(1, 1,figsize=(8, 4)) # drow empty sheet
x = np.linspace(norm.ppf(0.0001),norm.ppf(0.9999),10000)
plt.xlim([-3.5, 3.5])
ax.plot(x,norm.pdf(x)) #pdf-probability density function
ax.set_ylabel('Density'+' '+'$f(x)$')
ax.set_xlabel('$x$')
ax.fill_between(x, 0, norm.pdf(x), facecolor='gray', alpha=0.3)

perc1 = np.percentile(x, 28)#левая величина квантиля 
perc2 = np.percentile(x, 72)#правая величина квантиля 
#print(perc1,perc2)

ax.fill_between(x,norm.pdf(x), where=x < perc1,facecolor='red', alpha=0.6)
ax.fill_between(x,norm.pdf(x), where=x > perc2,facecolor='red', alpha=0.6)
#plt.plot([perc1,perc1], [0, norm.pdf(perc1)], color='blue', linewidth=2, linestyle="--")
#plt.plot([perc2,perc2], [0, norm.pdf(perc2)], color='blue', linewidth=2, linestyle="--")
#plt.scatter([perc1, ], [norm.pdf(perc1), ], 30, color='blue')
#plt.scatter([perc2, ], [norm.pdf(perc2), ], 30, color='blue')

ax.text(perc1, -0.02, f"$X_{{0.28}} = {perc1:0.2f}$", fontsize=12)
ax.text(perc2, -0.02, f"$X_{{0.72}} = {perc2:0.2f}$", fontsize=12)
plt.savefig('Density.svg')
#%% стандартное нормальное распределение 
fig, ax2 = plt.subplots(1, 1,figsize=(8, 4))
df = 3
x2 = np.linspace(chi2.ppf(0.0001, df),chi2.ppf(0.9999, df), 10000)
#plt.xlim([-3.5, 3.5])
ax2.plot(x2, chi2.pdf(x2,df))
ax2.set_ylabel('Squared continuous random variable.'+' '+'$f(x)$')
ax2.set_xlabel('$x$')
ax2.fill_between(x2, 0, chi2.pdf(x2,df), facecolor='gray', alpha=0.3)

perc12 = np.percentile(x2, 5)
perc22 = np.percentile(x2, 95)
#print(perc1,perc2)

ax2.fill_between(x2,chi2.pdf(x2,df), where=x2 < perc12,facecolor='red', alpha=0.6)
ax2.fill_between(x2,chi2.pdf(x2,df), where=x2 > perc22,facecolor='red', alpha=0.6)
plt.plot([perc12,perc12], [0, chi2.pdf(perc12,df)], color='blue', 
        linewidth=2, linestyle="--")
plt.plot([perc22,perc22], [0, chi2.pdf(perc22,df)], color='blue',
        linewidth=2, linestyle="--")
plt.scatter([perc12, ], [chi2.pdf(perc12,df), ], 30, color='blue')
plt.scatter([perc22, ], [chi2.pdf(perc22,df), ], 30, color='blue')

ax2.text(perc12, -0.02, f"$X_{{0.05}} = {perc12:0.2f}$", fontsize=12)
ax2.text(perc22, -0.02, f"$X_{{0.95}} = {perc22:0.2f}$", fontsize=12)
plt.savefig('Squared_variable.svg')
#%%