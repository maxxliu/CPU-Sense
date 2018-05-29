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

APP_COLS = ['a1', 'a2', 'a3', 'a4', 'a5']

def binary_prep(filename, mode, test_size=0.2, seed=20):
    '''
    prepares data to feed into a binary classification model

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
    elif mode is 4: # the only data is CPU data
        df = df.drop(TS_COLS, axis=1)
        df = df.drop(EXTRA_COLS, axis=1)
        df = df.drop(EXTRA_CPU, axis=1)
        df = df.drop(APP_COLS, axis=1)

    y_var = 'change' # this is what we are trying to predict
    app_data = 'app' # this is data about what app just opened
    x = df.drop([y_var, app_data], axis=1)
    y = df[y_var]

    x_train, x_test, y_train, y_test = train_test_split(x, y, \
                                                        test_size=test_size, \
                                                        random_state=seed)

    return x_train, x_test, y_train, y_test


def app_prep(filename, mode, test_size=0.2, seed=20):
    '''
    prepares data to feed into classification model

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
    elif mode is 4: # the only data is CPU data
        df = df.drop(TS_COLS, axis=1)
        df = df.drop(EXTRA_COLS, axis=1)
        df = df.drop(EXTRA_CPU, axis=1)
        df = df.drop(APP_COLS, axis=1)

    y_var = 'app' # this is what we are trying to predict
    # change is the column that is telling us if an app was opened
    x = df.drop([y_var, 'change'], axis=1)
    y = df[y_var]

    x_train, x_test, y_train, y_test = train_test_split(x, y, \
                                                        test_size=test_size, \
                                                        random_state=seed)

    return x_train, x_test, y_train, y_test


EXP1_STATES = {'00000': 0,
                 '10000': 1,
                 '01000': 2,
                 '00100': 3,
                 '00010': 4,
                 '00001': 5}

EXP2_STATES = {'00000': 0,
                 '00100': 1,
                 '00101': 2,
                 '01000': 3,
                 '01001': 4,
                 '01010': 5,
                 '01011': 6,
                 '01100': 7,
                 '01101': 8,
                 '01110': 9,
                 '01111': 10,
                 '10000': 11,
                 '11000': 12,
                 '11100': 13,
                 '11110': 14,
                 '11111': 15}


def state_prep(filename, mode, STATES, test_size=0.2, seed=20):
    '''
    if we have access to the device then I can leave in app and change columns
    if we do not have access to the device then I cannot leave them in

    mode 1 - access to IoT device
    mode 2 - no access
    '''
    df = pd.read_csv(filename)

    # in general I am just gonna drop the following columns
    df = df.drop(TS_COLS, axis=1)
    df = df.drop(EXTRA_COLS, axis=1)
    df = df.drop(EXTRA_CPU, axis=1)

    # now I need to make some adjustments to the app columns
    device_state = []
    for index, row in df.iterrows():
        state = str(int(row['a1'])) +  str(int(row['a2'])) + \
                str(int(row['a3'])) + str(int(row['a4'])) + str(int(row['a5']))
        state = STATES[state]
        device_state.append(state)

    df['state'] = device_state

    if mode is 1: # we have access to the device
        df = df.drop(APP_COLS, axis=1)
    elif mode is 2: # we do not have access to the device
        df = df.drop(APP_COLS, axis=1)
        df = df.drop(['change', 'app'], axis=1)
    elif mode is 3: # same as mode 1 but we only use data from no changes
        df = df.drop(APP_COLS, axis=1)
        df = df.loc[df['change'] == 0]
    elif mode is 4: # same as mode 2 but only use data from no changes
        df = df.drop(APP_COLS, axis=1)
        df = df.loc[df['change'] == 0]
        df = df.drop(['change', 'app'], axis=1)

    x = df.drop(['state'], axis=1)
    y = df['state']

    x_train, x_test, y_train, y_test = train_test_split(x, y, \
                                                        test_size=test_size, \
                                                        random_state=seed)

    return x_train, x_test, y_train, y_test
