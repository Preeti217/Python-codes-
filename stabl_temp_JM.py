# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 09:47:00 2016

@author: Preeti
"""
import pandas as pd
import os


mypath = 'C:\Users\Preeti\Desktop\CTS\Test Data\gpl'

os.chdir(mypath)

filename = os.listdir(mypath)

temp_cycle = range(0,12,2)
tempfile = list()

for index in range(len(temp_cycle)):
    ind_temp = temp_cycle[index]
    tempfile.insert(index,filename[ind_temp])
    
cycle_ind = range(0,6)
for num in range(len(tempfile)):
    my_temp_path = mypath+'\\'+tempfile[num]+'\\'+tempfile[num]
    os.chdir(my_temp_path)
    temp_filename = os.listdir(my_temp_path)
    temp_filename.pop(0)   #If there are any other files listed in the folder.
    temp_soot = pd.DataFrame()
    first_temp_unit = pd.DataFrame()
    column_name = [str(cycle_ind[num]) + 'gpl']
    conc_range =range(66,101)
    for index in conc_range:
        ro_file = pd.read_csv(temp_filename[index], usecols = ['Magnitude'])
        ro_file = pd.DataFrame(ro_file)
        #ro_file['Avg_Temp'] = ro_file[['Inlet Temp','Outlet Temp']].mean(axis = 1)
        #soot_first_unit = ro_file['Avg_Temp']
        temp_soot = pd.concat([temp_soot,ro_file], axis = 1)
    #first_temp_unit.columns = column_name
    #temp_chart = pd.concat([temp_chart,first_temp_unit], axis = 1)
    temp_soot.columns = conc_range
    ro_name = str(cycle_ind[num]) + 'gpl' +'.csv'
    destination = mypath + '\Temp_Regen'
    if not os.path.exists(destination): os.makedirs(destination)
    temp_soot.to_csv(os.path.join(destination, ro_name))  