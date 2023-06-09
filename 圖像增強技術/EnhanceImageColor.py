import cv2
import numpy as np

# 读取彩色图像
img = cv2.imread('test/face_test.jpg')


# 将图像从 BGR 转换为 HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 增加饱和度
hsv[:,:,1] = hsv[:,:,1] * 1.5

# 将图像从 HSV 转换回 BGR
out = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

# 显示结果
cv2.imshow('Original Image', img)
cv2.imshow('Enhanced Image', out)
cv2.waitKey(0)
