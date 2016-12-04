# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 09:53:21 2016

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
    tcc = temp_chart_condensed
    tcc = tcc.round(0).astype(int)
    parameter = raw_input('Which parameter do you want to check? [Magnitude/Phase] : ')

    y = tcc.shape[1]
    rw_index = pn.DataFrame()
    for ex in range(len(tcc)):
        #file_index = np.repeat(ex,y)        #Not being used to read ro)files. Currently using just all the files in sequence
        param_df = pn.DataFrame()
        cycle_ind = range(0,y)
        for num in range(len(tempcycle)):
            my_temp_path = mypath+'\\'+tempfile[num]+'\\'+tempfile[num]
            os.chdir(my_temp_path)
            temp_filename = os.listdir(my_temp_path)   
            if temp_filename[0] == '.Rhistory':
                temp_filename.pop(0)
            ro_file = pn.read_csv(temp_filename[ex], usecols = [parameter])
            ro_file = pn.DataFrame(ro_file)
            param_df = pn.concat([param_df, ro_file], axis = 1)
        
        param_df.columns = cycle_ind
       
        for g in range(y-1,0,-1):
            prec = g - 1
            succ = g
            a_1 = param_df[prec]
            b_1 = param_df[succ]            
            ab_df = pn.concat([a_1,b_1], axis = 1)
            ab_df.columns = ['a_1','b_1']
            ab_df = ab_df[['a_1','b_1']].query('a_1 > b_1') 
            param_df = param_df.loc[ab_df.index]
        col_ind = pn.Series(param_df.index, name = str(ex))
        if len(col_ind) != 0:
            rw_index = pn.concat([rw_index,col_ind], axis = 1)
    
    #rw_index = rw_index[rw_index < len(rw_index)]
    #rw_index = rw_index.dropna()
    
    store_region = pn.DataFrame()
    for i in range(rw_index.shape[1]):
        if i == 0:
            region_of_interest = rw_index[[i]]
        else:
            store_region = rw_index.iloc[i]
            region_of_interest[region_of_interest.isin(store_region)]
            #pn.Series(list(set(region_of_interest).intersection(set(store_region))))
            #region_of_interest = pn.Series(np.intersect1d(region_of_interest.values,store_region.values))
        
    param_plot = ft.parameter_component(my_path, temp_file, parameter)
    param_plot[~param_plot.index.isin(region_of_interest.iloc[:,0])] = None
    #param_plot[~(param_plot.index.isin(region_of_interest))] = None
    
    fi = param_plot.plot()
    mp.title(parameter)
    mp.xlabel('Frequency Count')
    
    return param_copy, fi


        
         
         
*****Saved Code*******************************

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
    
    tcc = temp_chart_condensed
    
    ans_1 = raw_input('Would you like to round off the temperatures off the temperature chart? [y/n] : ')
    parameter = raw_input('Which parameter do you want to check? [Magnitude/Phase] : ')
    if ans_1 == 'y':
        tcc = tcc.round(0).astype(int)
    
    y = tcc.shape[1]
    subset_index = pn.DataFrame()
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
            store_region = subset_index[[i]]
            region_of_interest = pn.Series(np.intersect1d(region_of_interest.values,store_region.values))
    
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
            
            
            
        