# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 14:28:06 2016

@author: Preeti
"""

#Returns the RO file for all SOOT loads at a given temperature 
#(approximately close to that Temperature)

import pandas as pn
import os
import numpy as np
import matplotlib.pyplot as mp
mp.style.use('ggplot')

#Set the working directory which has the individual gpl files 
#consisting of subfolders with the gpl csv files
mypath = 'C:\Users\Preeti\Desktop\CTS\Test Data\gpl'

os.chdir(mypath)

filename = os.listdir(mypath)

#Lists the temperature cycle file folders using their indices. 
#These are the folders that will be considered while extracting 
#the RF parameters for the given soot load
temp_cycle = range(0,12,2)
tempfile = list() #creates a blank variable which will be used to 
                  #store the filenames listed using the temp_cycle variable

for index in range(len(temp_cycle)):
    ind_temp = temp_cycle[index]
    tempfile.insert(index,filename[ind_temp])

#We now look into the file which has the temperature information for 
#the individual RO_files for each soot load. This dataframe is created using 
#the JM_temperature.py script.
os.chdir('C:\Users\Preeti\Desktop\CTS\Test Data\gpl\Temp_Regen')
jm = pn.read_csv('temperature_condensed.csv', index_col = 0) 


#The condensed temperature file has its temperatures rounded off to the 
#nearest integer for the ease of comparison between the various soot loads
#This assumption is made since a slight increase in temperature does not 
#cause a drastic change in the profile of a RF spectra for any given soot load.   
jm_1 = jm.round(0).astype(int)
y = jm_1.shape[1]
#jm_1 = pn.read_csv('jm_1.csv', usecols = ['Unnamed: 0']) 
subset_index = pn.DataFrame()
for ex in range(len(jm_1)):
    x = ex
    file_index = np.repeat(x,y)
    mag_comp = pn.DataFrame() 
    cycle_ind = range(0,y)
    for index in range(len(temp_cycle)):
        my_temp_path = mypath+'\\'+tempfile[index]+'\\'+tempfile[index]
        os.chdir(my_temp_path)
        temp_filename = os.listdir(my_temp_path)
        temp_filename.pop(0)  #If there are any other files listed in the folder.
        #column_name = ['a','b','c','d','e','f']
        column_name = list
        ro_file = pn.read_csv(temp_filename[file_index[index]], usecols = ['Magnitude'])
        ro_file = pn.DataFrame(ro_file)
        mag_comp = pn.concat([mag_comp,ro_file], axis = 1)
        
    mag_comp.columns = cycle_ind
    for g in range(y-1,0,-1):
        prec = g - 1
        succ = g
        mag_comp = mag_comp[mag_comp[prec] > mag_comp[succ]]
    find_index = mag_comp.index
    find_index = pn.DataFrame(find_index)
    find_index.columns = [str(ex)]
            
#Returns the index of all those rows for which as the soot load increases the magnitude drops
#    find_index = pn.DataFrame()
#    for j in range(len(mag_comp)):
#        temp_row = mag_comp.iloc[[j]]
#        a = np.array(temp_row[[0]])
#        b = np.array(temp_row[[1]])
#        c = np.array(temp_row[[2]])
#        d = np.array(temp_row[[3]])
#        e = np.array(temp_row[[4]])
#        f = np.array(temp_row[[5]])
#        ind = pn.Series(j)
#        ind = pn.DataFrame(ind)
#        if a > b > c > d > e > f: 
#            find_index = find_index.append(ind, ignore_index = True)
            
    #subset_index = pn.concat([subset_index, find_index], axis = 1, join = 'inner', ignore_index = True)
    subset_index = pn.concat([subset_index, find_index], axis = 1, join = 'inner')
        

for i in range(subset_index.shape[1]):
    if i == 0:
        region_of_interest = subset_index[[i]]
    else:
        temp_interest = subset_index[[i]]
        region_of_interest = pn.Series(np.intersect1d(region_of_interest.values,temp_interest.values))
    
    
os.chdir(mypath +'\Temp_Regen')    
m_c = pn.read_csv('mag_component.csv', index_col = 0)

roi = list(region_of_interest)   

m_c[~m_c.index.isin(roi)] = None


m_c.plot()
mp.title('Magnitude')
mp.xlabel('Temperature in deg C')