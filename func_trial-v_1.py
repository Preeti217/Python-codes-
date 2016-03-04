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
    
#    ans_1 = raw_input('Would you like to save the file to a new folder in the working directory? [y/n] : ')
    
    
#    if ans_1 == 'y':
#        destination = mypath + '\Temp_Regen'
#        if not os.path.exists(destination): os.makedirs(destination)
#        os.chdir(destination)
#        temp_chart.to_csv('Temperature_chart.csv', index = False)
#    else:
    ans_2 = raw_input('Would like to have the condensed version of the temperature chart?[y/n] : ')
    if ans_2 == 'y':
        temp_chart_condensed = temp_chart.dropna()
#            ans_3 = raw_input('Would you like to save this file?[y/n] : ')
#            if ans_3 == 'y':
#                temp_chart_condensed.to_csv('temperature_condensed.csv')
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
                                
#    ans_1 = raw_input('Would you like to save this file? [y/n] : ')
#    if ans_1 == 'y':
#        destination = mypath + '\Temp_Regen'
#        para = parameter + '_comp.csv'
#        param_comp.to_csv(para)
#    else:
    return(param_comp)
                        
    
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
        
        param_sub_df = subset_region(param_df,0)
        col_ind = pn.Series(param_sub_df.index, name = str(ex))
        if len(col_ind) != 0:
            rw_index = pn.concat([rw_index,col_ind], axis = 1)
    
    store_region = pn.DataFrame()
    for i in range(rw_index.shape[1]):
        if i == 0:
            region_of_interest_1 = rw_index[[i]]
        else:
            #store_region = rw_index.iloc[i]
            store_region = rw_index[[i]]
            #store_region.columns = region_of_interest.columns
            region_of_interest_1 = pn.Series(np.intersect1d(region_of_interest_1,store_region))
            #region_of_interest = region_of_interest.isin(store_region) & store_region.isin(region_of_interest)
            #region_of_interest_1 = pn.Series(region_of_interest.iloc[:,0])
            
    ans_1 = raw_input('Would you like to check the monotonic region over the average parameter? [y/n] : ')
    if ans_1 == 'y':
        param_plot = ft.parameter_component(my_path, tempfile, parameter)
        #param_copy = param_plot
        param_plot[~param_plot.index.isin(region_of_interest_1.iloc[:])] = None
        
        param_plot.plot()
        plot_title = 'Average' + parameter + 'values over the entire temperature range'
        mp.title(parameter)
        mp.xlabel('Frequency Count')
    
    ans_3 = 'y'    
    while ans_3 == 'y':
        ans_2 = raw_input('Would you like to check the monotonic region over a specified temperature? [y/n] : ')
        if ans_2 == 'y':
            param_sub = ft.temp_parameter_extract(my_path, tempfile, tcc)
            param_comp = param_sub[0]
            ans_4 = raw_input('Would like to check over all soot loads? [y/n] : ')
            if ans_4 == 'y':
                param_sub_df = ft.subset_region(param_comp,0)
                col_ind = pn.Series(param_sub_df.index)
                if len(col_ind) != 0:
                    region_of_interest_2 = col_ind
                
                param_comp[~param_comp.index.isin(region_of_interest_2.iloc[:])] = None
                
                param_comp.plot()
                plot_title = parameter + ' at ' + str(param_sub[1]) + ' Degrees C' 
                mp.title(plot_title)
                mp.xlabel('Frequency Count')
                
            else:
                ans_5 = raw_input('Please enter the column numbers that you would like to check the monotonic range for: ')
                param_sub_df = ft.subset_region(param_comp,ans_5)
                col_ind = pn.Series(param_sub_df.index)
                if len(col_ind) != 0:
                    region_of_interest_3 = col_ind
                
                param_comp[~param_comp.index.isin(region_of_interest_3.iloc[:])] = None
                
                param_comp.plot()
                plot_title = parameter + ' at ' + str(param_sub[1]) + ' Degrees C' 
                mp.title(plot_title)
                mp.xlabel('Frequency Count')
                
            
        ans_3 = raw_input('Would you like to check at another temperature or check out a different parameter? [y/n] : ')
    

               
#z = 1: have a specific file index for each soot load to check for the ROI
#   0: would like to check the ROI over the entire temperature range   
def subset_region(param_del,z):
    import pandas as pn
    import numpy as np
    import func_trial as ft
    
    if z == 0:
        param_df = param_del
        col = param_df.shape[1]
        for i in range(col-1,0,-1):
            curr = param_df.iloc[:,i]
            curr.name = 'curr'
            prev = param_df.iloc[:,i - 1]
            prev.name = 'prev'
            check = pn.concat([prev,curr],axis = 1)
            col_ind = check.ix[check['prev'] >= check['curr']]
            #col_ind = np.array(col_ind.index)
            col_ind = pn.Series(col_ind.index)
            param_df = param_df.ix[col_ind]
            
    else: 
        z = map(int,z.split(','))
        param_df = param_del.iloc[:,z]
        col = param_df.shape[1]
        for i in range(col-1,0,-1):
            curr = param_df.iloc[:,i]
            curr.name = 'curr'
            prev = param_df.iloc[:,i - 1]
            prev.name = 'prev'
            check = pn.concat([prev,curr],axis = 1)
            col_ind = check.ix[check['prev'] >= check['curr']]
            #col_ind = np.array(col_ind.index)
            col_ind = pn.Series(col_ind.index)
            param_df = param_df.ix[col_ind]
            
    return param_df
            
        
    
           
def temp_index_extract(my_path,temp_file,tcc,z):
    import os
    import pandas as pn
    import numpy as np
    import func_trial as ft
    
    
    ans_1 = raw_input('Enter the temperature you would like to check at : ' )
    tcc = tcc.round(0).astype(int)
    
    y = tcc.shape[1]
    temp_value = int(ans_1)
    file_index = np.repeat(0,y)
#    file_index = pn.Series(file_index)
    for soot_col in range(0,y):
        col_consideration = tcc.ix[:,soot_col]
        #idx = col_consideration.index[col_consideration <= temp_value]
        #idx = np.array(idx)
        idx = []   
        while len(idx) == 0:
            for i in range(0,z):
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
                    if check.values.all()  == True :
                        f = pn.Series(f)
                        temp_f = pn.concat([temp_f,f])
            if len(temp_f) == 0:
                file_index[soot_col] = None
            elif len(temp_f) == 1:
                file_index[soot_col] = temp_f.values
            else:
                dec = col_consideration[temp_f]
                dec_1 = abs(dec - temp_value)
                my_temp_path = my_path + '\\' + temp_file[soot_col] + '\\' + temp_file[soot_col]
                os.chdir(my_temp_path)
                temp_filename = os.listdir(my_temp_path)
                dec_2 = pn.Series()
                if temp_filename[0] == '.Rhistory':
                    temp_filename.pop(0)   #If there are any other files listed in the folder.
                for n in range(len(dec)):
                    ro_temp = pn.read_csv(temp_filename[n], usecols = ['Magnitude'])
                    area_ro = ft.area_under_curve(ro_temp)
                    area_ro = list(area_ro)
                    area_ro = pn.Series(area_ro)
                    dec_2 = pn.concat([dec_2,area_ro], ignore_index = True)
                dec_2.index = dec_1.index
                t_1 = dec_1.idxmin()
                t_2 = dec_2.idxmin()
                if t_1 == t_2:
                    file_index[soot_col] = t_1
                else: file_index[soot_col] = t_2
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
    fi = ft.temp_index_extract(my_path,temp_file,tcc,5)
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
    file_output = (param_comp, temp_value, file_index)
    return file_output
    

def area_under_curve(ro_temp):
    import numpy as np
    l = len(ro_temp)
    first = ro_temp.loc[[0]]
    last = ro_temp.loc[[l-1]]
    mid_sum = ro_temp[ro_temp.index.isin(range(1,l-1))].sum()
    mid_sum = np.array(mid_sum)
    end_sum = (first.values + last.values) * 0.5
    
    return end_sum+mid_sum
    
    
def surface_plot(my_path, temp_file):
    import os
    import pandas as pn
    import numpy as np
    
    mypath = my_path
    tempfile = temp_file
    ans_1 = raw_input('Enter the soot load values in increasing order : ')
    ans_1 = map(int, ans_1.split(','))
    
    temp_curve = pn.DataFrame()
    area_curve = pn.DataFrame()
    soot_curve = pn.DataFrame()
    
    for num in range(len(tempfile)):
        my_temp_path = mypath+'\\'+tempfile[num]+'\\'+tempfile[num]
        os.chdir(my_temp_path)
        temp_filename = os.listdir(my_temp_path)
        temp_mag = pn.Series()
        temp_temperature = pn.Series()
        if temp_filename[0] == '.Rhistory':
            temp_filename.pop(0)   #If there are any other files listed in the folder.
        for index in range(len(temp_filename)):
            ro_file = pn.read_csv(temp_filename[index], usecols = ['Inlet Temp','Outlet Temp','Magnitude'])
            ro_file['Avg_Temp'] = ro_file[['Inlet Temp','Outlet Temp']].mean(axis = 1)
            ro_file = ro_file.ix[1000:1101]
            ro_file = ro_file.reset_index()
            ro_mag = ro_file['Magnitude']
            temp_1 = area_under_curve(ro_mag)
            temp_1 = pn.DataFrame(temp_1)
            temp_2 = ro_file['Avg_Temp']
            temp_2 = temp_2[temp_2.index == 0]
            temp_mag = pn.concat([temp_mag,temp_1],ignore_index = True)
            temp_temperature = pn.concat([temp_temperature, temp_2], ignore_index = True)
        area_curve = pn.concat([area_curve,temp_mag], axis = 1)
        temp_curve = pn.concat([temp_curve, temp_temperature], axis = 1)
        l = len(temp_curve)
        temp_3 = np.repeat(ans_1[num],l)
        temp_soot = pn.Series(temp_3)
        soot_curve = pn.concat([soot_curve,temp_soot],axis = 1)
    
    area_curve.columns = ans_1
    temp_curve.columns = ans_1
    soot_curve.columns = ans_1
    
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')  
    for load in range(len(ans_1)):
        ax.plot(temp_curve.index,area_curve[[load]],load)
        
    
