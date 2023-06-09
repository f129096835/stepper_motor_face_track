import cv2

# 读取图像
image = cv2.imread('test/371297900142265427.jpg')

# 应用高斯滤波器
blurred_image = cv2.GaussianBlur(image, (9, 9), 0)

# 显示原始图像和平滑后的图像
cv2.imshow('Original Image', image)
cv2.imshow('Blurred Image', blurred_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
