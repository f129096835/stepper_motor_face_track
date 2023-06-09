import cv2
import numpy as np

# 读取彩色图像
img = cv2.imread('test/face_test.jpg')

# 对比度增强
a = np.min(img)
b = np.max(img)
c = 0
d = 255
out = np.uint8((img - a) * ((d-c)/(b-a)) + c)

# 显示结果
cv2.imshow('Original Image', img)
cv2.imshow('Enhanced Image', out)
cv2.waitKey(0)