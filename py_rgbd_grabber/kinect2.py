from py_rgbd_grabber.sensorbase import SensorBase
from py_rgbd_grabber.camera import Camera
import pyfreenect2


class Kinect2(SensorBase):
    def __init__(self, camera_path):
        self.serial_number = pyfreenect2.getDefaultDeviceSerialNumber()
        self.device = pyfreenect2.Freenect2Device(self.serial_number)
        self.frame_listener = pyfreenect2.SyncMultiFrameListener(pyfreenect2.Frame.COLOR,
                                                                 pyfreenect2.Frame.IR,
                                                                 pyfreenect2.Frame.DEPTH)

        self.device.setColorFrameListener(self.frame_listener)
        self.device.setIrAndDepthFrameListener(self.frame_listener)
        self.camera = Camera.load_from_json(camera_path)

    def start(self):
        success = self.device.start()
        self.registration = pyfreenect2.Registration(self.device)
        return success

    def stop(self):
        self.device.stop()

    def intrinsics(self):
        """
        ((1060.707250708333, 1058.608326305465),
        (956.354471815484, 518.9784429882449),
        (956.354471815484, 530),
      (1920, 1080))
        :return:
        """
        return self.camera

    def get_frame(self, block=True):
        # TODO implement non blocking operation
        frames = self.frame_listener.waitForNewFrame()
        rgbFrame = frames.getFrame(pyfreenect2.Frame.COLOR)
        depthFrame = frames.getFrame(pyfreenect2.Frame.DEPTH)
        timestamp = depthFrame.getTimestamp()/10000
        (undistorted, color_registered, depth_registered) = self.registration.apply(rgbFrame=rgbFrame,
                                                                                    depthFrame=depthFrame)
        depth_frame = depth_registered.getDepthData().copy()
        rgb_frame = rgbFrame.getRGBData()[:, :, :3][:, :, ::-1].copy()
        self.frame_listener.release(frames)

        depth_frame[depth_frame == float('inf')] = 0
        return rgb_frame, depth_frame, timestamp