# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 10:24:41 2016

@author: Preeti
"""
****V1******

****V2*****

def temp_index_extract(my_path,tcc):
    import pandas as pn
    import numpy as np
    ans_1 = raw_input('Enter the temperature you would like to check at : ' )
    tcc = tcc.round(0).astype(int)
    ans_2 = raw_input('Would you like to check the monotonic range over all soot loads? [y/n] : ')
    if ans_2 == 'y':
        y = tcc.shape[1]
        rang = range(0,y)
    else: 
        ans_3 = raw_input('Enter the column numbers of the soot load for which you wish to find monotonic range: ')
        ans_3 = map(int, ans_3.split(',')) 
        ans_3 = np.array(ans_3)
        rang = ans_3
        y = len(rang)
    
    temp_value = int(ans_1)
    file_index = np.repeat(0,y)
#    file_index = pn.Series(file_index)
    for soot_col in rang:
        col = np.where(rang == soot_col)
        col_consideration = tcc.ix[:,soot_col]
        idx = col_consideration.index[col_consideration == temp_value]
        idx = np.array(idx)        
        while len(idx) == 0:
            for i in range(0,10):
                temp_ind = col_consideration.index[col_consideration >= temp_value - i] & col_consideration.index[col_consideration <= temp_value + i ]
                temp_ind = np.array(temp_ind)
                idx = temp_ind
        if len(idx) == 1:
            mini_df = col_consideration[(idx-1):(idx+2)]
            check = sorted(mini_df) == mini_df
            if check is not False:
                file_index[col] = idx
            else: file_index[col] = None
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
                file_index[col] = None
            else:
                dec = col_consideration[temp_f]
                dec_1 = abs(dec - temp_value)
                t = dec_1.idxmin()
                file_index[col] = t
    file_output = (file_index, temp_value)
    return (file_output)
                   
        #my_temp_path = mypath+'\\'+tempfile[soot_col]+'\\'+tempfile[soot_col]
      