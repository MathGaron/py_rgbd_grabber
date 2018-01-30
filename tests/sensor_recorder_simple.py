from py_rgbd_grabber.realsense import Realsense

from py_rgbd_grabber.kinect2 import Kinect2
import time
import cv2
import numpy as np
import os


if __name__ == '__main__':
    sensor = Kinect2()

    save_path = "test_save"
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # will manage the other process automagically
    with sensor:
        # main loop
        while True:
            start_time = time.time()
            frame = sensor.pop_frame()
            #print("grab time : {}".format(time.time() - start_time))

            # show and handle keyboard entries
            cv2.imshow("rgb", frame.rgb[:, :, ::-1])
            cv2.imshow("depth", (frame.depth/np.max(frame.depth)*255).astype(np.uint8))
            key = cv2.waitKey(1)
            if key == 1048603:  # ESC
                break
