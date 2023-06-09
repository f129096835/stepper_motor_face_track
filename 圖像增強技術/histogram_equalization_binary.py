import cv2
import numpy as np
import matplotlib.pyplot as plt

#读取彩色图像
img = cv2.imread('test/test10.jpg')
#img = cv2.imread('test/face_test.jpg')

#转换为灰度图像
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 应用直方图均衡化
equalized_image = cv2.equalizeHist(gray_image)

# 显示结果
plt.subplot(2, 1, 1)
plt.hist(img.ravel(), 256, [0, 255], label="original image")
plt.subplot(2, 1, 2)
plt.hist(equalized_image.ravel(), 256, [0, 255], label="histogram_equalization image")
plt.savefig("histogram.png")
plt.show()

cv2.imshow('Original Image', img)
cv2.imshow('Equalized Image', equalized_image)
cv2.imwrite('Original_Image.jpg', img)
cv2.imwrite('Equalized_Image.jpg', equalized_image)
cv2.waitKey(0)
