import os

os.chdir('C:\Users\Preeti\Desktop\CTS\Codes\python')

from func_trial import *
#C:\Users\Preeti\Desktop\CTS\MTU Data
#C:\Users\Preeti\Desktop\CTS\Test Data\gpl
#C:\Users\Preeti\Desktop\CTS\FEV Calibration-Copy
#C:\Users\Preeti\Desktop\CTS\Porsche
a = ro_file_list()

my_path = a[0]

temp_file = a[1]

temp_cycle = a[2]


df = unique_temperature(my_path, temp_file)
a = param_subset(my_path, temp_cycle, temp_file, df)
#param_plot = parameter_component(my_path, temp_file, 'Magnitude')
#subset_file = subset_file[0]
