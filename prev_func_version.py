#Returns the RO file for all SOOT loads at a given temperature 
#(approximately close to that Temperature)

def ro_file_list():   #returns the working directory path, the names and index 
                      #of the files under consideration
    import os
    import numpy as np
        
    p = raw_input('Enter the working directory path: ')     #'C:\Users\Preeti\Desktop\CTS\Test Data\gpl'    
    my_path = p
    os.chdir(my_path)
    filename = os.listdir(my_path)
    
    r = ''
    
    r = raw_input('Enter the indices to be considered (Hit ENTER if you would like to enter a range or enter the index numbers strictly with commas and no other characters: ')        #range(0,12,2)
    if  r == '':
        r_0 = raw_input('Would you like to define a range of indices? [y/n] : ')
        if r_0 == 'y':
            r_1 = raw_input('Please enter the first digint for your range: ')
            r_1 = int(r_1)
            r_2 = raw_input('Please enter the last value for you range: ')
            r_2 = int(r_2)
            r_2 = r_2 + 1
            r_3 = raw_input('Please enter the increment for your range (Type 0 if there are no steps): ')
            r_3 = int(r_3)
            
            r = range(r_1,r_2,r_3)
            
    else:
        r = map(int, r.split(',')) 
        
    temp_cycle = r        
    temp_file = list()
    
    for index in range(len(temp_cycle)):
        ind_temp = temp_cycle[index]
        temp_file.insert(index,filename[ind_temp])
        
    ans_1 = raw_input('Are the RO files arranged in increasing order of Soot load? [y/n] : ')
    if ans_1 == 'n':
        ans_2 = raw_input('Please enter the order in which you would like to arrange your files : ')
        ans_2 = map(int, ans_2.split(',')) 
        ans_2 = np.array(ans_2)
        order_file = np.array(temp_file)
        temp_file = order_file[ans_2]
        temp_file.tolist()

        
    return my_path,temp_file,temp_cycle
        
    
     

def unique_temperature(my_path,temp_file):
#Returns unique Temperature values for a given Soot Load RO File. This file 
#can be used to create a temperature profile for all the given soot loads. 



    import pandas as pn
    import os
#    a = ro_file_list()
#    mypath = a[0]
#    tempfile = a[1]
    mypath = my_path
    tempfile = temp_file
    x = len(tempfile)
    cycle_ind = range(0,x)
    temp_chart = pn.DataFrame()
    
    
    for num in range(len(tempfile)):
        my_temp_path = mypath+'\\'+tempfile[num]+'\\'+tempfile[num]
        os.chdir(my_temp_path)
        temp_filename = os.listdir(my_temp_path)
        if temp_filename[0] == '.Rhistory':
            temp_filename.pop(0)   #If there are any other files listed in the folder.
        first_temp_unit = pn.DataFrame()
        column_name = [str(cycle_ind[num]) + 'gpl']
        for index in range(len(temp_filename)):
            ro_file = pn.read_csv(temp_filename[index], usecols = ['Inlet Temp','Outlet Temp'])
            ro_file['Avg_Temp'] = ro_file[['Inlet Temp','Outlet Temp']].mean(axis = 1)
            soot_first_unit = ro_file['Avg_Temp']
            #soot_first_unit = pn.DataFrame(soot_first_unit)
            if index == 0:
                first_temp_unit = first_temp_unit.append(soot_first_unit[[0]])
            else:
                first_temp_unit = first_temp_unit.append(soot_first_unit[[0]], ignore_index = True)
        first_temp_unit.columns = column_name
        temp_chart = pn.concat([temp_chart,first_temp_unit], axis = 1)
    
    ans_1 = raw_input('Would you like to save the file to a new folder in the working directory? [y/n] : ')
    
    
    if ans_1 == 'y':
        destination = mypath + '\Temp_Regen'
        if not os.path.exists(destination): os.makedirs(destination)
        os.chdir(destination)
        temp_chart.to_csv('Temperature_chart.csv', index = False)
    else:
        ans_2 = raw_input('Would like to have the condensed version of the temperature chart?[y/n] : ')
        if ans_2 == 'y':
            temp_chart_condensed = temp_chart.dropna()
            ans_3 = raw_input('Would you like to save this file?[y/n] : ')
            if ans_3 == 'y':
                temp_chart_condensed.to_csv('temperature_condensed.csv')
        else:
            temp_chart_condensed = temp_chart
    final_temp_chart = temp_chart_condensed
    return final_temp_chart
    
    
def parameter_component(my_path, temp_file,parameter):
#Returns a dataframe consisting of the parameter values for all the SOOT 
#load files represented by the columns
    import pandas as pn
    import os
    
    mypath = my_path
    #tempcycle = temp_cycle
    tempfile = temp_file
    param_comp = pn.DataFrame()
    for num in range(len(tempfile)):
        my_temp_path = mypath + '\\' + tempfile[num]+ '\\' + tempfile[num]
        os.chdir(my_temp_path)
        temp_filename = os.listdir(my_temp_path)
        temp_filename.pop(0)   #If there are any other files listed in the folder.
        temp_soot = pn.DataFrame()
        column_name = [str(num) + 'gpl']
        for index in range(len(temp_filename)):
            ro_file = pn.read_csv(temp_filename[index], usecols = [parameter])
            ro_file = pn.DataFrame(ro_file)
            temp_soot = pn.concat([temp_soot,ro_file], axis = 1)
            temp_param = temp_soot.mean(axis = 1, name = column_name)
            temp_param = pn.DataFrame(temp_param)
            temp_param.columns = column_name
        param_comp = pn.concat([param_comp, temp_param], axis = 1)
                                
    ans_1 = raw_input('Would you like to save this file? [y/n] : ')
    if ans_1 == 'y':
        destination = mypath + '\Temp_Regen'
        para = parameter + '_comp.csv'
        param_comp.to_csv(para)
    else:
        return(param_comp)
                        
    
    

               
def param_subset(my_path, temp_cycle, temp_file, temp_chart_condensed):
#Returns the plot for the average of the parameter at a given 
#temperature/frequency over the entire temperature range with a monotonic 
#behaviour of the soot load files
    import os
    import pandas as pn
    #import numpy as np
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
    
    store_region = pn.DataFrame()
    for i in range(rw_index.shape[1]):
        if i == 0:
            region_of_interest = rw_index[[i]]
        else:
            #store_region = rw_index.iloc[i]
            store_region = rw_index[[i]]
            region_of_interest[region_of_interest.isin(store_region)]
            
    ans_1 = raw_input('Would you like to check the monotonic region over the average parameter? [y/n] : ')
    if ans_1 == 'y':
        param_plot = ft.parameter_component(my_path, temp_file, parameter)
        #param_copy = param_plot
        param_plot[~param_plot.index.isin(region_of_interest.iloc[:,0])] = None
        
        param_plot.plot()
        plot_title = 'Average' + parameter + 'values over the entire temperature range'
        mp.title(parameter)
        mp.xlabel('Frequency Count')
    
    ans_3 = 'y'    
    while ans_3 == 'y':
        ans_2 = raw_input('Would you like to check the monotonic region over a specified temperature? [y/n] : ')
        if ans_2 == 'y':
            param_sub = ft.temp_parameter_extract(my_path, temp_file, tcc)
            param_comp = param_sub[0]
            param_comp[~param_comp.index.isin(region_of_interest.iloc[:,0])] = None
            
            param_comp.plot()
            plot_title = parameter + ' at ' + str(param_sub[1]) + ' Degrees C' 
            mp.title(plot_title)
            mp.xlabel('Frequency Count')
            
        ans_3 = raw_input('Would you like to check at another temperature or check out a different parameter? [y/n] : ')
    
    
    
    
       
def temp_index_extract(my_path,tcc):
    import pandas as pn
    import numpy as np
    ans_1 = raw_input('Enter the temperature you would like to check at : ' )
    tcc = tcc.round(0).astype(int)
    
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
    file_output = (file_index, temp_value)
    return (file_output)
                   
        #my_temp_path = mypath+'\\'+tempfile[soot_col]+'\\'+tempfile[soot_col]
        
        
        
def temp_parameter_extract(my_path,temp_file, tcc):
    import os
    import pandas as pn
    import func_trial as ft
    import matplotlib.pyplot as mp
    mp.style.use('ggplot')
    
    mypath = my_path
    fi = ft.temp_index_extract(my_path,tcc)
    file_index = fi[0]
    temp_value = fi[1]
    tempfile = temp_file
    parameter = raw_input('Enter the parameter that you would like to check: [Magnitude/ Phase] : ')
    param_comp = pn.DataFrame()
    for i in range(len(file_index)):
        my_temp_path = mypath+'\\'+tempfile[i]+'\\'+tempfile[i]
        os.chdir(my_temp_path)
        temp_filename = os.listdir(my_temp_path)
        if temp_filename[0] == '.Rhistory':
            temp_filename.pop(0)
        ro_file = pn.read_csv(temp_filename[file_index[i]], usecols = [parameter])
        ro_file = pn.DataFrame(ro_file)
        ro_file.columns = [str(i)]
        param_comp = pn.concat([param_comp,ro_file], axis = 1)
    #plot_title = parameter + ' at ' + str(temp_value) + ' Degrees C' 
    
    #f2 = param_comp.plot()
    #mp.title(plot_title)
    #mp.xlabel('Frequency Count')
    file_output = (param_comp, temp_value)
    return file_output