from py_rgbd_grabber.kinect2 import Kinect2
from py_rgbd_grabber.realsense import Realsense
import cv2
import numpy as np
import os

from py_rgbd_grabber.video_recorder import VideoRecorder


def preprocess_function(frame):
    frame.rgb = cv2.pyrDown(frame.rgb)
    frame.depth = cv2.pyrDown(frame.depth)
    return frame

if __name__ == '__main__':
    sensor = Kinect2(preprocess_function)
    #sensor = Realsense(preprocess_function)

    save_path = "test_save"
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    # Will be better to get width and height from sensor...
    recorder = VideoRecorder(os.path.join(save_path, "video.avi"), 30, 960, 540)

    # will manage the other process automagically
    with sensor, recorder:
        # main loop
        while True:
            frames = sensor.get_frames()
            if len(frames) == 0:
                # could sleep here
                continue
            # grab the last frame
            frame = frames[-1]

            # do whatever with the frame

            # save the frame in another process
            recorder.save_frame(frame)

            # show and handle keyboard entries
            cv2.imshow("rgb", frame.rgb[:, :, ::-1])
            print(np.max(frame.depth))
            cv2.imshow("depth", (frame.depth/np.max(frame.depth)*255).astype(np.uint8))
            key = cv2.waitKey(10)
            if key == 1048603:  # ESC
                break
