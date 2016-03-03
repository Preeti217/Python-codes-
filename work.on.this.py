# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 15:33:18 2016

@author: Preeti
"""

def param_subset(my_path, temp_cycle, temp_file, temp_chart_condensed):
#Returns the plot for the average of the parameter at a given 
#temperature/frequency over the entire temperature range with a monotonic 
#behaviour of the soot load files
    import os
    import pandas as pn
    import numpy as np
    import func_trial as ft
    import matplotlib.pyplot as mp
    mp.style.use('ggplot')
    
    mypath = my_path
    tempcycle = temp_cycle
    tempfile = temp_file
    
    tcc = tcc.round(0).astype(int)
    
    y = tcc.shape[1]
    subset_index = pn.DataFrame()
    soot_col = pn.DataFrame()
    for index in range(y):
        param_comp = pn.DataFrame() 
        my_temp_path = mypath+'\\'+tempfile[index]+'\\'+tempfile[index]
        os.chdir(my_temp_path)
        temp_filename = os.listdir(my_temp_path)
        if temp_filename[0] == '.Rhistory':
            temp_filename.pop(0)
        for count in range(len(tcc)):
            ro_file = pn.read_csv(temp_filename[count], usecols = [parameter])
            ro_file = pn.DataFrame(ro_file)
            
            param_comp = pn.concat([param_comp,ro_file], axis = 1)
        param_comp = param_comp.mean(axis = 1)
        param_comp.name = str(index)
        soot_col = pn.concat([soot_col,param_comp], axis = 1)
        
    for g in range(y-1,0,-1):
        prec = g - 1
        succ = g
        a_1 = soot_col[soot_col.columns[prec]]
        b_1 = soot_col[soot_col.columns[succ]]
        ab = pn.concat([a_1,b_1], axis = 1)
        find_index = ab.index
        find_index = pn.DataFrame(find_index)
        find_index.columns = [str(ex)]
    subset_index = pn.concat([subset_index, find_index], axis = 1, join = 'inner')
        
        
    for ex in range(len(tcc)):
        x = ex
        file_index = np.repeat(x,y)
        param_comp = pn.DataFrame() 
        cycle_ind = range(0,y)
        for index in range(len(tempcycle)):
            my_temp_path = mypath+'\\'+tempfile[index]+'\\'+tempfile[index]
            os.chdir(my_temp_path)
            temp_filename = os.listdir(my_temp_path)
            if temp_filename[0] == '.Rhistory':
                temp_filename.pop(0)
            ro_file = pn.read_csv(temp_filename[file_index[index]], usecols = [parameter])
            ro_file = pn.DataFrame(ro_file)
            param_comp = pn.concat([param_comp,ro_file], axis = 1)

        param_comp.columns = cycle_ind
        param_copy = param_comp
        for g in range(y-1,0,-1):
            prec = g - 1
            succ = g
            a_1 = param_comp[prec]
            b_1 = param_comp[succ]
            param_comp = param_comp[a_1 > b_1]
        find_index = param_comp.index
        find_index = pn.DataFrame(find_index)
        find_index.columns = [str(ex)]
        subset_index = pn.concat([subset_index, find_index], axis = 1, join = 'inner')
        for i in range(subset_index.shape[1]):
            if i == 0:
                region_of_interest = subset_index[[i]]
            else:
                temp_interest = subset_index[[i]]
        region_of_interest = pn.Series(np.intersect1d(region_of_interest.values,temp_interest.values))
    
    param_plot = ft.parameter_component(my_path, temp_file, parameter)
    
#    ro = np.array(region_of_interest)  
#    roi = ro.tolist()
    param_plot[~param_plot.index.isin(region_of_interest.iloc[:,0])] = None
    
#    matplotlib.interactive(True)
#    matplotlib.is_interactive()
#    mp.hold(True)
    
    fi = param_plot.plot()
    mp.title(parameter)
    mp.xlabel('Frequency Count')
    
    return param_copy, fi
    