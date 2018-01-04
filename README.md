# py_rgbd_grabber
Simple python3 utility to get/save frames (asynchronously) from RGB-D sensors used for research.

Currently support two rgbd sensors:
    - Kinect2
    - Realsense


## Grab/Save [Example](https://github.com/MathGaron/py_rgbd_grabber/blob/master/tests/sensor_tests.py)
```python
    # instantiate Kinect2 or Realsense
    sensor = Kinect2()
    # instantiate the recorder
    recorder = VideoRecorder(save_path, fps, width, height)
    # Inside the with statement, launch/release the async processes
    with sensor, recorder:
        # Get the list of frames grabbed (empty list if there is no new frames)
        frames = sensor.get_frames()
        # Or pop the last frame (will block until next frame)
        frame = sensor.pop_frame()
        # Send frame to recorder
        recorder.save_frame(frame)
```

Frame contains an rgb numpy array [H, W, C], depth (mm) numpy array [H, W] and timestamp (s)

### Kinect2 dependencies
- [libfreenect2](https://github.com/OpenKinect/libfreenect2)
- [Bindings for libfreenect2](https://github.com/MathGaron/py3freenect2) <- (Tested only with the linked fork)

### Realsense dependencies
- [librealsense](https://github.com/IntelRealSense/librealsense#installation-guide)
- [Bindings for librealsense](https://github.com/toinsson/pyrealsense)

## TODO
- Recorder process could be based on a listener principle to have different recorder on the same process
- Kinect2: implement function to get intrinsics from the driver

## Contribution
Write an issue or send a pull request!