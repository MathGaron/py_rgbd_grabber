from py_rgbd_grabber.realsense import Realsense

from py_rgbd_grabber.kinect2 import Kinect2
import time
import cv2
import numpy as np
import os


if __name__ == '__main__':
    sensor = Kinect2()

    # will manage the other process automagically
    with sensor:
        # main loop
        while True:
            start_time = time.time()
            frame = sensor.pop_frame()

            # show and handle keyboard entries
            rgb = cv2.resize(frame.rgb, (int(frame.rgb.shape[1]/2), int(frame.rgb.shape[0]/2)))
            depth = cv2.resize(frame.depth, (int(frame.depth.shape[1]/2), int(frame.depth.shape[0]/2)))
            cv2.imshow("rgb", rgb[:, :, ::-1])
            cv2.imshow("depth", (depth/np.max(depth)*255).astype(np.uint8))
            key = cv2.waitKey(1)
            if key == 1048603:  # ESC
                break
            print("FPS : {}".format(1./(time.time() - start_time)))
