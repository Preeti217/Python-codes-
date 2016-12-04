# -*- coding: utf-8 -*-
"""
Created on Mon Feb 08 16:20:58 2016

@author: Preeti
"""

#Returns unique Temperature values for a given Soot Load RO File. This file can be used to create
#a temperature profile for all the given soot loads. Use this file to create a csv and not as a function


import pandas as pd
import numpy as np
import os

mypath = 'C:\Users\Preeti\Desktop\CTS\MTU Data\Temp_Regen'
os.chdir(mypath)

file_list = os.listdir(mypath)
my_order = [3,7,8,0,1,2,4,5,6]
file_list = [file_list[i] for i in my_order]
ro_name = [2,5,8,11,14,17,20,23,26]
temp_chart = pd.DataFrame()

for index in range(len(file_list)):
    temp_name = file_list[index]
    field_name = ['Avg_Temp']
    ro_number = ['K'+ str(ro_name[index])] 
    temp_file = pd.read_csv(temp_name, usecols = field_name)
    temp_file_1 = pd.unique(temp_file.values.ravel())
    temp_file_1 = pd.DataFrame(temp_file_1)
    #temp_file_1 = temp_file_1.rename(columns ={'0':ro_number})
    temp_file_1.columns = ro_number
    temp_chart = pd.concat([temp_chart,temp_file_1], axis = 1)
            

temp_chart_condensed = temp_chart.dropna()  
temp_chart.to_csv('temperature_chart.csv', index = False) 
temp_chart_condensed.to_csv('temperature_condensed.csv', index = False)
