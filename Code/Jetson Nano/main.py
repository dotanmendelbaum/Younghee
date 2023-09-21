import argparse
import time
from numpy import random
import numpy as np
import cv2
import imutils
from imutils.video import VideoStream, FPS
import serial
import playsound

def initialize_model(prototxt_path, model_path):
    print("[INFO] Loading model...")
    return cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--prototxt", required=True, help="Path to Caffe 'deploy' prototxt file")
    ap.add_argument("-m", "--model", required=True, help="Path to Caffe pre-trained model")
    ap.add_argument("-c", "--confidence", type=float, default=0.2, help="Minimum probability to filter weak detections")
    return vars(ap.parse_args())

def process_frame(frame, net, min_confidence):
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > min_confidence:
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
            if "person" in label:
                return (startX, startY, endX, endY, label)
    return (0, 0, 0, 0, "")

if __name__ == "__main__":
    args = get_args()
    net = initialize_model(args["prototxt"], args["model"])
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    fps = FPS().start()
    arduino = serial.Serial('/dev/cu.usbmodem144101', 9600)

    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor", "cup"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    # Initialize game variables
    wasShot = False
    running = False
    just_stopped = False
    last_startX, last_startY, last_endX, last_endY = 0, 0, 0, 0

    while True:
        runtime = 4
        start_time = time.time()
        running = not running
        just_stopped = not running
        sound_played = False

        while (time.time() - start_time) < runtime:
            frame = vs.read()
            frame = imutils.resize(frame, width=400)
            startX, startY, endX, endY, label = process_frame(frame, net, args["confidence"])

            if "person" in label:
                if running:
                    playsound.playsound('sound.mp3')
                    sound_played = True
                else:
                    if just_stopped:
                        last_startX, last_startY, last_endX, last_endY = startX, startY, endX, endY
                        just_stopped = False
                    else:
                        if abs(last_startX - startX) > 15 or abs(last_startY - startY) > 15 or abs(last_endX - endX) > 15 or abs(last_endY - endY) > 15:
                            if not wasShot:
                                print("loserrrrr!!!!!!")
                                arduino.write(b'4')
                                wasShot = True

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        fps.update()

    fps.stop()
    print("[INFO] Elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] Approx. FPS: {:.2f}".format(fps.fps()))

    cv2.destroyAllWindows()
    vs.stop()
