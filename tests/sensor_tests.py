from py_rgbd_grabber.kinect2 import Kinect2
from py_rgbd_grabber.realsense import Realsense
import cv2
import numpy as np


def preprocess_function(frame):
    frame.rgb = cv2.pyrDown(frame.rgb)
    frame.depth = cv2.pyrDown(frame.depth)
    return frame

if __name__ == '__main__':
    sensor = Kinect2(preprocess_function)
    #sensor = Realsense()
    # will manage the other process automagically
    with sensor:

        # main loop
        while True:
            frames = sensor.get_frames()
            if len(frames) == 0:
                # could sleep here
                continue
            # grab the last frame
            frame = frames[-1]

            # show and handle keyboard entries
            cv2.imshow("rgb", frame.rgb[:, :, ::-1])
            print(np.max(frame.depth))
            cv2.imshow("depth", (frame.depth/np.max(frame.depth)*255).astype(np.uint8))
            key = cv2.waitKey(10)
            if key == 1048603:  # ESC
                break
