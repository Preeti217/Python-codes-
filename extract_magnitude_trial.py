# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 15:41:27 2016

@author: Preeti
"""

import pandas as pd

import os

temp_min = 450
temp_max = 460

#os.chdir('C:\Users\Preeti\Desktop\CTS\MTU Data\Temp_Regen')
#mtu = pd.read_csv('temperature_condensed.csv', index = False)
#
#os.chdir('C:\Users\Preeti\Desktop\CTS\Test Data\gpl\Temp_Regen')
#jm = pd.read_csv('temperature_condensed.csv', index = False)
#
#mtu_1 = mtu.round(0).astype(int)
#jm_1 = jm.round(0).astype(int)

os.chdir('C:\Users\Preeti\Desktop\CTS')
#mtu_1.to_csv('mtu_1.csv', index = False)
#jm_1.to_csv('jm_1.csv', index = False)

jm_1 = pd.read_csv('jm_1.csv')

jm_1 = jm_1.drop(['Unnamed: 0'], axis = 1)
get_mono_index = pd.DataFrame()
get_mono_temp = pd.DataFrame()
for column in jm_1:
    temp_col = jm_1[column]
    n = len(temp_col)
    mono_series_index = pd.DataFrame()
    mono_series_temp = pd.DataFrame()
    for element in range(1,n-1):
        prev = temp_col[element - 1]
        nex = temp_col[element + 1]
        current = temp_col[element]
        if abs(current - prev) <= 2 and abs(nex - current) <= 2:
            current_series = [current]
            enter_series = [element]
            enter_series = pd.DataFrame(enter_series)
            current_series = pd.DataFrame(current_series)
            if len(mono_series_index) == 0:
                mono_series_index = mono_series_index.append(enter_series)
                mono_series_temp = mono_series_temp.append(current_series)                
            else:
                mono_series_index = mono_series_index.append(enter_series, ignore_index = True)
                mono_series_temp = mono_series_temp.append(current_series, ignore_index = True)                
    get_mono_index = pd.concat([get_mono_index,mono_series_index], axis = 1)
    get_mono_temp = pd.concat([get_mono_temp,mono_series_temp], axis = 1)
            
    
get_mono_index.columns = jm_1.columns
get_mono_temp.columns = jm_1.columns