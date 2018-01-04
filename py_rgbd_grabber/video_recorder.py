import abc
from py_rgbd_grabber.recorderbase import RecorderBase
import cv2


class VideoRecorder(RecorderBase):
    def __init__(self, path, fps, width, height, encoding="XVID", max_buffer_size=-1):
        super(VideoRecorder, self).__init__(max_buffer_size=max_buffer_size)
        self.fps = fps
        self.path = path
        self.encoding = encoding
        self.width = width
        self.height = height
        self.encoder = None

    @abc.abstractmethod
    def initialize_(self):
        """
        Initialise anything in the other process
        :return:
        """
        fourcc = cv2.VideoWriter_fourcc(*self.encoding)
        self.encoder = cv2.VideoWriter(self.path, fourcc, self.fps,
                              (self.width, self.height))
        pass

    @abc.abstractmethod
    def clean_(self):
        """
        Clean everything in the other process
        :return:
        """
        self.encoder.release()

    @abc.abstractmethod
    def save_frame_(self, frame):
        """
        Receive a frame and execute save code
        :return:
        """
        self.encoder.write(frame)

