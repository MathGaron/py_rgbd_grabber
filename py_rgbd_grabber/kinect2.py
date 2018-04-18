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
        timestamp = depthFrame.getTimestamp() * 0.000125  # Unit 0.125 millisecond see libfreenect frame_listener.hpp
        (undistorted, color_registered, depth_registered) = self.registration.apply(rgbFrame=rgbFrame,
                                                                                    depthFrame=depthFrame)
        depth_frame = depth_registered.getDepthData()
        rgb_frame = rgbFrame.getRGBData()

        depth = depth_frame[:, ::-1].copy()
        # depth offset : https://github.com/OpenKinect/libfreenect2/issues/144
        # todo, calibrate this...
        depth += 20
        # flip x axis, and flip channels
        rgb = rgb_frame[:, ::-1, :3][:, :, ::-1].copy()

        self.frame_listener.release(frames)

        depth[depth == float('inf')] = 0

        return RgbdFrame(rgb, depth, timestamp)