import abc
from enum import Enum
import time

from py_rgbd_grabber.camera import Camera
from multiprocessing import Process, Queue


class SensorMessage(Enum):
    Stop = 0


class SensorBase:
    def __init__(self, preprocess_function=None, max_buffer_size=-1):
        self.max_buffer_size = max_buffer_size
        self.preprocess_function = preprocess_function

    @abc.abstractmethod
    def initialize_(self):
        """
        Everything to initialize the sensor on the other process
        :return:
        """
        pass

    @abc.abstractmethod
    def clean_(self):
        """
        Everything to clean the sensor on the other process
        :return:
        """
        pass

    @abc.abstractmethod
    def get_intrinsics(self):
        """
        return Camera object
        :return:
        """
        pass

    @abc.abstractmethod
    def get_frame_(self):
        """
        Return a frame (single object), will run on the other process and pipe the frames to the main process
        :return:
        """
        pass

    def get_frames(self):
        """
        Return all frames processed on the other thread
        :return:
        """
        output_frames = []
        for i in range(self.frames.qsize()):
            output_frames.append(self.frames.get(block=True, timeout=None))
        return output_frames

    def pop_frame(self):
        """
        Return next frame in FIFO (Will block)
        :return:
        """
        return self.frames.get(block=True, timeout=None)

    def __enter__(self):
        self.frames = Queue(self.max_buffer_size)
        self.message_queue = Queue(10)
        self.frames.cancel_join_thread()
        self.message_queue.cancel_join_thread()
        self.worker = Process(target=self.grabber_, args=(self.frames, self.message_queue))
        self.worker.daemon = True
        self.worker.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.message_queue.put(SensorMessage.Stop)
        # TODO : hack, since the process is a deamon we dont want to terminate without cleaning...
        # Bug with Kinect2 hanging when terminating the process..
        time.sleep(1)

    def grabber_(self, frames, message_queue):
        self.initialize_()
        while True:
            frame = self.get_frame_()
            if self.preprocess_function is not None:
                frame = self.preprocess_function(frame)
            frames.put(frame)
            if message_queue.qsize():
                message = message_queue.get()
                if message == SensorMessage.Stop:
                    break
        self.clean_()

    def set_intrinsics(self, camera):
        self.camera = camera

    def set_intrinsics_from_json(self, path):
        self.camera = Camera.load_from_json(path)