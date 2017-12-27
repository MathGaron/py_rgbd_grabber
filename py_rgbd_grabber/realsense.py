from py_rgbd_grabber.rgbd_frame import RgbdFrame
from py_rgbd_grabber.sensorbase import SensorBase
from py_rgbd_grabber.camera import Camera
import pyrealsense as pyrs
from pyrealsense import stream
# from pyrealsense.constants import rs_option

class Realsense(SensorBase):
    def initialize_(self):
        self.serv = pyrs.Service()
        fps = 30
        self.depth_stream = pyrs.stream.DepthStream(fps=fps)
        self.color_stream = pyrs.stream.ColorStream(fps=fps)
        self.device = self.serv.Device(device_id=0, streams=[self.color_stream, self.depth_stream])
        self.device.apply_ivcam_preset(0)

        #try:  # set custom gain/exposure values to obtain good depth image
        #    custom_options = [(rs_option.RS_OPTION_R200_LR_EXPOSURE, 30.0),
        #                      (rs_option.RS_OPTION_R200_LR_GAIN, 70.0)]
        #    self.device.set_device_options(*zip(*custom_options))
        #except pyrs.RealsenseError:
        #    pass  # options are not available on all devices

    def clean_(self):
        self.device.stop()
        self.serv.stop()
        self.device = None

    def intrinsics(self):
        distortion = []
        for i in range(5):
            distortion.append(self.device.colour_intrinsics.coeffs[i])
        camera = Camera((self.device.colour_intrinsics.fx, self.device.colour_intrinsics.fy),
               (self.device.colour_intrinsics.ppx, self.device.colour_intrinsics.ppy),
               (self.device.colour_intrinsics.width, self.device.colour_intrinsics.height),
               distortion)
        return camera

    def get_frame_(self):
        self.device.wait_for_frames()
        depth = self.device.depth.copy()
        # This camera is so noisy that removing values higher than 3 m may be a good thing
        depth[depth > 3000] = 0
        return RgbdFrame(self.device.color.copy(),
                         depth,
                         self.device.get_frame_timestamp(self.depth_stream.stream))
