import cv2

img1 = cv2.imread("images/img1.jpeg")
img2 = cv2.imread("images/img2.jpeg")

alpha = 1

img3 = cv2.addWeighted(img1, alpha, img2, 1-alpha, 0.0)

img3 = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)

cv2.imshow("ok", img3)
cv2.waitKey(0)