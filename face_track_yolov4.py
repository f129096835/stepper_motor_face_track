"""trt_yolo.py

This script demonstrates how to do real-time object detection with
TensorRT optimized YOLO engine.
"""

import os
import time
import argparse
import cv2
import pycuda.autoinit  # This is needed for initializing CUDA driver
import serial
from utils.yolo_classes import get_cls_dict
from utils.camera import add_camera_args, Camera
from utils.display import open_window, show_fps,  FpsCalculator
from utils.visualization import BBoxVisualization
from utils.yolo_with_plugins import TrtYOLO
import numpy as np

WINDOW_NAME = 'TRT accelerates YOLO'
COM_PORT = '/dev/ttyACM0'  
BAUD_RATES =9600


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
        '-m', '--model', type=str,   default='yolov4-tiny-3l-face-416x416',
        help=('[yolov3-tiny|yolov3|yolov3-spp|yolov4-tiny|yolov4|'
              'yolov4-csp|yolov4x-mish|yolov4-p5]-[{dimension}], where '
              '{dimension} could be either a single number (e.g. '
              '288, 416, 608) or 2 numbers, WxH (e.g. 416x256)'))
    parser.add_argument(
        '-l', '--letter_box', action='store_true',
        help='inference with letterboxed image [False]')
    parser.add_argument( '-o', '--open_image_process', type=int, default=0,
                        help='1=open_image_process, 0=close_image_process')
    parser.add_argument( '-a', '--arduino_serial', type=int, default=0,
                        help='1=open_arduino_serial, 0=close_arduino_serial')
    parser.add_argument( '-s', '--show_window', type=int, default=1,
                        help='1=open_window, 0=close_window')
    args = parser.parse_args()

    return args
args = parse_args()

def IMAGE_PROSSES(img):
            #应用高斯滤波器
            #img = cv2.GaussianBlur(img, (3, 3), 0)
             #将图像从 BGR 转换为 HSV
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            # 對明度通道應用自適應直方圖均衡化
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))  # 創建CLAHE對象
            hsv[:, :, 2] = clahe.apply(hsv[:, :, 2])  # 對明度通道應用自適應直方圖均衡化
            #将图像转换回 BGR 颜色空间
            img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

            return img

if args.category_num <= 0:
    raise SystemExit('ERROR: bad category_num (%d)!' % args.category_num)
if not os.path.isfile('yolo/%s.trt' % args.model):
    raise SystemExit('ERROR: file (yolo/%s.trt) not found!' % args.model)

cam = Camera(args)
if not cam.isOpened():
    raise SystemExit('ERROR: failed to open camera!')


"""Continuously capture images from camera and do object detection.

# Arguments
    cam: the camera instance (video source).
    trt_yolo: the TRT YOLO object detector instance.
    conf_th: confidence/score threshold for object detection.
    vis: for visualization.
"""
cls_dict = get_cls_dict(args.category_num)
max_bbox  = 0
vis = BBoxVisualization(cls_dict)
trt_yolo = TrtYOLO(args.model, args.category_num, args.letter_box)
fps = FpsCalculator()
width = args.width
height =args.height
image_prosses_switch = args.open_image_process
arduino_switch = args.arduino_serial
window_switch = args.show_window


if window_switch:
    open_window(
        WINDOW_NAME, 'Camera TensorRT YOLO',
        cam.img_width, cam.img_height)
if arduino_switch : 
    ArduinoSerial=serial.Serial(COM_PORT,BAUD_RATES)

time.sleep(2)  
start =time.time()

try:
    while True: 
        img = cam.read()
        if img is None:
            break
       
        #影像處理(開啟image_prosses適用)
        if image_prosses_switch:
            img = IMAGE_PROSSES(img)
        
        #使用TRT引擎進行物件偵測
        boxes, confs, clss = trt_yolo.detect(img, args.conf_thresh)
        
        #取出最大的BBOX
        if len(boxes)!=0:
            max=-1
            target=0
            for idx, (x_min, y_min, x_max, y_max) in enumerate(boxes):
                if ((x_max-x_min)*(y_max-y_min)) > max:
                    max = ((x_max-x_min)*(y_max-y_min))
                    target = idx
            x_min, y_min, x_max, y_max = boxes[target]
            string='X{0:d}Y{1:d}'.format(((x_min+x_max)//2),((y_min+y_max)//2))
            max_bbox =  (x_max-x_min)*(y_max-y_min)
       
        #如果最大的BBOX符合條件送出給Arduino
        if  max_bbox>=1000 and arduino_switch:  
            ArduinoSerial.write(string.encode('utf-8'))
       
        #畫出BBOX(開啟show_window適用)
        if window_switch:
            img = vis.draw_bboxes(img, boxes, confs, clss)
       
        #計算最終FPS和在終端機上印出訊息
        fps_curr = fps.update()
        print('FPS: {:.2f} Object:{:d} MAX{:d}'.format(fps_curr, len(clss), max_bbox))
        
        #顯示偵測視窗(開啟show_window適用)
        if window_switch: 
            show = show_fps(img, fps_curr)
            cv2.imshow(WINDOW_NAME,show)
            key = cv2.waitKey(1)
           
        
        max_bbox = 0 
        
except  KeyboardInterrupt:
   print('程式結束')
   cam.release()
   cv2.destroyAllWindows()

