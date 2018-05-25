import time
import psutil
import multiprocessing
from threading import Thread
import csv
import copy
import Applications
import os
from sys import argv


def record_utilization(data, stop, divide):
    psutil.cpu_percent(percpu=True)
    temp = []
    while stop.value == 0:
        temp.append((
            psutil.cpu_freq(percpu=True),
            psutil.disk_io_counters(nowrap=True),
            psutil.net_io_counters(nowrap=True)
        ))
        if divide.value == 1:
            data.append(temp)
            temp = []
            divide.value = 0
        time.sleep(0.05)
    data.append(temp)
    return 0


def prepare_data_exp1(seq, data):
    overall = []
    for stage in data:
        per_stage = []
        for entry in stage:
            row = [cpu_freq[0] for cpu_freq in entry[0]]
            row += entry[1][2:4]
            row += entry[2][0:2]
            per_stage.append(row)
        overall.append(per_stage)
    initial_tag = [0] * 5
    if seq > 0:
        application_tag = [0] * (seq - 1) + [1] + [0] * (5 - seq)
    else:
        application_tag = initial_tag
    overall[0] = [initial_tag + entry for entry in overall[0]]
    overall[1] = [application_tag + entry for entry in overall[1]]
    overall[2] = [initial_tag + entry for entry in overall[2]]
    consolidated = [line for phase in overall for line in phase]
    return consolidated


def prepare_data_exp2(seq, data):
    possible_sequences = [[1, 2, 3, 4, 5],
                          [2, 3, 4, 5],
                          [2, 4, 5],
                          [2, 3, 5],
                          [3, 5],
                          [2, 5]]
    tags = [[0] * 5]
    for i in possible_sequences[seq - 1]:
        last_tag = copy.deepcopy(tags[-1])
        last_tag[i - 1] = 1
        tags.append(last_tag)
    final_form = []
    for i in range(0, len(data)):
        for entry in data[i]:
            row = [cpu_freq[0] for cpu_freq in entry[0]]
            row += entry[1][2:4]
            row += entry[2][0:2]
            row = tags[i] + row
            final_form.append(row)
    return final_form


def dump_data(data, experiment, sequence, exp_num):
    header = []
    for i in range(0, 5):
        header.append("App" + str(i + 1))
    for i in range(0, len(psutil.cpu_freq(percpu=True))):
        header.append("CPU" + str(i + 1))
    header.append("read_bytes")
    header.append("write_bytes")
    header.append("bytes_sent")
    header.append("bytes_recv")
    if experiment == 1:
        data_consolidated = prepare_data_exp1(sequence, data)
    elif experiment == 2:
        data_consolidated = prepare_data_exp2(sequence, data)
    with open("{0}_{1}_{2}.csv"
              .format(experiment, sequence, exp_num), "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)
        for row in data_consolidated:
            csvwriter.writerow(row)
        csvfile.close()


def get_exp2_seq(seq, video_app, voice_app, network_app):
    if seq == 1:
        sequence = [("f", video_app.hybrid, [0, 1, 0, 0]),
                    ("l", [0, 1, 1, 0]),
                    ("l", [0, 1, 1, 1]),
                    ("fs", voice_app.record), ("fn", network_app.transfer)]
    elif seq == 2:
        sequence = [("f", video_app.hybrid, [0, 0, 1, 0]),
                    ("l", [0, 0, 0, 1]),
                    ("fs", voice_app.record), ("fn", network_app.transfer)]
    elif seq == 3:
        sequence = [("f", video_app.hybrid, [0, 0, 1, 0]),
                    ("fs", voice_app.record), ("fn", network_app.transfer)]
    elif seq == 4:
        sequence = [("f", video_app.hybrid, [0, 0, 1, 0]),
                    ("l", [0, 0, 1, 1]), ("fn", network_app.transfer)]
    elif seq == 5:
        sequence = [("f", video_app.hybrid, [0, 0, 0, 1]),
                    ("fn", network_app.transfer)]
    elif seq == 6:
        sequence = [("f", video_app.hybrid, [0, 0, 1, 0]),
                    ("fn", network_app.transfer)]
        # Add application 5 later
    return sequence


def experiment2(seq):
    video_app = Applications.VideoRecorder()
    voice_app = Applications.VoiceRecorder()
    network_app = Applications.NetworkApplication()
    sequence = get_exp2_seq(seq, video_app, voice_app, network_app)
    times = [20]
    for i in range(0, len(sequence) - 1):
        times = [13 + times[0]] + times
    # Turn on monitor
    manager = multiprocessing.Manager()
    data = manager.list([])
    stop = multiprocessing.Value('i', 0)
    temp_divide = multiprocessing.Value('i', 0)
    monitor = multiprocessing.Process(target=record_utilization,
                                      args=(data, stop, temp_divide))
    print "Starting experiment"
    threads = []
    monitor.start()
    time.sleep(2)
    for i in range(0, len(sequence)):
        print "Started App {0}".format(i + 1)
        temp_divide.value = 1
        if sequence[i][0] == "f":
            shared_seq_list = sequence[i][2]
            t = Thread(target=sequence[i][1],
                       args=(times[i], shared_seq_list, ))
            t.start()
            threads.append(t)
        elif sequence[i][0] == "l":
            for j in range(0, len(sequence[i][1])):
                shared_seq_list[j] = sequence[i][1][j]
        elif sequence[i][0] == "fs":
            t = Thread(target=sequence[i][1],
                       args=(times[i], ))
            t.start()
            threads.append(t)
        elif sequence[i][0] == "fn":
            t = Thread(target=sequence[i][1])
            t.start()
            threads.append(t)
        time.sleep(13)
    for t in threads:
        t.join()
    stop.value = 1
    monitor.join()
    video_app.destroy()
    voice_app.destroy()
    network_app.destroy()
    return data


def experiment1(seq):
    manager = multiprocessing.Manager()
    data = manager.list([])
    stop = multiprocessing.Value('i', 0)
    temp_divide = multiprocessing.Value('i', 0)
    # Run application
    monitor = multiprocessing.Process(target=record_utilization,
                                      args=(data, stop, temp_divide))
    monitor.start()
    time.sleep(2)
    temp_divide.value = 1
    if seq == 1:
        camera = Applications.VideoRecorder()
        camera.turn_on(16)
        camera.destroy()
    elif seq == 2:
        camera = Applications.VideoRecorder()
        camera.turn_on_record(16)
        camera.destroy()
    elif seq == 3:
        detector = Applications.FaceDetector()
        detector.turn_on(16)
        detector.destroy()
    elif seq == 4:
        mic_recorder = Applications.VoiceRecorder()
        mic_recorder.record(16)
        mic_recorder.destroy()
    elif seq == 5:
        network_app = Applications.NetworkApplication()
        network_app.transfer()
        network_app.destroy()
    else:
        time.sleep(16)
    temp_divide.value = 1
    time.sleep(2)
    stop.value = 1
    monitor.join()
    return data


def main(experiment, sequence):
    if not os.path.isdir("test_files"):
        os.makedirs("test_files")
        Applications.NetworkApplication.generate_files()
    else:
        if len(os.listdir("test_files")) < 20:
            Applications.NetworkApplication.generate_files(
                20 - len(os.listdir("test_files")))
    if experiment == 1:
        for i in range(0, 20):
            data = experiment1(sequence)
            dump_data(data, experiment, sequence, i + 1)
    else:
        data = experiment2(sequence)
        dump_data(data, experiment, sequence, 0)


if __name__ == "__main__":
    if len(argv) < 2:
        print "Usage: python experiments.py \
        <experiment_number> <sequence_number>"
    experiment = int(argv[1])
    sequence = int(argv[2])
    main(experiment, sequence)
