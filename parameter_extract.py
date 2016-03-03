# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 15:13:26 2016

@author: Preeti
"""

def temp_parameter_extract(my_path,tcc):
    import os
    import pandas as pn
    import numpy as np
    ans_1 = raw_input('Enter the temperature you would like to check at : ' )
    ans_2 = raw_input('Would you like to round off the temperatures off the temperature chart? [y/n] : ')
    if ans_2 == 'y':
        tcc_1 = tcc.round(0).astype(int)
        tcc = tcc_1
    
    y = tcc.shape[1]
    temp_value = int(ans_1)
    file_index = np.repeat(0,y)
#    file_index = pn.Series(file_index)
    for soot_col in range(0,y):
        col_consideration = tcc.ix[:,soot_col]
        idx = col_consideration.index[col_consideration == temp_value]
        idx = np.array(idx)        
        while len(idx) == 0:
            for i in range(0,5):
                temp_ind = col_consideration.index[col_consideration >= temp_value - i] & col_consideration.index[col_consideration <= temp_value + i ]
                temp_ind = np.array(temp_ind)
                idx = temp_ind
        if len(idx) == 1:
            mini_df = col_consideration[(idx-1):(idx+2)]
            check = sorted(mini_df) == mini_df
            if check is not False:
                file_index[soot_col] = idx
            else: file_index[soot_col] = None
        else:
            temp_f = pn.Series()
            for j in range(len(idx)):
                f = idx[j]
                if f != 0:
                    mini_df = col_consideration[(f-1):(f+2)]
                    check = sorted(mini_df) == mini_df
                    if check is not False:
                        f = pn.Series(f)
                        temp_f = pn.concat([temp_f,f])
            if len(temp_f) == 0:
                file_index[soot_col] = None
            else:
                t = temp_f.iloc[0]
                file_index[soot_col] = t
    return file_index
                   
        #my_temp_path = mypath+'\\'+tempfile[soot_col]+'\\'+tempfile[soot_col]
        
        
        
        
        
        