# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 09:26:09 2016

@author: Preeti
"""

#This file is used to create a dataframe consisting of all RO files for a given SOOT LOAD
#Not a function. Use it just to create a dataframe in the given directory

#And it also returns unique Temperature values for a given Soot Load RO File. This file can be used to create
#a temperature profile for all the given soot loads. Use this file to create a csv and not as a function


import pandas as pn
import os

#Set the working directory
mypath = 'C:\Users\Preeti\Desktop\CTS\Test Data\gpl'

os.chdir(mypath)

filename = os.listdir(mypath)

#Lists the temperature cycle files using their indices
temp_cycle = range(0,12,2)
tempfile = list()

for index in range(len(temp_cycle)):
    ind_temp = temp_cycle[index]
    tempfile.insert(index,filename[ind_temp])
 
soot = list()
cycle_ind = range(0,6)
temp_chart = pn.DataFrame()
for num in range(len(tempfile)):
    my_temp_path = mypath+'\\'+tempfile[num]+'\\'+tempfile[num]
    os.chdir(my_temp_path)
    temp_filename = os.listdir(my_temp_path)
    temp_filename.pop(0)   #If there are any other files listed in the folder.
    temp_soot = pn.DataFrame()
    first_temp_unit = pn.DataFrame()
    column_name = [str(cycle_ind[num]) + 'gpl']
    for index in range(len(temp_filename)):
        ro_file = pn.read_csv(temp_filename[index])
        ro_file['Avg_Temp'] = ro_file[['Inlet Temp','Outlet Temp']].mean(axis = 1)
        soot_first_unit = ro_file['Avg_Temp']
        if index == 0:
            temp_soot = temp_soot.append(ro_file)
            first_temp_unit = first_temp_unit.append(soot_first_unit[[0]])
        else:
            temp_soot = temp_soot.append(ro_file, ignore_index = True)
            first_temp_unit = first_temp_unit.append(soot_first_unit[[0]], ignore_index = True)
    first_temp_unit.columns = column_name
    temp_chart = pn.concat([temp_chart,first_temp_unit], axis = 1)
    ro_name = str(cycle_ind[num]) + 'gpl' +'.csv'
    destination = mypath + '\Temp_Regen'
    if not os.path.exists(destination): os.makedirs(destination)
    temp_soot.to_csv(os.path.join(destination, ro_name))       
os.chdir(destination)
temp_chart.to_csv('Temperature_chart.csv', index = False)
temp_chart_condensed = temp_chart.dropna()
temp_chart_condensed.to_csv('temperature_condensed.csv')