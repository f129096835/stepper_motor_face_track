import cv2
import numpy as np
import matplotlib.pyplot as plt

#读取彩色图像
img = cv2.imread('test/dark_face/20.png')
#img = cv2.imread('test/face_test.jpg')

#应用高斯滤波器
#blurred_image = cv2.GaussianBlur(img, (3, 3), 0)

#将图像从 BGR 转换为 HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#对V通道进行直方图均衡化
hsv[:,:,2] = cv2.equalizeHist(hsv[:,:,2])

#将图像转换回 BGR 颜色空间
img_eq = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

# 显示结果
plt.subplot(3, 1, 1)
plt.hist(img.ravel(), 256, [0, 255], label="original image")
plt.subplot(3, 1, 2)
#plt.hist(blurred_image.ravel(), 256, [0, 255], label="GaussianBlur")
plt.subplot(3, 1, 3)
plt.hist(img_eq.ravel(), 256, [0, 255], label="histogram_equalization image")
plt.savefig("histogram.png")
plt.show()

cv2.imshow('Original Image', img)
cv2.imshow('Equalized Image', img_eq)
cv2.imwrite('Original_Image.jpg', img)
cv2.imwrite('Equalized_Image.jpg', img_eq)
cv2.waitKey(0)
