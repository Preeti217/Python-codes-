# -*- coding: utf-8 -*-
"""
Created on Tue Mar 01 11:00:35 2016

@author: Preeti
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

my_path = 'C:\Users\Preeti\Desktop\CTS\Porsche'
os.chdir(my_path)
filename = os.listdir(my_path)


my_temp_path = my_path + '\\' + filename[0] + '\\' + filename[0]

os.chdir(my_temp_path)

temp_file = os.listdir(my_temp_path)
ro_area_curve = pd.Series()
if temp_file[0] == '.Rhistory':
    temp_file.pop(0)
for index in range(len(temp_file)):
    ro_temp = pd.read_csv(temp_file[index], usecols = ['Magnitude'])
    area_value = area_under_curve(ro_temp)
    area_param = pd.DataFrame(area_value)
    ro_area_curve = pd.concat([ro_area_curve,area_param], ignore_index = True)
    


def area_under_curve(ro_temp):
    l = len(ro_temp)
    first = ro_temp.loc[[0]]
    last = ro_temp.loc[[l-1]]
    mid_sum = ro_temp[ro_temp.index.isin(range(1,l-1))].sum()
    mid_sum = np.array(mid_sum)
    end_sum = (first.values + last.values) * 0.5
    
    return end_sum+mid_sum
    
Axes3D.plot_surface(ro_area_curve,1) 
   