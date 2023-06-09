import cv2
import numpy as np

# 读取图像
img = cv2.imread('test/face_test.jpg')

# 将图像从 BGR 转换为 YCbCr
ycbcr = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)

# 设置肤色区域的阈值
lower = np.array([0, 133, 77], dtype=np.uint8)
upper = np.array([255, 173, 127], dtype=np.uint8)

# 对图像进行阈值分割
mask = cv2.inRange(ycbcr, lower, upper)

# 对二值化图像进行形态学操作，以去除噪点
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
mask = cv2.erode(mask, kernel, iterations=1)
mask = cv2.dilate(mask, kernel, iterations=1)

# 将肤色区域提取出来
skin = cv2.bitwise_and(img, img, mask=mask)

# 显示结果
cv2.imshow('Original Image', img)
cv2.imshow('Skin Mask', mask)
cv2.imshow('Skin', skin)
cv2.waitKey(0)
