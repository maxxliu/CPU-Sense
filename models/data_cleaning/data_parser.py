import pandas as pd
import csv
import numpy as np
from statistics import *
import os


# global variables
READINGS_SEC = 20
'''
For our first prediction models we want to reformat the data like so:
1. Find the times at which there is a change in which applications are
    running
2. Gather the data from 1 second before that time and 8 seconds after that time
3. Now you should have a data row that looks like:
    [application that was just opened, other app data, cpu, r/w, network]

I am actually not sure if there will be enough time before the start of the
first application open so might just take the data from after application start
'''


def find_app_changes(df):
    '''
    df - pandas dataframe

    returns:
        change_times - has triples of (app that was turned on, time, index)
    '''
    change_times = []

    prev_apps_running = [0, 0, 0, 0, 0]
    for index, row in df.iterrows():
        cur_apps_running = [row['App1'], row['App2'], row['App3'], row['App4'], row['App5']]
        for i in range(len(prev_apps_running)):
            if prev_apps_running[i] != cur_apps_running[i]:
                app_changed = i + 1
                change_times.append((app_changed, index, prev_apps_running))
                break
        prev_apps_running = cur_apps_running

    return change_times


def reformat_data(df, change_times, csv_out):
    '''
    df - pandas dataframe
    change_times - times where a change occurred
    csv_out - list to store output lines

    reformat to part 3 of description above
    NOTE: part description no longer up to date
    '''
    for change in change_times:
        index = change[1]
        app_changed = change[0]
        prev_state = change[2]
        cpu1 = list(df['CPU1'][index-(READINGS_SEC*1):index+(READINGS_SEC*8)])
        cpu2 = list(df['CPU2'][index-(READINGS_SEC*1):index+(READINGS_SEC*8)])
        cpu3 = list(df['CPU3'][index-(READINGS_SEC*1):index+(READINGS_SEC*8)])
        cpu4 = list(df['CPU4'][index-(READINGS_SEC*1):index+(READINGS_SEC*8)])
        cpu_avg = list([sum([cpu1[i], cpu2[i], cpu3[i], cpu4[i]])/4 for i in range(len(cpu1))])
        cpu1_d1 = list(np.gradient(np.array(cpu1)))
        cpu2_d1 = list(np.gradient(np.array(cpu2)))
        cpu3_d1 = list(np.gradient(np.array(cpu3)))
        cpu4_d1 = list(np.gradient(np.array(cpu4)))
        cpu_avg_d1 = list(np.gradient(np.array(cpu_avg)))
        r = list(df['read_bytes'][index-(READINGS_SEC*1):index+(READINGS_SEC*8)])
        w = list(df['write_bytes'][index-(READINGS_SEC*1):index+(READINGS_SEC*8)])
        n_in = list(df['bytes_sent'][index-(READINGS_SEC*1):index+(READINGS_SEC*8)])
        n_out = list(df['bytes_recv'][index-(READINGS_SEC*1):index+(READINGS_SEC*8)])
        r_d1 = list(np.gradient(np.array(r)))
        w_d1 = list(np.gradient(np.array(w)))
        n_in_d1 = list(np.gradient(np.array(n_in)))
        n_out_d1 = list(np.gradient(np.array(n_out)))

        data = [1, app_changed, prev_state[0], prev_state[1], prev_state[2], \
                prev_state[3], prev_state[4], \
                cpu1, cpu2, cpu3, cpu4, cpu_avg, \
                cpu1_d1, cpu2_d1, cpu3_d1, cpu4_d1, cpu_avg_d1, r, w, n_in, n_out, \
                r_d1, w_d1, n_in_d1, n_out_d1]
        csv_out.append(data)

        '''
        from this change time I also know that we have data for a duration
        of 9-10 seconds where this app is just running. I want to include a
        data line of this period where no new apps are being added.
        '''
        cpu1 = list(df['CPU1'][index+(READINGS_SEC*3):index+(READINGS_SEC*12)])
        cpu2 = list(df['CPU2'][index+(READINGS_SEC*3):index+(READINGS_SEC*12)])
        cpu3 = list(df['CPU3'][index+(READINGS_SEC*3):index+(READINGS_SEC*12)])
        cpu4 = list(df['CPU4'][index+(READINGS_SEC*3):index+(READINGS_SEC*12)])
        cpu_avg = [sum([cpu1[i], cpu2[i], cpu3[i], cpu4[i]])/4 for i in range(len(cpu1))]
        cpu1_d1 = list(np.gradient(np.array(cpu1)))
        cpu2_d1 = list(np.gradient(np.array(cpu2)))
        cpu3_d1 = list(np.gradient(np.array(cpu3)))
        cpu4_d1 = list(np.gradient(np.array(cpu4)))
        cpu_avg_d1 = list(np.gradient(np.array(cpu_avg)))
        r = list(df['read_bytes'][index+(READINGS_SEC*3):index+(READINGS_SEC*12)])
        w = list(df['write_bytes'][index+(READINGS_SEC*3):index+(READINGS_SEC*12)])
        n_in = list(df['bytes_sent'][index+(READINGS_SEC*3):index+(READINGS_SEC*12)])
        n_out = list(df['bytes_recv'][index+(READINGS_SEC*3):index+(READINGS_SEC*12)])
        r_d1 = list(np.gradient(np.array(r)))
        w_d1 = list(np.gradient(np.array(w)))
        n_in_d1 = list(np.gradient(np.array(n_in)))
        n_out_d1 = list(np.gradient(np.array(n_out)))

        prev_state[app_changed - 1] = 1
        app_changed = 0
        data = [0, app_changed, prev_state[0], prev_state[1], prev_state[2], \
                prev_state[3], prev_state[4], \
                cpu1, cpu2, cpu3, cpu4, cpu_avg, \
                cpu1_d1, cpu2_d1, cpu3_d1, cpu4_d1, cpu_avg_d1, r, w, n_in, n_out, \
                r_d1, w_d1, n_in_d1, n_out_d1]
        csv_out.append(data)

    return


def add_statistics_data(csv_out):
    '''
    add statistics data for time series data
    '''
    for i, row in enumerate(csv_out):
        # we need to get statistics for all of the time series data
        for item in row:
            if type(item) == list:
                a_mean = mean(item)
                n_median = median(item)
                sd = stdev(item)
                var = variance(item)
                max_ = max(item)
                min_ = min(item)
                csv_out[i].extend([a_mean, n_median, sd, var, max_, min_])


def process_files(files, exp):
    '''
    files - list of files
    exp (int) - indicate if these files are for experiment 1 or 2

    will create one big new csv with all processed data
    when running models just remove the columns that we don't want to use
    '''
    col_headers = ['change', 'app', 'a1', 'a2', 'a3', 'a4', 'a5', 'cpu1', 'cpu2', \
                    'cpu3', 'cpu4', 'cpu_avg',
                    'cpu1_d1', 'cpu2_d1', 'cpu3_d1', 'cpu4_d1', 'cpu_avg_d1', \
                    'r', 'w', 'n_in', 'n_out', \
                    'r_d1', 'w_d1', 'n_in_d1', 'n_out_d1']
    for col in col_headers[7:]:
        col_headers.append(col + '_mean')
        col_headers.append(col + '_median')
        col_headers.append(col + '_sd')
        col_headers.append(col + '_var')
        col_headers.append(col + '_max')
        col_headers.append(col + '_min')

    csv_out = []
    for file in files:
        df = pd.read_csv(file)
        change_times = find_app_changes(df)
        # if file is for experiment 1, I only want the first change for now
        if exp == 1:
            change_times = [change_times[0]]
        reformat_data(df, change_times, csv_out)

    # add the stats data features
    add_statistics_data(csv_out)

    # outputname
    if exp == 1:
        outputname = '../data/experiment1_data.csv'
    else:
        # must be experiment 2
        outputname = '../data/experiment2_data.csv'
    # write the new data to a file
    with open(outputname, "w") as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(col_headers)
        for data in csv_out:
            writer.writerow(data)

    return

# testing to make sure my changes still work
# files = ['exp2_example.csv']
# process_files(files, 2)

def get_exp1_files():
    '''
    returns a list of experiment 1 data files
    '''
    filepath = '../../experiments/exp_1_data/'
    files = [filepath + f for f in os.listdir(filepath)]

    return files


def get_exp2_files():
    '''
    returns a list of experiment 2 data files
    '''
    filepath = '../../experiments/exp_2_data/'
    files = [filepath + f for f in os.listdir(filepath)]

    return files


if __name__ == '__main__':
    exp1_files = get_exp1_files() # data for exp 1
    exp2_files = get_exp2_files() # data for exp 2

    process_files(exp1_files, 1) # process exp 1 data
    process_files(exp2_files, 2) # process exp 2 data
