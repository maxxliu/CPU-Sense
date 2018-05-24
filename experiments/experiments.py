import time
import psutil
import multiprocessing
import thread
import csv
import copy
import Applications
import cv2
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
            row = [cpu_percent[0] for cpu_percent in entry[0]]
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
    possible_sequences = [[1, 2, 3, 4],
                          [2, 3, 4],
                          [2, 4],
                          [2, 3],
                          [3],
                          [2]]
    tags = [[0] * 5]
    for i in possible_sequences[seq - 1]:
        last_tag = copy.deepcopy(tags[-1])
        last_tag[i - 1] = 1
        tags.append(last_tag)
    final_form = []
    for i in range(0, len(data)):
        for entry in data[i]:
            row = [cpu_percent for cpu_percent in entry[0]]
            row += entry[1][2:4]
            row += entry[2][0:2]
            row = tags[i] + row
            final_form.append(row)
    return final_form


def dump_data(data, experiment, sequence):
    header = []
    for i in range(0, 5):
        header.append("App" + str(i + 1))
    for i in range(0, len(psutil.cpu_percent(percpu=True))):
        header.append("CPU" + str(i + 1))
    header.append("read_bytes")
    header.append("write_bytes")
    header.append("bytes_sent")
    header.append("bytes_recv")
    if experiment == 1:
        data_consolidated = prepare_data_exp1(sequence, data)
    elif experiment == 2:
        data_consolidated = prepare_data_exp2(sequence, data)
    with open("dump.csv", "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)
        for row in data_consolidated:
            csvwriter.writerow(row)
        csvfile.close()


def get_exp2_seq(seq, video_app, fdetector, voice_app):
    if seq == 1:
        sequence = [video_app.turn_on,
                    video_app.turn_on_record,
                    fdetector.turn_on, voice_app]
    elif seq == 2:
        sequence = [video_app.turn_on_record,
                    fdetector.turn_on,
                    voice_app]
    elif seq == 3:
        sequence = [video_app.turn_on_record,
                    voice_app.record]
    elif seq == 4:
        sequence = [video_app.turn_on_record,
                    fdetector.turn_on]
    elif seq == 5:
        sequence = [fdetector.turn_on_record]
    elif seq == 6:
        sequence = [video_app.turn_on_record]
    return sequence


def experiment2(seq):
    common_camera = cv2.VideoCapture()
    video_app = Applications.VideoRecorder(camera=common_camera)
    fdetector = Applications.FaceDetector(camera=common_camera)
    voice_app = Applications.VoiceRecorder(camera=common_camera)
    sequence = get_exp2_seq(seq, video_app, fdetector, voice_app)
    times = [10]
    for i in range(0, len(sequence) - 1):
        times = [10 + 13 + times[0]] + times
    # Turn on monitor
    manager = multiprocessing.Manager()
    data = manager.list([])
    stop = multiprocessing.Value('i', 0)
    temp_divide = multiprocessing.Value('i', 0)
    monitor = multiprocessing.Process(target=record_utilization,
                                      args=(data, stop, temp_divide))
    monitor.start()
    time.sleep(2)
    for application in sequence:
        temp_divide.value = 1
        thread.start_new_thread(function=application, args=(10,))
        time.sleep(13)
    stop.value = 1
    monitor.join()
    common_camera.release()
    voice_app.destroy()
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
        camera.turn_on(3)
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
    # elif seq == 5:
    #     # Waiting on Aji to complete this application
    else:
        time.sleep(16)
    temp_divide.value = 1
    time.sleep(2)
    stop.value = 1
    monitor.join()
    return data


def main(experiment, sequence):
    if experiment == 1:
        data = experiment1(sequence)
    else:
        data = experiment2(sequence)
    dump_data(data, experiment, sequence)


if __name__ == "__main__":
    if len(argv) < 2:
        print "Usage: python experiments.py \
        <experiment_number> <sequence_number>"
    experiment = int(argv[1])
    sequence = int(argv[2])
    main(experiment, sequence)
