import pickle
import cv2
import numpy as np
import os
import sys


def findEdges(image):
    # Detect edges using Canny
    canny_output = cv2.Canny(image, 100, 200)
    # Find contours
    contours, hierarchy = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Draw contours
    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    for i in range(len(contours)):
        cv2.drawContours(drawing, contours, i, (255, 255, 255), 1, cv2.LINE_8, hierarchy, 0)
    # Show in a window
    return drawing


def pic2array(image):
    pointsList = []
    for row in range(len(image)):
        for col in range(len(image[0])):
            if image[row][col] != 0:
                pointsList.append([col, len(image)-row])
    return pointsList


#img = cv2.imread("images/penguindab3.jpeg")
#img = findEdges(img)
#img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#coordsList = np.array(pic2array(img))
#coordsList = np.transpose(coordsList)

#with open('examplePoints', 'wb') as fp:
    #pickle.dump(coordsList, fp)

