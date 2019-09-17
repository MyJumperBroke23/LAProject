import cv2
import matplotlib.pyplot as plt
import numpy as np
import math


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


def showPlot():
    img = cv2.imread("images/penguindab3.jpeg")
    img = findEdges(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    coordsList = np.array(pic2array(img))
    coordsList = np.transpose(coordsList)

    colors = (0,1,0)
    colors2 = (1,0,0)

    ROTATION = math.radians(90)  # How much to rotate clockwise in degrees

    r_matrix = np.array([[math.cos(ROTATION), -math.sin(ROTATION)],
                        [math.sin(ROTATION), math.cos(ROTATION)]])

    SHEAR = 1.2

    r_matrix = np.array([[1, 0],
                         [0, 1]])

    coords_new = np.dot(r_matrix, coordsList)

    plt.scatter(coordsList[0], coordsList[1], s=1, c=colors2, alpha=0.5)
    plt.scatter(coords_new[0], coords_new[1], s=1, c=colors, alpha=0.5)
    plt.title('Can')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()