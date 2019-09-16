import cv2

img1 = cv2.imread("img1.jpeg")
img2 = cv2.imread("img2.jpeg")

img3 = cv2.addWeighted(img1, 0.9, img2, 0.1, 0.0)

cv2.imshow("ok", img3)
cv2.waitKey(0)