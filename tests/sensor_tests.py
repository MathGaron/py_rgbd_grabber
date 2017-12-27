from py_rgbd_grabber.kinect2 import Kinect2

if __name__ == '__main__':
    import cv2
    camera_parameters_path = "../py_rgbd_grabber/camera_calibration_files/Kinect2_lab_small.json"
    sensor = Kinect2(camera_parameters_path)
    sensor.start()
    while True:
        rgb, depth, timestamp = sensor.get_frame()
        cv2.imshow("test", rgb)
        cv2.waitKey(30)
        sensor.stop()