# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 15:58:22 2016

@author: Preeti
"""
#Returns the RO file for all SOOT loads at a given temperature (approximately close to that Temperature)

import pandas as pn
import os
import numpy as np

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
    
file_index = [22,22,22,22,22,22]
mag_comp = pn.DataFrame() 
cycle_ind = range(0,6)
for index in range(len(temp_cycle)):
    my_temp_path = mypath+'\\'+tempfile[index]+'\\'+tempfile[index]
    os.chdir(my_temp_path)
    temp_filename = os.listdir(my_temp_path)
    temp_filename.pop(0)
    column_name = [str(cycle_ind[index]) + 'gpl']#If there are any other files listed in the folder.
    ro_file = pn.read_csv(temp_filename[file_index[index]], usecols = ['Magnitude'])
    ro_file = pn.DataFrame(ro_file)
    ro_file.columns = column_name
    mag_comp = pn.concat([mag_comp,ro_file], axis = 1)

os.chdir('C:\Users\Preeti\Desktop\CTS\Test Data\gpl\Temp_Regen')
mag_comp.to_csv('mag_component.csv')


#Returns the index of all those rows for which as the soot load increases the magnitude drops

find_index = pn.Series()
for j in range(len(mag_comp)):
    temp_row = mag_comp.iloc[[j]]
    a = np.array(temp_row[[0]])
    b = np.array(temp_row[[1]])
    c = np.array(temp_row[[2]])
    d = np.array(temp_row[[3]])
    e = np.array(temp_row[[4]])
    f = np.array(temp_row[[5]])
    j = pn.Series(j)
    if a > b > c > d > e > f: 
        find_index = pn.concat([find_index,j], axis = 0)
       
