# I want to create a test csv with random numbers just to see how I would
# clean the data files before having the actual data from experiments
import csv

# this is the information we are collecting
# 14 columns
COL_HEADERS = ['t', 'a1', 'a2', 'a3', 'a4', 'a5', 'cpu1', 'cpu2', 'cpu3', 'cpu4', 'r', 'w', 'n_in', 'n_out']

NULL_ROWS_B = 20 * 2 # 20 readings a second and run nothing for 2 seconds
NULL_ROWS_A = 20 * 5 # 20 readings a second and run nothing for 5 seconds
APP_ROWS = 20 * 13 # 20 readings a second and run each app for 13 seconds

# lets first create the example data for experiment #1 (single app only run)
# this should run for 20 seconds, 2 second buffer before and after of nothing
csv_out = []
time = 0
for i in range(NULL_ROWS_B):
    time += 1
    data = [time, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    csv_out.append(data)
for i in range(APP_ROWS):
    time += 1
    data = [time, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    csv_out.append(data)
for i in range(NULL_ROWS_A):
    time += 1
    data = [time, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    csv_out.append(data)

with open("exp1_example.csv", "w") as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(COL_HEADERS)
    for data in csv_out:
        writer.writerow(data)

# now lets create an example for experiment #2 (sequential run)
# lets do 2 second buffer and then go into the other apps
csv_out = []
time = 0
for i in range(NULL_ROWS_B): # nothing running
    time += 1
    data = [time, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    csv_out.append(data)
for i in range(APP_ROWS): # app 1 starts running
    time += 1
    data = [time, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    csv_out.append(data)
for i in range(APP_ROWS): # app 3 starts running
    time += 1
    data = [time, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    csv_out.append(data)
for i in range(APP_ROWS): # app 5 starts running
    time += 1
    data = [time, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    csv_out.append(data)

with open("exp2_example.csv", "w") as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(COL_HEADERS)
    for data in csv_out:
        writer.writerow(data)
