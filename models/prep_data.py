# use these functions to prepare data to feed into model
import pandas as pd
from sklearn.model_selection import train_test_split

# these are the time series columns that I need to remove
TS_COLS = ['cpu1','cpu2','cpu3','cpu4','cpu_avg','cpu1_d1','cpu2_d1',\
'cpu3_d1','cpu4_d1','cpu_avg_d1','r','w','n_in','n_out','r_d1','w_d1',\
'n_in_d1','n_out_d1']
# these are the extra columns relating to r, w, network, etc.
EXTRA_COLS = ['r_mean','r_median','r_sd','r_var','r_max','r_min','w_mean',\
'w_median','w_sd','w_var','w_max','w_min','n_in_mean','n_in_median',\
'n_in_sd','n_in_var','n_in_max','n_in_min','n_out_mean','n_out_median',\
'n_out_sd','n_out_var','n_out_max','n_out_min','r_d1_mean','r_d1_median',\
'r_d1_sd','r_d1_var','r_d1_max','r_d1_min','w_d1_mean','w_d1_median',\
'w_d1_sd','w_d1_var','w_d1_max','w_d1_min','n_in_d1_mean','n_in_d1_median',\
'n_in_d1_sd','n_in_d1_var','n_in_d1_max','n_in_d1_min','n_out_d1_mean',\
'n_out_d1_median','n_out_d1_sd','n_out_d1_var','n_out_d1_max','n_out_d1_min']
# these are the extra CPU columns
EXTRA_CPU = ['cpu1_mean','cpu1_median','cpu1_sd','cpu1_var','cpu1_max',\
'cpu1_min','cpu2_mean','cpu2_median','cpu2_sd','cpu2_var','cpu2_max',\
'cpu2_min','cpu3_mean','cpu3_median','cpu3_sd','cpu3_var','cpu3_max',\
'cpu3_min','cpu4_mean','cpu4_median','cpu4_sd','cpu4_var','cpu4_max',\
'cpu4_min','cpu1_d1_mean','cpu1_d1_median','cpu1_d1_sd','cpu1_d1_var',\
'cpu1_d1_max','cpu1_d1_min','cpu2_d1_mean','cpu2_d1_median','cpu2_d1_sd',\
'cpu2_d1_var','cpu2_d1_max','cpu2_d1_min','cpu3_d1_mean','cpu3_d1_median',\
'cpu3_d1_sd','cpu3_d1_var','cpu3_d1_max','cpu3_d1_min','cpu4_d1_mean',\
'cpu4_d1_median','cpu4_d1_sd','cpu4_d1_var','cpu4_d1_max','cpu4_d1_min']

def binary_prep(filename, mode):
    '''
    mode (int)
        1 - use all data except for timeseries
        2 - use all data except for timeseries and r, w, n_in, n_out data
        3 - use only the cpu_avg data

    return
        x_train, x_test, y_train, y_test
    '''
    df = pd.read_csv(filename)
    if mode is 1:
        df = df.drop(TS_COLS, axis=1)
    elif mode is 2:
        df = df.drop(TS_COLS, axis=1)
        df = df.drop(EXTRA_COLS, axis=1)
    elif mode is 3:
        df = df.drop(TS_COLS, axis=1)
        df = df.drop(EXTRA_COLS, axis=1)
        df = df.drop(EXTRA_CPU, axis=1)
