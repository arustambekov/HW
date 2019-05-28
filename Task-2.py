#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 22:38:11 2018

@author: artemrustambekov
"""

import numpy as np
import pandas as pd
import zipfile
import matplotlib.pylab as plt
import seaborn as sns; sns.set(color_codes=True)
import calendar
import datetime
from mean import Means
#распакуем файл из зип и запишем выбранные нами столбцы в ms-Москву, spb-Питер
#сразу делая индексом Дату index_col='DATE'
zf = zipfile.ZipFile('weather.zip') 
with zf.open('moscow.csv') as f:
    ms = pd.read_csv(f,index_col='DATE', parse_dates=True,
                     usecols=['DATE','PRCP', 'SNWD','TAVG','TMAX','TMIN'])
with zf.open('spb.csv') as f:
    spb = pd.read_csv(f, index_col='DATE', parse_dates=True,
                       usecols = ['DATE','PRCP', 'SNWD','TAVG','TMAX','TMIN'])
#%%
#выберем дату с декабря 2012 по январь 2014, удалим все пропущенные наблюдения
#print(spb)
import matplotlib.dates as mdates
dfm = ms['2013-1':'2013-12']
dfm = dfm.dropna(subset=['TAVG','PRCP'], axis = 0)
dfs = spb['2013-1':'2013-12']
dfs = dfs.dropna(subset=['TAVG','PRCP'], axis = 0)
#print(dfm)
#распечатаем график Средней температуры по дням это колонка 'TAVG'
fig, axm = plt.subplots(1, 1,figsize = (8, 4)) # drow empty sheet
axm.plot(dfm['TAVG'],label = "Moscow")
axm.plot(dfs['TAVG'],label = "SPb")
axm.xaxis.set_major_locator(mdates.MonthLocator())
axm.xaxis.set_major_formatter(mdates.DateFormatter("%B"))
#plt.xticks(rotation='vertical')
fig.autofmt_xdate()
axm.legend(loc = 'upper left')
plt.suptitle('Average temperature in celsius')
plt.savefig('Average_temperature .svg')
# распечатаем графики для кол-ва осадков за 2013 год, колонка PRCP
fig, axs = plt.subplots(1, 1,figsize = (8, 4)) # drow empty sheet
axs.xaxis.set_major_locator(mdates.MonthLocator())
axs.xaxis.set_major_formatter(mdates.DateFormatter("%B"))
axs.plot(dfm['PRCP'],label = "Moscow")
axs.plot(dfs['PRCP'],label = "SPb")
#plt.xticks(rotation='vertical')
fig.autofmt_xdate()
axs.legend(loc = 'upper left')
plt.suptitle('Precipitations in millimeters')
plt.savefig('Precipitations.svg')
#%% создадим две датыфрейм с функцией среднего месячногоо по температуре
df_Mosk_mean = ms["2013"].groupby(lambda d: d.month).mean()["TAVG"]
df_SPb_mean = spb["2013"].groupby(lambda d: d.month).mean()["TAVG"]
mean_df = pd.concat([df_Mosk_mean,df_SPb_mean], axis=1)
mean_df.columns = ["Moscow_means", "SPb_means"]
print(mean_df)
#%% расчитаем стандартную ошибку для средних
df_Mosc = ms['2013-1':'2013-12'].dropna(subset=['TAVG'], axis = 0)
df_SPb = spb['2013-1':'2013-12'].dropna(subset=['TAVG'], axis = 0)                       
df_Mosc["MONTH"] = df_Mosc.index.map(lambda d: d.month)
df_SPb["MONTH"] = df_SPb.index.map(lambda d: d.month)
df_Mstderr = Means(df_Mosc["MONTH"], df_Mosc["TAVG"])
df_SPbstderr = Means(df_SPb["MONTH"],df_SPb["TAVG"])
#print(df_Mstderr.stderrs)
#print(df_SPbstderr.stderrs)
stderr_df = pd.DataFrame({'Moscow_stderrs':df_Mstderr.stderrs,
                          'SPb_stderrs':df_SPbstderr.stderrs},
                         index=[1, 2, 3,4,5,6,7,8,9,10,11,12])
print(stderr_df)
#df_SPb[['TAVG','MONTH']].head()
#%% Изобразим среднемесячную температуру
p1=plt.bar(df_Mosk_mean.index,df_Mosk_mean,width=0.36,align='edge') # график средних 
p2=plt.bar(df_SPb_mean.index,df_SPb_mean,width=-0.36,align='edge')
Mosc_error=[df_Mstderr.stderrs[i]*1.96 for i in range(len(df_Mstderr.stderrs))]
SPb_error=[df_SPbstderr.stderrs[i]*1.96 for i in range(len(df_SPbstderr.stderrs))]
p3=plt.errorbar(df_Mosk_mean.index+0.18,df_Mosk_mean, yerr=Mosc_error,linestyle='None',
                color='black') #график доверительного интервала
p4=plt.errorbar(df_SPb_mean.index-0.18,df_SPb_mean, yerr=SPb_error,linestyle='None',
                color='black') #график доверительного интервала
plt.title('Average monthly temperatures')
plt.legend((p1[0], p2[0]), ('Moscow', 'SPb'))
plt.savefig('Average_monthly_temperatures.svg')
plt.show()
#%% Нарисуем скрипичные диаграммы violinplot()
Data=pd.concat([df_Mosc["TAVG"], df_SPb[["TAVG","MONTH"]]], axis=1, sort=False)
df_long = pd.concat([
    pd.DataFrame({
        "TAVG": Data.iloc[:, 0], 
        "City": "Moscow"
    }),
    pd.DataFrame({
        "TAVG": Data.iloc[:, 1], 
        "City": "SPb"
    })
])

df_long["Month"] = df_long.index.map(lambda d: d.month_name())
#print(df_long)
sns.violinplot(data=df_long, y="TAVG", x="Month", hue="City", split=True)
plt.xticks(rotation='vertical')
plt.savefig('violin.svg')
#%% изобразитм ящичные диаграммы(boxplot())
Data_2=pd.concat([df_Mosc["PRCP"], df_SPb[["PRCP","MONTH"]]], axis=1, sort=False)
df_long2 = pd.concat([
    pd.DataFrame({
        "PRCP": Data.iloc[:, 0], 
        "City": "Moscow"
    }),
    pd.DataFrame({
        "PRCP": Data.iloc[:, 1], 
        "City": "SPb"
    })
])

df_long2["Month"] = df_long2.index.map(lambda d: d.month_name())

plt.figure(figsize=(10, 10))
sns.boxplot(x="Month", y="PRCP",
            hue="City", data=df_long2, linewidth=.5)
plt.xticks(rotation='vertical')
plt.savefig('boxplot.svg')
plt.show()

#%% 7. Найдите дни, в которых дневной разброс температур 
#(максимальная минус минималь- ная) был самым большим и самым маленьким (по каждому городу).

ms['Max_Mosc']=(ms.loc[:,'TMAX']-ms.loc[:,'TMIN'])
ms.dropna(subset=['Max_Mosc'],axis = 0)
max_M=ms.sort_values(by='Max_Mosc', ascending=False)
print(max_M.ix[:1,['Max_Mosc']])
spb['Max_SPb']=(spb.loc[:,'TMAX']-spb.loc[:,'TMIN'])
spb.dropna(subset=['Max_SPb'],axis = 0)
max_S=spb.sort_values(by='Max_SPb', ascending=False)
print(max_S.ix[:1,['Max_SPb']]) 
#%%









































