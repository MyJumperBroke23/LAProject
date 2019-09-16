# Basic Animation Framework

from tkinter import *
import numpy as np
import cv2


def distance(x0,x1,y0,y1):
    return ((x0-x1)**2 + (y0-y1)**2) ** 0.5

####################################
# Helper Image Functions
####################################

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


####################################
# customize these functions
####################################

def init(data):
    data.width = 800
    data.height = 800
    data.line_spacing = 80

    data.i_x = data.width/2 + data.line_spacing
    data.i_y = data.height/2
    data.j_x = data.width / 2
    data.j_y = data.height / 2 - data.line_spacing

    data.i = None
    data.i_circle = None
    data.j = None
    data.j_circle = None

    data.i_selected = False
    data.j_selected = False

    data.img = cv2.imread("penguindab3.jpeg")
    data.img = findEdges(data.img)
    data.img = cv2.cvtColor(data.img, cv2.COLOR_BGR2GRAY)

    data.coordsList = np.array(pic2array(data.img))
    data.coordsList = np.transpose(data.coordsList)

    max_val = np.max(data.coordsList)
    data.scale = 4/max_val
    data.coordsList = data.coordsList * data.scale  # CoordsList stores # of notches away from the origin

    data.mult_matrix = np.array([[1, 0],
                                [0, 1]])

    data.drawCoords = data.coordsList


def leftPressed(event, canvas, data):
    if (distance(data.i_x, event.x, data.i_y, event.y) < 4):
        data.i_selected = True
    elif (distance(data.j_x, event.x, data.j_y, event.y) < 4):
        data.j_selected = True
    pass

def leftMoved(event, canvas, data):
    if (data.i_selected):
        data.i_x = event.x
        data.i_y = event.y
        canvas.coords(data.i, data.width/2, data.height/2, event.x, event.y)
        canvas.coords(data.i_circle, event.x-4, event.y-4, event.x+4, event.y+4)
    elif (data.j_selected):
        data.j_x = event.x
        data.j_y = event.y
        canvas.coords(data.j, data.width / 2, data.height / 2, event.x, event.y)
        canvas.coords(data.j_circle, event.x - 4, event.y - 4, event.x + 4, event.y + 4)

def leftReleased(event, canvas, data):
    if (data.i_selected):
        data.i_selected = False
        i_x = (event.x - data.width/2)/data.line_spacing
        i_y = -(event.y - data.height/2)/data.line_spacing
        data.mult_matrix = np.array([[i_x, data.mult_matrix[0,1]],
                                     [i_y, data.mult_matrix[1,1]]])
        data.drawCoords = np.dot(data.mult_matrix, data.coordsList)

        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()
    elif (data.j_selected):
        data.j_selected = False
        j_x = (event.x - data.width/2)/data.line_spacing
        j_y = -(event.y - data.height/2)/data.line_spacing
        data.mult_matrix = np.array([[data.mult_matrix[0,0], j_x],
                                     [data.mult_matrix[1,0], j_y]])
        data.drawCoords = np.dot(data.mult_matrix, data.coordsList)

        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    drawGrid(canvas, data)
    drawUnitVectors(canvas, data)
    drawImage(canvas, data)

def drawGrid(canvas, data):
    w = data.width
    h = data.height
    l = data.line_spacing
    for i in range(0, w, l):
        canvas.create_line([(i, 0), (i, h)], tag='grid_line')

    # Creates all horizontal lines at intevals of 100
    for i in range(0, h, l):
        canvas.create_line([(0, i), (w, i)], tag='grid_line')

    canvas.create_line([(w/2, 0), (w/2, h)], fill="blue", width=2)  # Y Axis
    canvas.create_line([(0, h/2), (w, h/2)], fill="red", width=2)  # Y Axis

def drawUnitVectors(canvas, data):
    data.i = canvas.create_line([(data.width/2, data.height/2), (data.i_x, data.i_y)], fill="red", width=3,
                       arrow=LAST)  # I Vector
    data.i_circle = canvas.create_oval(data.i_x-4, data.i_y-4, data.i_x+4, data.i_y+4, fill="red", outline="")
    data.j = canvas.create_line([(data.width / 2, data.height / 2), (data.j_x, data.j_y)],fill="blue", width=3,
                       arrow=LAST)  # J Vector
    data.j_circle = canvas.create_oval(data.j_x-4, data.j_y-4, data.j_x+4, data.j_y+4, fill="blue", outline="")

def drawImage(canvas, data):
    for point in range(len(data.drawCoords[0])):
        x = (data.drawCoords[0, point] * data.line_spacing) + data.width/2
        y = -(data.drawCoords[1, point] * data.line_spacing) + data.height/2
        canvas.create_oval(x-1, y-1, x+1, y+1, fill="purple", outline="")


####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mouseWrapper(mouseFn, event, canvas, data):
        mouseFn(event, canvas, data)
        #redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        #redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        #canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mouseWrapper(leftPressed, event, canvas, data))
    canvas.bind("<B1-Motion>", lambda event:
                            mouseWrapper(leftMoved, event, canvas, data))
    root.bind("<B1-ButtonRelease>", lambda event:
                            mouseWrapper(leftReleased, event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(400, 200)