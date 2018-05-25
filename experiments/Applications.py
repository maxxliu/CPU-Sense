import cv2
import time
import pyaudio
import wave


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
                break
            outf.write(frame)
        outf.release()
        return 0

    def read(self):
        return self.cap.read()

    def destroy(self):
        self.cap.release()


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
                    break
                cv2.imshow("Frame", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        cv2.destroyAllWindows()
        return 0

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
