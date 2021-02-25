import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
from tensorflow import keras
from absl import app
from PIL import Image
import core.config as cfg
import core.utils as utils
from core.yolov4 import filter_boxes
from tensorflow.python.saved_model import tag_constants
import cv2
import numpy as np
import requests


def main(_argv):
    model = tf.saved_model.load("yolov4-416",tags=[tag_constants.SERVING])
    infer = model.signatures['serving_default']
    cam = cv2.VideoCapture("firetest.mp4")
    input_size = 416
    iou = 0.45
    score = 0.25
    x=0
    url = "http://localhost:3000/"
    data = "경남 합천군 가야면 해인사길 122".encode('utf-8')
    while True:
        return_value, frame = cam.read()
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)

        frame_size = frame.shape[:2]
        image_data = cv2.resize(frame, (input_size, input_size))
        image_data = image_data / 255.
        image_data = image_data[np.newaxis, ...].astype(np.float32)

        batch_data = tf.constant(image_data)
        pred_bbox = infer(batch_data)
        for key, value in pred_bbox.items():
            boxes = value[:, :, 0:4]
            pred_conf = value[:, :, 4:]

        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=50,
            max_total_size=50,
            iou_threshold=iou,
            score_threshold=score
        )
        pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]
        classlist = utils.read_class_names("./data/classes/obj.names")
        if(x==0):
            for i in classes.numpy()[0]:
                if(classlist[i]=="fire"):
                    x=1
                    requests.post(url,data=data)
                    print("sent")
                    break
        
        image = utils.draw_bbox(frame, pred_bbox)

        result = np.asarray(image)

        result = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        cv2.namedWindow("result", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("result", result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass