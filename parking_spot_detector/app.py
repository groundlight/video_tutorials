from framegrab import FrameGrabber, MotionDetector
import groundlight
import time
import os
import logging

logger = logging.getLogger(__name__)

yaml_path = './camera_config.yaml'
grabber = FrameGrabber.from_yaml(yaml_path)[0]

motion_detector = MotionDetector(pct_threshold=0.5)

gl = groundlight.Groundlight()
detector = gl.get_detector('det_xxxxxx')

def get_seconds_since_midnight(t: time.struct_time) -> int:
    return t.tm_hour * 3600 + t.tm_min * 60 + t.tm_sec

WAIT_TIME = 30
START = time.struct_time((0, 0, 0, 7, 0, 0, 0, 0 , 0))
END = time.struct_time((0, 0, 0, 21, 30, 0, 0, 0 , 0))

START_SECONDS = get_seconds_since_midnight(START)
END_SECONDS = get_seconds_since_midnight(END)

def is_operating_hours(now: time.struct_time) -> bool:
    now_seconds = get_seconds_since_midnight(now)
    return START_SECONDS < now_seconds < END_SECONDS

def main():
    motion_detected, motion_detected_prev = False, False
    while True:
        now = time.localtime()
        now_str = time.strftime('%Y-%m-%d %H:%M:%S', now)

        if not is_operating_hours(now):
            logger.info(f'The current time ({now_str}) is not within the operating hours.')
        else:
            frame = grabber.grab()
            if frame is None:
                logger.error('Unable to capture frame')
                return

            motion_detected_prev = motion_detected
            motion_detected = motion_detector.motion_detected(frame)
            if motion_detected or motion_detected_prev:
                logger.info(f'motion_detected: {motion_detected} | motion_detected_previous: {motion_detected_prev}')
                iq = gl.ask_async(detector, frame)
                logger.info(f'Asking Groundlight: "{detector.query}". iq_id: {iq.id}')
            else:
                logger.info(f"No motion detected at {now_str}.")

        logger.info(f'Sleeping for {WAIT_TIME} seconds...')
        time.sleep(WAIT_TIME)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        grabber.release()
    
