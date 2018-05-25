import cv2
import time
import pyaudio
import paramiko
import wave
import random
from os import listdir, path


class VideoRecorder:
    def __init__(self, camera=None):
        if camera is None:
            self.cap = cv2.VideoCapture(0)
        else:
            self.cap = camera

    def turn_on(self, duration=10, pause=0):
        end_time = time.time() + duration
        while time.time() < end_time:
            ret, frame = self.cap.read()
            if not ret:
                print "Error with camera: Could not get frame"
                break
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        return 0

    def turn_on_record(self, duration=10, pause=0, file_name="output.avi"):
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        outf = cv2.VideoWriter(file_name, fourcc, 20.0, (640, 480))
        end_time = time.time() + duration
        while time.time() < end_time:
            ret, frame = self.cap.read()
            if not ret:
                print "Error with video recorder: Could not get frame"
                break
            outf.write(frame)
        outf.release()
        return 0

    def hybrid(self, duration, seq):
        fcascade = cv2.CascadeClassifier("./cascade_default.xml")
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        outf = cv2.VideoWriter("output.avi", fourcc, 20.0, (640, 480))
        end_time = time.time() + duration
        while time.time() < end_time:
            ret, frame = self.cap.read()
            if not ret:
                print "Error with hybrid: Could not get frame"
                break
            if seq[1] == 1 and seq[3] != 1:
                cv2.imshow("Frame", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            elif seq[3] == 1:
                detected_faces = FaceDetector.detect(frame, fcascade)
                cv2.imshow("Frame", detected_faces)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            if seq[2] == 1:
                outf.write(frame)
        outf.release()
        cv2.destroyAllWindows()
        return 0

    def destroy(self):
        self.cap.release()
        cv2.destroyAllWindows()


class FaceDetector:
    def __init__(self, camera=None):
        self.fcascade = cv2.CascadeClassifier("./cascade_default.xml")
        if camera is None:
            self.camera = VideoRecorder()
        else:
            self.camera = camera

    def turn_on(self, duration=10, pause=0, show=True):
        end_time = time.time() + duration
        while time.time() < end_time:
            ret, frame = self.camera.read()
            faces = self.fcascade.detectMultiScale(
                cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
            )
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h),
                              (0, 255, 0), 2)
            if show:
                if not ret:
                    print "Error FaceDetector: Could not get frame"
                    break
                cv2.imshow("Frame", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        cv2.destroyAllWindows()
        return 0

    @staticmethod
    def detect(frame, cascade):
        faces = cascade.detectMultiScale(
            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y),
                          (x + w, y + h), (0, 255, 0), 2)
        return frame

    def destroy(self):
        self.camera.destroy()


class VoiceRecorder:
    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.recorder = pyaudio.PyAudio()

    def record(self, time=10):
        stream = self.recorder.open(format=self.FORMAT,
                                    channels=self.CHANNELS,
                                    rate=self.RATE,
                                    input=True,
                                    frames_per_buffer=self.CHUNK)
        frames = []
        for i in range(0, int(self.RATE/self.CHUNK * time)):
            frames.append(stream.read(self.CHUNK))
        stream.stop_stream()
        stream.close()
        wf = wave.open("output.wav", 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.recorder.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        return 0

    def destroy(self):
        self.recorder.terminate()


class NetworkApplication:
    def __init__(self):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(hostname='98.206.161.171',
                                username="odroid",
                                password="S33Codroid")

    def transfer(self):
        ftp_client = self.ssh_client.open_sftp()
        for file_name in listdir("./test_files"):
            ftp_client.put(path.join("test_files/", file_name),
                           path.join("/local/ahsanp/test_files/", file_name))
        ftp_client.close()
        return 0

    @staticmethod
    def generate_files(num=20):
        for i in range(0, num):
            size = random.randint(100 * 1024, (15 * 1024 * 1024) + 1)
            with open(path.join("test_files/", str(i)), 'wb') as f:
                f.seek(size)
                f.write("\0")
                f.close()

    def destroy(self):
        self.ssh_client.exec_command("rm -rf /local/ahsanp/test_files/*")
        self.ssh_client.close()
