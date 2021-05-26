# import packages
# from pyimagesearch.motion_detection import SingleMotionDetector
from imutils.video import VideoStream
from flask import Response, Flask, render_template
from prometheus_client import start_http_server, Gauge, generate_latest
import threading
import argparse
import datetime
import numpy as np
import cv2
import imutils
import time
import sys
import os

class SingleMotionDetector:
    def __init__(self, accumWeight=0.5):
        # store the accumulated weight factor
        self.accumWeight = accumWeight
        # initialize the background model
        self.bg = None

    def update(self, image):
        # initialize the bg model
        if self.bg is None:
            self.bg = image.copy().astype("float")
            return

        # update the bg model by accumulating weight avg
        cv2.accumulateWeighted(image, self.bg, self.accumWeight)

    def detect(self, image, tVal=25):
        # compute the absolute difference between the bg model
        # and the image passed in, the threshold the delta
        delta = cv2.absdiff(self.bg.astype("uint8"), image)
        thresh = cv2.threshold(delta, tVal, 255, cv2.THRESH_BINARY)[1]

        # Perform aseries of erosions and dilations to remove blobs
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)

        # find contours in the thresholded image and initialize the
        # minimum and maximum bounding box regions for motion
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        (minX, minY) = (np.inf, np.inf)
        (maxX, maxY) = (-np.inf, -np.inf)

        # if no contours were found, return None
        if len(cnts) == 0:
            return None

        # otherwise, loop over the contours
        for c in cnts:
            # compute the bounding box of the contour and use it to
            # update the minimum and maximum bounding box regions
            (x, y, w, h) = cv2.boundingRect(c)
            (minX, minY) = (min(minX, x), min(minY, y))
            (maxX, maxY) = (max(maxX, x + w), max(maxY, y + h))

        # otherwise, return a tuple of the thresholded image along
        # with bounding box
        return (thresh, (minX, minY, maxX, maxY))

# init the output frame and a lock to ensure thread-safe
# xchange of output frames (good for mult. clients)
outputFrame = None
lock = threading.Lock()

# keeps track of the cumulative sum of frames where motion was detected every 60 seconds
# mot_det_flag = 0
mot_det_sum = 0

# set content type for alert flag's HTTP response
CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

# grab the value we want to rotate the output frame by (Balena cloud variable)
if os.environ.get('STREAM_ROT_VAR') is not None:
    ROT_VAR = os.environ['STREAM_ROT_VAR']
else:
    ROT_VAR = None

# initialize a flask object
app = Flask(__name__)

# initialize the video stream and allow the camera sensor to warm up
vs = cv2.VideoCapture(0)
vs.set(3, 640)
vs.set(4, 480)

# vs = VideoStream(src=0).start()
time.sleep(2.0)

# Define Prometheus metrics
OPENCV_MOTIONDETECT = Gauge(
    'opencv_motiondetect',
    'Motion detected in the current frame'
)

@app.route("/")
def index():
    # return the template
    return render_template("index.html")

def detect_motion(frameCount):
    # grab global references to the video stream, output frame, and
    # lock vars
    global vs, outputFrame, lock, mot_det_sum

    #init the motion detector and total frames read
    md = SingleMotionDetector(accumWeight=0.1)
    total = 0

    # loop over frames from the video stream
    while True:
        # read the next frame from the video stream, resize it
        # convert the frame to greyscale and blur it
        ret, frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # Rotate the frame according to Balena environment variable
        # See cv2.rotate() documentation for list of values
        if ROT_VAR is not None:
            if ROT_VAR == "180":
                frame = cv2.rotate(frame, cv2.ROTATE_180)
            elif ROT_VAR == "+90":
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            elif ROT_VAR == "-90":
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # grab the current timestamp and draw it on the frame
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # if the total number of frames has reached a sufficient
        # number to construct a bg model, then continue to process
        if total > frameCount:
            # detect motion in the image
            motion = md.detect(gray)

            # check to see if motion was found in the frame
            if motion is not None:
                # unpack the tuple and draw the box
                (thresh, (minX, minY, maxX, maxY)) = motion
                cv2.rectangle(frame, (minX, minY), (maxX, maxY),
                    (0, 0, 255), 2)

                # set the alert flag, which updates the Prometheus Gauge in .../alert/
                print("Motion detected -- current cum. sum:\t", mot_det_sum)
                # mot_det_flag = 1

                # increment sum by 1 i.e. update the cumulative number of frames in which we detected motion
                mot_det_sum += 1

            # else:
            #     # reset motion detection flag
            #     # mot_det_flag = 0

        # update the background model and increment the total number
        # of frames read thus far
        md.update(gray)
        total += 1

        # acquire the lock, set the output frame, and release the lock
        with lock:
            outputFrame = frame.copy()

        time.sleep(0.06)    # sleep the camera stream for two frames

def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock

    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue

            # encode the frame is JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
            bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")


@app.route("/alert", methods=['GET'])
def alert():
    # return the response generated along with the specific media
    # return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
    # OPENCV_MOTIONDETECT.set(mot_det_flag) # this shouldn't work with the OPENCV_MOTIONDETECT being a gauge

    global mot_det_sum      # let the script make changes the variable defined outside its scope

    OPENCV_MOTIONDETECT.set(mot_det_sum)    # set gauge to value of our cumulative sum
    mot_det_sum = 0                         # reset the cumulative sum value
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# check to see if this is the main thread of execution
if __name__ == '__main__':
    # construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
        help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
        help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=32,
        help="# of frames used to construct the background model")
    args = vars(ap.parse_args())
    # start a thread that will perform motion detection
    t = threading.Thread(target=detect_motion, args=(
        args["frame_count"],))
    t.daemon = True
    t.start()
    # start the flask app
    app.run(host=args["ip"], port=args["port"], debug=True,
        threaded=True, use_reloader=False)
# release the video stream pointer
vs.release()