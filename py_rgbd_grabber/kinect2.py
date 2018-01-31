from py_rgbd_grabber.rgbd_frame import RgbdFrame
from py_rgbd_grabber.sensorbase import SensorBase
import cv2
import numpy as np


class Kinect2(SensorBase):
    def __init__(self, max_buffer_size=-1):
        super(Kinect2, self).__init__(max_buffer_size=max_buffer_size)

    def initialize_(self):
        # boostrapping code in pyfreenect2 todo: fix this...
        import pyfreenect2
        self.serial_number = pyfreenect2.getDefaultDeviceSerialNumber()
        self.device = pyfreenect2.Freenect2Device(self.serial_number)
        self.frame_listener = pyfreenect2.SyncMultiFrameListener(pyfreenect2.Frame.COLOR,
                                                                 pyfreenect2.Frame.DEPTH)

        self.device.setColorFrameListener(self.frame_listener)
        self.device.setIrAndDepthFrameListener(self.frame_listener)
        success = self.device.start()
        self.registration = pyfreenect2.Registration(self.device)
        self.buffer_rgb = np.zeros((1080, 1920, 3), dtype=np.uint8)

        return success

    def clean_(self):
        self.device.stop()

    def intrinsics(self):
        """
        TODO: implement bindings to get factory values
        ((1060.707250708333, 1058.608326305465),
        (956.354471815484, 518.9784429882449),
        (956.354471815484, 530),
      (1920, 1080))
        :return:
        """
        return self.camera

    def get_frame_(self):
        import pyfreenect2
        frames = self.frame_listener.waitForNewFrame()
        rgbFrame = frames.getFrame(pyfreenect2.Frame.COLOR)
        depthFrame = frames.getFrame(pyfreenect2.Frame.DEPTH)
        timestamp = depthFrame.getTimestamp()/10000
        (undistorted, color_registered, depth_registered) = self.registration.apply(rgbFrame=rgbFrame,
                                                                                    depthFrame=depthFrame)

        #import time
        #time_start = time.time()
        depth_frame = depth_registered.getDepthData().copy()
        rgb_frame = rgbFrame.getRGBData()

        self.buffer_rgb[:, :, 2] = rgb_frame[:, ::-1, 0]
        self.buffer_rgb[:, :, 1] = rgb_frame[:, ::-1, 1]
        self.buffer_rgb[:, :, 0] = rgb_frame[:, ::-1, 2]

        #print("Time {}".format(time_start - time.time()))

        self.frame_listener.release(frames)

        depth_frame[depth_frame == float('inf')] = 0
        depth_frame = depth_frame[:, ::-1]

        return RgbdFrame(self.buffer_rgb, depth_frame, timestamp)