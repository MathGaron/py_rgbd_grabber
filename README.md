# py_rgbd_grabber
Simple python3 utility to get frames (asynchronously) from RGB-D sensors used for research. (Kinect2, Realsense)

## [Example](https://github.com/MathGaron/py_rgbd_grabber/blob/master/tests/sensor_tests.py)
```python
    # instantiate Kinect2 or Realsense
    sensor = Kinect2()
    # Inside the with statement, launch/release the sensor grabber process
    with sensor:
        # Get the list of frames grabbed (empty list if there is no new frames)
        frames = sensor.get_frames()
        # Or pop the last frame (will block until next frame)
        frame = sensor.pop_frame()
```

Frame contains an rgb numpy array [H, W, C], depth (mm) numpy array [H, W] and timestamp (s)

### Kinect2 dependencies
- [libfreenect2](https://github.com/OpenKinect/libfreenect2)
- [Bindings for libfreenect2](https://github.com/MathGaron/py3freenect2) <- (Tested only with the linked fork)

### Realsense dependencies
- [librealsense](https://github.com/IntelRealSense/librealsense#installation-guide)
- [Bindings for librealsense](https://github.com/toinsson/pyrealsense)