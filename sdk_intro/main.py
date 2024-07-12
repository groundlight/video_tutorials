import groundlight
import cv2
from framegrab import FrameGrabber
import time

gl = groundlight.Groundlight()

detector_name = "trash_detector"
detector_query = "Is the trash can overflowing"

detector = gl.get_or_create_detector(detector_name, detector_query)

grabber = list(FrameGrabber.autodiscover().values())[0]

WAIT_TIME = 5
last_capture_time = time.time() - WAIT_TIME

while True:
    frame = grabber.grab()

    cv2.imshow('Video Feed', frame)
    key = cv2.waitKey(30)

    if key == ord('q'):
        break
    # # Press enter to submit an image query
    # elif key in (ord('\r'), ord('\n')):
    #     print(f'Asking question: {detector_query}')
    #     image_query = gl.submit_image_query(detector, frame)
    #     print(f'The answer is {image_query.result.label.value}')

    # # Press 'y' or 'n' to submit a label
    # elif key in (ord('y'), ord('n')):
    #     if key == ord('y'):
    #         label = 'YES'
    #     else:
    #         label = 'NO'
    #     image_query = gl.ask_async(detector, frame, human_review="NEVER")
    #     gl.add_label(image_query, label)
    #     print(f'Adding label {label} for image query {image_query.id}')

    # Submit image queries in a timed loop
    now = time.time()
    if last_capture_time + WAIT_TIME < now:
        last_capture_time = now

        print(f'Asking question: {detector_query}')
        image_query = gl.submit_image_query(detector, frame)
        print(f'The answer is {image_query.result.label.value}')

grabber.release()
cv2.destroyAllWindows()