"""trt_yolo.py

This script demonstrates how to do real-time object detection with
TensorRT optimized YOLO engine.
"""

import os
import time
import argparse
from tracker.centroidtracker import CentroidTracker
import cv2
import pycuda.autoinit  # This is needed for initializing CUDA driver
from utils.yolo_classes import get_cls_dict
from utils.camera import add_camera_args, Camera
from utils.display import open_window, show_fps,  FpsCalculator, ScreenToggler, show_model_ID, show_total
from utils.visualization import BBoxVisualization
from utils.yolo_with_plugins import TrtYOLO
import numpy as np

WINDOW_NAME = 'TRT accelerates YOLO'

def parse_args():
    """Parse input arguments."""
    desc = ('Capture and display live camera video, while doing '
            'real-time object detection with TensorRT optimized '
            'YOLO model on Jetson')
    parser = argparse.ArgumentParser(description=desc)
    parser = add_camera_args(parser)
    parser.add_argument(
        '-c', '--category_num', type=int, default=1,
        help='number of object categories [80]')
    parser.add_argument(
        '-t', '--conf_thresh', type=float, default=0.5,
        help='set the detection confidence threshold')
    parser.add_argument(
        '-m', '--model', type=str,   default='yolov4-custom-face-416x416',
        help=('[yolov3-tiny|yolov3|yolov3-spp|yolov4-tiny|yolov4|'
              'yolov4-csp|yolov4x-mish|yolov4-p5]-[{dimension}], where '
              '{dimension} could be either a single number (e.g. '
              '288, 416, 608) or 2 numbers, WxH (e.g. 416x256)'))
    parser.add_argument(
        '-l', '--letter_box', action='store_true',
        help='inference with letterboxed image [False]')
    args = parser.parse_args()
    return args

args = parse_args()
if args.category_num <= 0:
    raise SystemExit('ERROR: bad category_num (%d)!' % args.category_num)
if not os.path.isfile('yolo/%s.trt' % args.model):
    raise SystemExit('ERROR: file (yolo/%s.trt) not found!' % args.model)

cam = Camera(args)
if not cam.isOpened():
    raise SystemExit('ERROR: failed to open camera!')

cls_dict = get_cls_dict(args.category_num)
vis = BBoxVisualization(cls_dict)
trt_yolo = TrtYOLO(args.model, args.category_num, args.letter_box)

open_window(
    WINDOW_NAME, 'Camera TensorRT YOLO',
    cam.img_width, cam.img_height)

scrn_toggle = ScreenToggler(WINDOW_NAME)
fps = FpsCalculator()
time.sleep(2)  
start =time.time()
width = 1280
height = 720

while True: 
    if cv2.getWindowProperty(WINDOW_NAME, 0) < 0:
        break
    img = cam.read()
    if img is None:
        break

    boxes, confs, clss = trt_yolo.detect(img, args.conf_thresh)
    img = vis.draw_bboxes_only_bbox(img, boxes)
   # calculate an exponentially decaying average of fps number
    fps_curr = fps.update()
    img = show_fps(img, fps_curr)
    img = show_total(img, len(clss))
    img = show_model_ID(img, args.model)
    cv2.imshow(WINDOW_NAME,img)
    #cv2.imshow("Enhanced Image",skin)
  
    key = cv2.waitKey(1)
    if key == 27:  # ESC key: quit program
        break
    elif key == ord('F') or key == ord('f'):  # Toggle fullscreen
        scrn_toggle.toggle()

cv2.imwrite('output.jpg', img)
cam.release()
cv2.destroyAllWindows()
