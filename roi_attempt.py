# -*- coding: utf-8 -*-
"""
Created on Wed Mar 02 15:32:03 2016

@author: Preeti
"""
#z = 1: have a specific file index for each soot load to check for the ROI
#   0: would like to check the ROI over the entire temperature range    
def region_of_interest(param_del,z):
    import pandas as pn
    import numpy as np
    import func_trial as ft
    
    param_df = param_del
    if z == 0:
        col = param_df.shape[1]
        for i in range(col-1,0,-1):
            curr = param_df[[i]]
            curr.columns = ['curr']
            prev = param_df[[i - 1]]
            prev.columns = ['prev']
            check = pn.concat([prev,curr],axis = 1)
            col_ind = check.loc[check['prev'] >= check['curr']]
            col_ind = np.array(col_ind.index)
            col_ind = pn.Series(col_ind)
            param_df = param_df.loc[param_df.index.isin(col_ind.index)]
            
        
        
        
        
    