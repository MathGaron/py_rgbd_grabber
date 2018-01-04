import abc
from multiprocessing import Process, Queue


class RecorderBase:
    def __init__(self, max_buffer_size=-1):
        self.max_buffer_size = max_buffer_size

    @abc.abstractmethod
    def initialize_(self):
        """
        Initialise anything in the other process
        :return:
        """
        pass

    @abc.abstractmethod
    def clean_(self):
        """
        Clean everything in the other process
        :return:
        """
        pass



    @abc.abstractmethod
    def save_frame_(self, frame):
        """
        Receive a frame and execute save code
        :return:
        """
        pass

    def save_frame(self, frame):
        self.frames.put(frame)

    def __enter__(self):
        self.frames = Queue(self.max_buffer_size)
        self.frames.cancel_join_thread()
        self.worker = Process(target=self.saver_, args=(self.frames,))
        self.worker.daemon = True
        self.worker.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.frames.put(None)

    def saver_(self, frames):
        self.initialize_()
        while True:
            frame = frames.get(block=True, timeout=None)
            if frame is None:
                break
            self.save_frame_(frame)
        self.clean_()

