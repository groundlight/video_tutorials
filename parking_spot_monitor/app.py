from framegrab import FrameGrabber, MotionDetector
import groundlight
import time

gl = groundlight.Groundlight()
detector = gl.get_detector('det_xxxxxx')

grabber = FrameGrabber.from_yaml('camera_config.yaml')[0]
motion_detector = MotionDetector(pct_threshold=1.0)

WAIT_TIME = 30

while True:
    frame = grabber.grab()
    if frame is None:
        print('Unable to capture frame')
        time.sleep(WAIT_TIME)
        continue

    motion_detected = motion_detector.motion_detected(frame)
    
    if motion_detected:
        print(f'Asking Groundlight: "{detector.query}"')
        gl.ask_async(detector, frame)
    else:
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print(f"No motion detected at {now}.")
    
    print(f'Sleeping for {WAIT_TIME} seconds...')
    time.sleep(WAIT_TIME)

grabber.release()
    