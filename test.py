import math
from tkinter import *
import random
import time
import copy
import numpy


# Copyright © 2005-2018, NumPy Developers.
# All rights reserved.
# almostEqual and animation framework from http://www.cs.cmu.edu/~112n18/
def almostEqual(d1, d2, epsilon=10 ** -8):
    return (abs(d1 - d2) < epsilon)


def distance(x0, x1, y0, y1):
    return ((x0 - x1) ** 2 + (y0 - y1) ** 2) ** 0.5


# Idea for shooter gotten from: https://www.youtube.com/watch?v=GOFws_hhZs8

class Basketball(object):
    def __init__(self, cx, cy, r):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.vx = 0
        self.vy = 0
        self.gravity = 0
        self.airFriction = 0.05
        self.fitness = 300

    def isCollisionWithNode(self, node, data):
        if not (isinstance(node, Node)):
            return False
        distanceBetween = distance(self.cx, node.cx, self.cy, node.cy)
        if (distanceBetween < self.r + node.r):
            if (data.stage == 0):
                self.fitness = 0
        return distanceBetween < self.r + node.r

    def transferMomentum(self, node, data):
        if self.isCollisionWithNode(node, data):
            self.vx = node.vx
            self.vy = node.vy
            self.gravity = 0.5

    def addFitness(self, data):
        if (data.stage == 0):
            allTouchingGround = True
            for node in data.shoot1.nodeList:
                distList = []
                distList.append(distance(self.cx, node.cx, self.cy, node.cy))
                # print(distance)
            for node in data.shoot1.nodeList:
                if not (node.isTouchingGround(data)):
                    allTouchingGround = False
            if (allTouchingGround == True):
                return
            closest = min(distList)
            closest -= (self.r + 10)
            store = self.fitness
            self.fitness = min(closest, store, 300)
            self.fitness = max(self.fitness, 0)
        elif (data.stage == 1):
            d = data.distance * 80
            currDist = distance(self.cx, d - 130, self.cy, 190)
            store = self.fitness
            self.fitness = min(currDist, store)

    def isTouchingGround(self, data):
        if (self.cy + self.r / 2 >= data.height - 40):
            return True

    def pushOffGround(self, data):
        if (self.isTouchingGround(data)):
            self.vy = -self.vy * 0.7

    def onTimerFired(self, data):
        for node in data.shoot1.nodeList:
            self.transferMomentum(node, data)
        self.bounceOff(data)
        airFriction = self.airFriction
        self.vy += self.gravity
        if (self.vx < 0):
            self.vx += airFriction
        elif (self.vx > 0):
            self.vx -= airFriction
        if (self.vy < 0):
            self.vy += airFriction
        elif (self.vy > 0):
            self.vy -= airFriction
        self.cx += self.vx
        self.cy += self.vy
        if (self.isTouchingGround(data)):
            self.cy = data.height - 40 - (self.r / 2)
            self.pushOffGround(data)
        self.addFitness(data)

    def stop(self):
        self.vx = 0
        self.vy = 0

    def bounceOff(self, data):
        if (self.cx - self.r <= 0):
            self.cx = self.r
        d = data.distance * 80
        if (self.cx + self.r >= d - 50):
            if (self.cy > 190):
                self.cx = d - 50 - self.r
                self.vx = -self.vx * 0.5
                # print(self.vx)
        # canvas.create_line(d - 50, 190, d - 50, 370)

        if (self.cx + self.r >= d - 100 and self.cx - self.r <= d - 100):
            if (self.cy <= 170 and self.cy >= 90):
                self.vx = -self.vx * 0.5
                self.cx += self.vx
        # canvas.create_line(d - 100, 170, d - 100, 90)

        if ((self.cx + self.r >= d - 110) and self.cx - self.r <= d - 110):
            if (self.cy - self.r < 190 and self.cy + self.r > 150):
                self.vx = -self.vx * 0.5
                if (self.cy > 190):
                    # print("Happens")
                    self.vy = -self.vy * 0.5
                self.cx += self.vx
                self.vy += self.vy
        # canvas.create_line(d - 110, 150, d - 110, 190)

        if (self.cx + self.r >= d - 150 and self.cx - self.r <= d - 150):
            if (self.cy - self.r < 190 and self.cy + self.r > 150):
                self.vx = -self.vx * 0.5
                if (self.cy > 190):
                    self.vy = -self.vy * 0.5
                self.cx += self.vx
                self.vy += self.vy
        # canvas.create_line(d - 150, 150, d - 150, 190)

    def draw(self, canvas):
        r = self.r
        canvas.create_oval(self.cx - r, self.cy - r, self.cx + r,
                           self.cy + r, fill="red")


class Node(object):
    '''
    def __init__(self, connectionsList, cx, cy, name, friction = 0):
        self.connectionsList = connectionsList
        self.cx = cx
        self.cy = cy
        self.friction = friction
        self.r = 10
        self.name = name
        self.vx = 0
        self.vy = 0
        self.gravity = 0.3
        self.airFriction = 0.1
        '''

    def __init__(self, connectionsList, cxW, cxB, cyW, cyB, frictionW, frictionB, distance):
        self.connectionsList = connectionsList
        self.friction = frictionW * distance + frictionB
        self.cx = cxW * distance + cxB
        self.cy = cyW * distance + cyB
        self.cxW = cxW
        self.cxB = cxB
        self.cyW = cyW
        self.cyB = cyB
        self.frictionW = frictionW
        self.frictionB = frictionB
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.gravity = 0.3
        self.airFriction = 0.1
        if (self.friction < 0):
            self.friction = 0
        elif (self.friction > 1):
            self.friction = 1

    def distanceBetweenNodes(self, other):
        if not (isinstance(other, Node)):
            return None
        else:
            return math.sqrt((self.cx - other.cx) ** 2
                             + (self.cy - other.cy) ** 2)

    def walls(self, data):
        if (self.cx < 10):
            self.cx = 10
        if (self.cx > (data.distance * 80) - 150):
            self.cx = (data.distance * 80) - 150

    def draw(self, canvas):
        r = self.r
        canvas.create_oval(self.cx - r, self.cy - r, self.cx + r,
                           self.cy + r, fill="green2")

    def __repr__(self):
        return "%f, %f, %f, %f" % (self.cx, self.cy, self.vx, self.vy)

    def speedCap(self):
        if (self.vx >= 10):
            self.vx = 10
        if (self.vx <= -10):
            self.vx = -10
        if (self.vy >= 10):
            self.vy = 10
        if (self.vy <= -10):
            self.vy = -10

    def onTimerFired(self, data):
        # self.speedCap()
        airFriction = self.airFriction
        self.cx += self.vx
        self.cy += self.vy
        if (self.cy + self.r < data.height - 30):
            self.vy += self.gravity
            self.cy += self.vy
        if (self.isTouchingGround(data)):
            self.cy = data.height - 30 - (self.r / 2)
            self.pushOffGround(data)
        if (self.vx < 0):
            self.vx += airFriction
        elif (self.vx > 0):
            self.vx -= airFriction
        if (self.vy < 0):
            self.vy += airFriction
        elif (self.vy > 0):
            self.vy -= airFriction
        self.walls(data)
        # print("%s, %f, %f, %f, %f" %(self.name, self.cx, self.cy, self.vx, self.vy))

    def isTouchingGround(self, data):
        if (self.cy + self.r / 2 >= data.height - 35):
            return True

    def pushOffGround(self, data):
        if (self.isTouchingGround(data)):
            if self.vy <= 2:
                self.vy = 0
            else:
                self.vy = -self.vy * 0.7
            # self.vy = 0
        else:
            return


def getCircleAngle(cx0, cy0, cx1, cy1):
    if (cx0 - cx1 == 0):
        return math.pi / 2
    # if (cx0 < cx1 and cy0 < cy1):
    else:
        return (math.pi * 2) - math.atan2(cy1 - cy0, cx1 - cx0)


def newRandNode(nodeList, distance):
    cxW = numpy.random.randn()
    cyW = numpy.random.randn()
    cxB = random.randint(10, 100)
    cyB = random.randint(250, 370)
    frictionW = numpy.random.randn()
    frictionB = random.random()
    # return Node([], cxW, cxB, cyW, cyB, frictionW, frictionB, distance)
    nodeList.append(Node([], cxW, cxB, cyW, cyB, frictionW, frictionB, distance))


def mutateNode(node, distance):
    chance = random.randint(1, 4)
    if chance == 1:
        node.cxW += numpy.random.randn() / 10
    elif chance == 2:
        node.cxW += numpy.random.randn() / 5
    chance = random.randint(1, 4)
    if chance == 1:
        node.cxB += numpy.random.randn() / 10
    elif chance == 2:
        node.cxB += numpy.random.randn() / 5
    chance = random.randint(1, 4)
    if chance == 1:
        node.cyW += numpy.random.randn() / 10
    elif chance == 2:
        node.cyW += numpy.random.randn() / 5
    chance = random.randint(1, 4)
    if chance == 1:
        node.cyB += numpy.random.randn() / 10
    elif chance == 2:
        node.cyB += numpy.random.randn() / 5
    chance = random.randint(1, 4)
    if chance == 1:
        node.frictionW += numpy.random.randn() / 10
    elif chance == 2:
        node.frictionW += numpy.random.randn() / 5
    chance = random.randint(1, 4)
    if chance == 1:
        node.frictionB += numpy.random.randn() / 10
    elif chance == 2:
        node.frictionB += numpy.random.randn() / 5
    node.friction = node.frictionW * distance + node.frictionB
    node.cx = node.cxW * distance + node.cxB
    node.cy = node.cyW * distance + node.cyB
    if (node.friction < 0):
        node.friction = 0
    elif (node.friction > 1):
        node.friction = 1


class Muscle(object):
    # Pulls two nodes together by strength amount every certain amount of time as long as nodes are farther apart than minLength
    '''
    def __init__(self, node1, node2, strength, minLength,
                timer, contractionLength, maxLength, timer2,
                eccentricLength):
        self.node1 = node1
        self.node2 = node2
        self.strength = strength / 5
        self.length = node1.distanceBetweenNodes(node2)
        self.minLength = minLength
        self.maxLength = maxLength
        self.timer = timer
        self.contractionLength = contractionLength
        self.contractionStore = contractionLength
        self.isContracting = False
        self.isPushing = False
        self.timer2 = timer2
        self.eccentricLength = eccentricLength
        self.eccentricStore = eccentricLength
    '''

    def __init__(self, node1, node2, strengthW, strengthB, minLengthW,
                 minLengthB, timerW, timerB, contractionLengthW,
                 contractionLengthB, maxLengthW, maxLengthB, timer2W, timer2B,
                 eccentricLengthW, eccentricLengthB, distance):
        self.node1 = node1
        self.node2 = node2
        self.node1.connectionsList.append(self.node2)
        self.node2.connectionsList.append(self.node1)
        self.strength = abs(distance * strengthW + strengthB)
        self.length = node1.distanceBetweenNodes(node2)
        self.minLength = abs(distance * minLengthW + minLengthB)
        self.maxLength = abs(distance * maxLengthW + maxLengthB) * 3 + self.minLength
        self.contractionLength = (abs(distance * contractionLengthW + contractionLengthB) // 2) + 1
        self.timer = (abs(distance * timerW + timerB) // 1) + self.contractionLength
        self.contractionStore = self.contractionLength
        self.isContracting = False
        self.isPushing = False
        self.eccentricLength = (abs(distance * eccentricLengthW + eccentricLengthB) // 1) + 1
        self.timer2 = (abs(distance * timer2W + timer2B) // 1) + self.eccentricLength
        self.eccentricStore = self.eccentricLength
        self.strengthW, self.strengthB = strengthW, strengthB
        self.minLengthW, self.minLengthB = minLengthW, minLengthB
        self.timerW, self.timerB = timerW, timerB
        self.contractionLengthW, self.contractionLengthB = contractionLengthW, contractionLengthB
        self.maxLengthW, self.maxLengthB = maxLengthW, maxLengthB
        self.timer2W, self.timer2B = timer2W, timer2B
        self.eccentricLengthW, self.eccentricLengthB = eccentricLengthW, eccentricLengthB
        # print(self.node1.friction)

    def pullHelper(self, tempStrength=0):
        if tempStrength == 0:
            tempStrength = self.strength / 5
            if (self.length < self.minLength + self.strength):
                tempStrength = (self.length - self.minLength) / 2
        angle = getCircleAngle(self.node1.cx, self.node1.cy,
                               self.node2.cx, self.node2.cy)
        # print((angle / math.pi) * 180)
        dx1 = math.cos(angle) * tempStrength
        if (almostEqual(dx1, 0)): dx1 = 0
        dy1 = -(math.sin(angle) * tempStrength)
        if (almostEqual(dy1, 0)): dy1 = 0
        # print(dy1)
        dx2, dy2 = -dx1, -dy1
        self.node1.vx += dx1
        self.node2.vx += dx2
        self.node1.vy += dy1
        self.node2.vy += dy2
        # print(dx2, self.node2.vx, self.node1.vx)
        self.length = self.node1.distanceBetweenNodes(self.node2)

    def pull(self, data):
        # print("pull")
        if ((data.counter % self.timer == 0) and self.contractionLength != 0):
            self.isContracting = True
            self.contractionStore = self.contractionLength
        if (self.isContracting):
            self.contractionStore -= 1
            if (self.contractionStore == 0):
                self.isContracting = False
            if (self.length > self.minLength):
                tempStrength = self.strength / 2
                if (self.length < self.minLength + self.strength):
                    tempStrength = (self.length - self.minLength) / 2
                angle = getCircleAngle(self.node1.cx, self.node1.cy,
                                       self.node2.cx, self.node2.cy)
                # print((angle / math.pi) * 180)
                dx1 = math.cos(angle) * tempStrength
                if (almostEqual(dx1, 0)): dx1 = 0
                dy1 = -(math.sin(angle) * tempStrength)
                if (almostEqual(dy1, 0)): dy1 = 0
                # print(dy1)
                dx2, dy2 = -dx1, -dy1
                self.node1.vx += dx1
                self.node2.vx += dx2
                self.node1.vy += dy1
                self.node2.vy += dy2
                self.length = self.node1.distanceBetweenNodes(self.node2)

    def pushHelper(self, tempStrength=0):
        # print("Push")
        if tempStrength == 0:
            tempStrength = self.strength / 5
            if (self.length > self.maxLength - self.strength):
                tempStrength = (self.maxLength - self.length) / 2
        angle = getCircleAngle(self.node1.cx, self.node1.cy,
                               self.node2.cx, self.node2.cy)
        # print((angle / math.pi) * 180)
        dx1 = math.cos(angle) * tempStrength
        if (almostEqual(dx1, 0)): dx1 = 0
        dy1 = -(math.sin(angle) * tempStrength)
        if (almostEqual(dy1, 0)): dy1 = 0
        # print(dy1)
        dx2, dy2 = -dx1, -dy1
        self.node1.vx -= dx1
        self.node2.vx -= dx2
        self.node1.vy -= dy1
        self.node2.vy -= dy2
        # print("Happens", dx1, dy1)
        self.length = self.node1.distanceBetweenNodes(self.node2)

    def push(self, data):
        if ((data.counter % self.timer2 == 0) and self.eccentricLength != 0):
            self.isPushing = True
            self.eccentricStore = self.eccentricLength
        if (self.isPushing):
            self.eccentricStore -= 1
            if (self.eccentricStore == 0):
                self.isPushing = False
            if (self.length < self.maxLength):
                tempStrength = self.strength / 5
                if (self.length > self.maxLength - self.strength):
                    tempStrength = (self.maxLength - self.length) / 2
                angle = getCircleAngle(self.node1.cx, self.node1.cy,
                                       self.node2.cx, self.node2.cy)
                # print((angle / math.pi) * 180)
                dx1 = math.cos(angle) * tempStrength
                if (almostEqual(dx1, 0)): dx1 = 0
                dy1 = -(math.sin(angle) * tempStrength)
                if (almostEqual(dy1, 0)): dy1 = 0
                # print(dy1)
                dx2, dy2 = -dx1, -dy1
                self.node1.vx -= dx1
                self.node2.vx -= dx2
                self.node1.vy -= dy1
                self.node2.vy -= dy2
                self.length = self.node1.distanceBetweenNodes(self.node2)

    def keepLength(self, data):
        tooLong = 0
        self.length = self.node1.distanceBetweenNodes(self.node2)
        tempLength = self.length
        while ((tempLength > self.maxLength) and (tooLong <= 100)):
            self.pullHelper(0.01)
            # print(self.length, self.maxLength)
            tooLong += 1
            tempLength = distance(self.node1.cx + self.node1.vx, self.node2.cx + self.node2.vx,
                                  self.node1.cy + self.node1.vy, self.node2.cy + self.node2.vy)
        # print(self.length, self.maxLength, self.node2.vy)
        while ((self.length < self.minLength) and (tooLong <= 100)):
            self.pushHelper(0.01)
            tooLong += 1
            tempLength = distance(self.node1.cx + self.node1.vx, self.node2.cx + self.node2.vx,
                                  self.node1.cy + self.node1.vy, self.node2.cy + self.node2.vy)
            # print("2")
            # print(self.length, self.minLength)

    def nodeFriction(self, data):
        if (self.node1.isTouchingGround(data)):
            if ((self.isPushing == True) or (self.isContracting == True)):
                self.node1.vx -= self.node1.vx * self.node1.friction
        if (self.node2.isTouchingGround(data)):
            if ((self.isPushing == True) or (self.isContracting == True)):
                self.node2.vx -= self.node2.vx * self.node2.friction

    def __eq__(self, other):
        if not (isinstance(other, Muscle)):
            return False
        else:
            return (self.node1 == other.node1) and (self.node2 == other.node2)

    def draw(self, canvas):
        canvas.create_line(self.node1.cx, self.node1.cy, self.node2.cx,
                           self.node2.cy)


# strengthW, strengthB, minLengthW, minLengthB, timerW, timerB, contractionLengthW, contractionLengthB, maxLengthW, maxLengthB, timer2W, timer2B, eccentricLengthW, eccentricLengthB

def newRandMuscle(nodeList, muscleList, distance):
    node1 = random.choice(nodeList)
    node2 = random.choice(nodeList)
    while (node1 == node2):
        node2 = random.choice(nodeList)
    strengthW = numpy.random.randn()
    strengthB = numpy.random.randn()
    minLengthW = numpy.random.randn()
    minLengthB = numpy.random.randn()
    maxLengthW = numpy.random.randn()
    maxLengthB = numpy.random.randn()
    timerW = numpy.random.randn()
    timerB = numpy.random.randn()
    contractionLengthW = numpy.random.randn()
    contractionLengthB = numpy.random.randn()
    timer2W = numpy.random.randn()
    timer2B = numpy.random.randn()
    eccentricLengthW = numpy.random.randn()
    eccentricLengthB = numpy.random.randn()
    muscleList.append(Muscle(node1, node2, strengthW, strengthB, minLengthW, minLengthB,
                             timerW, timerB, contractionLengthW, contractionLengthB,
                             maxLengthW, maxLengthB, timer2W, timer2B, eccentricLengthW,
                             eccentricLengthB, distance))


def mutateMuscle(muscle, distance):
    chance = random.randint(1, 10)
    if chance == 1:
        muscle.strengthW += numpy.random.randn() / 15
    elif chance == 2:
        muscle.strengthW += numpy.random.randn() / 10
    chance = random.randint(1, 10)
    if chance == 1:
        muscle.strengthB += numpy.random.randn() / 15
    elif chance == 2:
        muscle.strengthB += numpy.random.randn() / 10
    chance = random.randint(1, 10)
    if chance == 1:
        muscle.minLengthW += numpy.random.randn() / 15
    elif chance == 2:
        muscle.minLengthW += numpy.random.randn() / 10
    chance = random.randint(1, 10)
    if chance == 1:
        muscle.minLengthB += numpy.random.randn() / 15
    elif chance == 2:
        muscle.minLengthB += numpy.random.randn() / 10
    chance = random.randint(1, 10)
    if chance == 1:
        muscle.maxLengthW += numpy.random.randn() / 15
    elif chance == 2:
        muscle.maxLengthW += numpy.random.randn() / 10
    chance = random.randint(1, 10)
    if chance == 1:
        muscle.maxLengthB += numpy.random.randn() / 15
    elif chance == 2:
        muscle.maxLengthB += numpy.random.randn() / 10
    chance = random.randint(1, 10)
    if chance == 1:
        muscle.timerW += numpy.random.randn() / 30
    elif chance == 2:
        muscle.timerW += numpy.random.randn() / 10
    chance = random.randint(1, 10)
    if chance == 1:
        muscle.timerB += numpy.random.randn() / 15
    elif chance == 2:
        muscle.timerB += numpy.random.randn() / 10
    chance = random.randint(1, 10)
    if chance == 1:
        muscle.contractionLengthW += numpy.random.randn() / 15
    elif chance == 2:
        muscle.contractionLengthW += numpy.random.randn() / 10
    chance = random.randint(1, 10)
    if chance == 1:
        muscle.contractionLengthB += numpy.random.randn() / 15
    elif chance == 2:
        muscle.contractionLengthB += numpy.random.randn() / 10
    chance = random.randint(1, 10)
    if chance == 1:
        muscle.timer2W += numpy.random.randn() / 15
    elif chance == 2:
        muscle.timer2W += numpy.random.randn() / 10
    chance = random.randint(1, 10)
    if chance == 1:
        muscle.timer2B += numpy.random.randn() / 15
    elif chance == 2:
        muscle.timer2B += numpy.random.randn() / 10
    chance = random.randint(1, 10)
    if chance == 1:
        muscle.eccentricLengthW += numpy.random.randn() / 15
    elif chance == 2:
        muscle.eccentricLengthW += numpy.random.randn() / 10
    chance = random.randint(1, 10)
    if chance == 1:
        muscle.eccentricLengthB += numpy.random.randn() / 15
    elif chance == 2:
        muscle.eccentricLengthB += numpy.random.randn() / 10
    muscle.strength = abs(distance * muscle.strengthW + muscle.strengthB)
    muscle.length = muscle.node1.distanceBetweenNodes(muscle.node2)
    muscle.minLength = abs(distance * muscle.minLengthW + muscle.minLengthB)
    muscle.maxLength = abs(distance * muscle.maxLengthW + muscle.maxLengthB) * 3 + muscle.minLength
    muscle.contractionLength = (abs(distance * muscle.contractionLengthW + muscle.contractionLengthB
                                    ) // 2) + 1
    muscle.timer = (abs(distance * muscle.timerW + muscle.timerB) // 1) + muscle.contractionLength
    muscle.eccentricLength = (abs(distance * muscle.eccentricLengthW + muscle.eccentricLengthB) // 1) + 1
    muscle.timer2 = (abs(distance * muscle.timer2W + muscle.timer2B) // 1) + muscle.eccentricLength


class Shooter(object):
    def __init__(self, nodeList, muscleList):
        self.nodeList = nodeList
        self.muscleList = muscleList
        self.gravity = 0.5

    def draw(self, canvas):
        for node in self.nodeList:
            node.draw(canvas)
        for muscle in self.muscleList:
            muscle.draw(canvas)

    def onTimerFired(self, data):
        for muscle in self.muscleList:
            muscle.pull(data)
            muscle.push(data)
            muscle.keepLength(data)
            muscle.nodeFriction(data)
        for node in self.nodeList:
            node.onTimerFired(data)

    def stop(self):
        for node in self.nodeList:
            node.vx = 0
            node.vy = 0


def removeDeadNodes(shoot1):
    keepList = []
    for muscle in (shoot1.muscleList):
        keepList.append(muscle.node1)
        keepList.append(muscle.node2)
    for node in shoot1.nodeList:
        if node not in keepList:
            shoot1.nodeList.remove(node)


def newRandShooter(shooterList, distance):
    nodeList = []
    muscleList = []
    numNodes = random.randint(3, 6)
    numMuscles = random.randint(1, 6)
    for node in range(numNodes):
        newRandNode(nodeList, distance)
    for muscle in range(numMuscles):
        newRandMuscle(nodeList, muscleList, distance)
        for muscle2 in range(len(muscleList) - 2):
            if ((muscleList[muscle2] == muscleList[len(muscleList) - 1]) and len(muscleList) != 1):
                muscleList.pop()
    shoot1 = Shooter(nodeList, muscleList)
    removeDeadNodes(shoot1)
    shooterList.append(shoot1)


def generateAll(shooterList, ballList, popSize, distance):
    for i in range(popSize):
        newRandShooter(shooterList, distance)
        ballList.append(Basketball(130, 325, 15))


def newBaskets(popSize, ballList):
    ballList.clear()
    for i in range(popSize):
        ballList.append(Basketball(130, 325, 15))


def mutateShooter(shooter, distance):
    # print (shooter)
    for node in shooter.nodeList:
        mutateNode(node, distance)
    for muscle in shooter.muscleList:
        mutateMuscle(muscle, distance)


def indexOfLeastFit(ballList):
    pos = 0
    leastFit = -9999999
    for i in range(len(ballList)):
        # print(i, ballList[i].fitness)
        if (ballList[i].fitness > leastFit):
            leastFit = ballList[i].fitness
            pos = i
    ballList.pop(pos)
    return pos


def getMostFit(shooterList, ballList, distance):
    newList = copy.deepcopy(shooterList)
    for i in range(len(newList) // 2):
        pos = indexOfLeastFit(ballList)
        # print(pos)
        newList.pop(pos)
    newListCopy = []
    for shooter in newList:
        shooterCopy = copy.deepcopy(shooter)
        newListCopy.append(shooterCopy)
    newList.extend(newListCopy)
    # print(newList)
    for shooter in range(len(newList) // 2):
        mutateShooter(newList[shooter], distance)
        # print("Mutating " + str(shooter))
        # for node in newList[shooter].nodeList:
        # print(node.cx, node.cy)
    # for shooter in range(len(newList) //2, len(newList)):
    # print("Original " + str(shooter))
    # for node in newList[shooter].nodeList:
    # print(node.cx, node.cy)
    # newList.pop(len(newList) - 1)
    # newRandShooter(newList, distance)
    return newList


def getAverageFitness(ballList):
    fitTotal = 0
    for ball in ballList:
        fitTotal += ball.fitness
    return fitTotal / len(ballList)


def numZeros(ballList):
    zeros = 0
    for ball in ballList:
        if ball.fitness <= 0:
            zeros += 1
    return zeros


def fittestBall(ballList):
    fittest = None
    for ball in ballList:
        if fittest == None or ball.fitness < fittest:
            fittest = ball.fitness
    return fittest


def leastFit(ballList):
    unfittest = None
    for ball in ballList:
        if unfittest == None or ball.fitness > unfittest:
            unfittest = ball.fitness
    return unfittest


def leastFitEver(minFit):
    unfittest = None
    for elem in minFit:
        if (unfittest == None or elem > unfittest):
            unfittest = elem
    return unfittest


def makeGraphs(canvas, data):
    # graph start at 20, 300, goes on for 170, starts at 210, 300, goes on for 170
    canvas.create_line(20, 130, 20, 300)
    canvas.create_line(20, 300, 190, 300)
    canvas.create_line(210, 130, 210, 300)
    canvas.create_line(210, 300, 390, 300)
    leastFE = leastFitEver(data.minFit)
    if len(data.minFit) > 1:
        xScale = 170 // (len(data.minFit) - 1)
        for minVal in range(len(data.minFit) - 1):
            xVal = 20 + xScale * minVal
            xVal2 = xVal + xScale
            yVal = 300 - (170 * data.minFit[minVal] / leastFE)
            yVal2 = 300 - (170 * data.minFit[minVal + 1] / leastFE)
            canvas.create_line(xVal, yVal, xVal2, yVal2, fill="blue")
        for maxVal in range(len(data.maxFit) - 1):
            xVal = 20 + xScale * maxVal
            xVal2 = xVal + xScale
            yVal = 300 - (170 * data.maxFit[maxVal] / leastFE)
            yVal2 = 300 - (170 * data.maxFit[maxVal + 1] / leastFE)
            canvas.create_line(xVal, yVal, xVal2, yVal2, fill="red")
        for averageVal in range(len(data.averageFit) - 1):
            xVal = 20 + xScale * averageVal
            xVal2 = xVal + xScale
            yVal = 300 - (170 * data.averageFit[averageVal] / leastFE)
            yVal2 = 300 - (170 * data.averageFit[averageVal + 1] / leastFE)
            canvas.create_line(xVal, yVal, xVal2, yVal2)
    if len(data.minFit2) > 1:
        xScale = 170 // (len(data.minFit2) - 1)
        leastFE = leastFitEver(data.minFit2)
        for minVal2 in range(len(data.minFit2) - 1):
            xVal = 210 + xScale * minVal2
            xVal2 = xVal + xScale
            yVal = 300 - (170 * data.minFit2[minVal2] / leastFE)
            yVal2 = 300 - (170 * data.minFit2[minVal2 + 1] / leastFE)
            canvas.create_line(xVal, yVal, xVal2, yVal2, fill="blue")
        for maxVal2 in range(len(data.maxFit2) - 1):
            xVal = 210 + xScale * maxVal2
            xVal2 = xVal + xScale
            yVal = 300 - (170 * data.maxFit2[maxVal2] / leastFE)
            yVal2 = 300 - (170 * data.maxFit2[maxVal2 + 1] / leastFE)
            canvas.create_line(xVal, yVal, xVal2, yVal2, fill="red")
        for averageVal2 in range(len(data.averageFit2) - 1):
            xVal = 210 + xScale * averageVal2
            xVal2 = xVal + xScale
            yVal = 300 - (170 * data.averageFit2[averageVal2] / leastFE)
            yVal2 = 300 - (170 * data.averageFit2[averageVal2 + 1] / leastFE)
            canvas.create_line(xVal, yVal, xVal2, yVal2)


def makeNextButton(canvas, data):
    canvas.create_rectangle(150, 320, 250, 380, fill="green2")
    canvas.create_text(200, 350, text="Next", fill="white", font="ComicSansMS 19")


def genStats(canvas, data):
    canvas.create_text(80, 100, text="Average Fitness: %.1f" % (getAverageFitness(data.ballList))
                       , font="ComicSansMS 15")
    canvas.create_text(210, 100, text="Most Fit: %.1f" % (fittestBall(data.ballList))
                       , font="ComicSansMS 15")
    canvas.create_text(320, 100, text="Least Fit: %.1f" % (leastFit(data.ballList))
                       , font="ComicSansMS 15")


def makeMenu(canvas):
    canvas.create_rectangle(20, 100, 190, 200, fill="green2")
    canvas.create_rectangle(210, 100, 380, 200, fill="green2")
    canvas.create_text(105, 150, text="Randomly Generate", font="ComicSansMS 19")
    canvas.create_text(295, 150, text="Create Your Own", font="ComicSansMS 19")


def makeShapeCreator(canvas):
    canvas.create_rectangle(0, 0, 105, 50)
    canvas.create_oval(42.5, 15, 62.5, 35, fill="green2")
    canvas.create_rectangle(105, 0, 210, 50)
    canvas.create_line(142.5, 25, 172.5, 25)


def makeDone(canvas):
    canvas.create_rectangle(250, 0, 400, 50, fill="green2")
    canvas.create_text(325, 25, text="Done", font="ComicSansMs 19")


class Hoop(object):
    def drawHoop(self, canvas, data):
        d = data.distance * 80
        canvas.create_line(d - 50, 190, d - 50, 370)
        canvas.create_line(d - 50, 190, d - 100, 140)
        canvas.create_line(d - 100, 170, d - 100, 90)
        canvas.create_line(d - 100, 150, d - 150, 150)
        canvas.create_line(d - 110, 150, d - 110, 190)
        canvas.create_line(d - 150, 150, d - 150, 190)
        canvas.create_oval(d - 140, 140, d - 120, 160, fill="blue")


def init(data):
    data.counter = 0
    data.stage = 0
    '''
    data.nodeList = []
    data.muscleList = []
    data.node1 = Node([], 50, 250, "1")
    data.node2 = Node([data.node1], 100, 300, "2")
    data.muscle1 = Muscle(data.node2, data.node1, 10, 20, 15, 4, 100, 10, 4)
    data.node3 = Node([data.node1], 50, 350, "3")
    data.muscle2 = Muscle(data.node1, data.node3, 10, 20, 15, 3, 100, 10, 4)
    data.muscle3 = Muscle(data.node2, data.node3, 10, 20, 25, 3, 100, 10, 4)
    data.nodeList.append(data.node1)
    data.nodeList.append(data.node2)
    data.nodeList.append(data.node3)
    data.muscleList.append(data.muscle1)
    data.muscleList.append(data.muscle2)
    data.muscleList.append(data.muscle3)
    #data.node1 = Node([], 100, 360, '1')
    #data.node2 = Node([], 100, 310, '2')
    #data.muscle1 = Muscle(data.node1, data.node2, 30, 20, 10000, 0, 100, 15, 5)
    #data.nodeList.append(data.node1)
    data.nodeList.append(data.node2)
    data.muscleList.append(data.muscle1)
    data.shoot1 = Shooter(data.nodeList, data.muscleList)
    '''
    data.shooterList = []
    data.distance = data.width / 80
    data.ballList = []
    data.genEnd = False
    data.popSize = 10
    data.pos = 0
    data.gen = 0
    data.next = False
    generateAll(data.shooterList, data.ballList, data.popSize, data.distance)
    data.shoot1 = data.shooterList[0]
    data.originalState = copy.deepcopy(data.shooterList)
    data.ball1 = data.ballList[0]
    data.hoop1 = Hoop()
    data.minFit = []
    data.maxFit = []
    data.averageFit = []
    data.minFit2 = []
    data.maxFit2 = []
    data.averageFit2 = []
    # data.autoNext = True
    data.menu = True
    data.createOwn = False
    data.selectNode = False
    data.fakeBallPos = (None, None)
    data.canEnter = False
    data.preText = ""
    data.enterStuff = ""
    data.newShooter = Shooter([], [])
    data.testPos = (None, None)
    data.selectMuscle = False
    data.muscleConnectList = []
    data.msStrength = None
    data.msContractionTimer = None
    data.msExtensionTimer = None
    data.msContractionLength = None
    data.msExtensionLength = None
    data.msMinLength = None
    data.msMaxLength = None


def leftPressed(event, canvas, data):
    if (event.x >= 150 and event.x <= 250 and event.y >= 320 and event.y <= 380
            and data.next == True):  # or data.autoNext == True):
        if (numZeros(data.ballList) >= 7):
            data.stage += 1
        if (data.stage == 1):
            newWidth = random.randint(400, 700)
            canvas.config(width=newWidth, height=400)
            data.width = newWidth
            data.distance = newWidth / 80
        data.shooterList = getMostFit(data.originalState, data.ballList, data.distance)
        data.originalState = copy.deepcopy(data.shooterList)
        newBaskets(data.popSize, data.ballList)
        data.shoot1 = data.shooterList[0]
        data.ball1 = data.ballList[0]
        data.pos = 0
        data.genEnd = False
        data.next = False
    if (event.x >= 20 and event.x <= 190 and event.y >= 100 and event.y <= 200
            and data.menu == True):
        data.menu = False
    elif (event.x >= 210 and event.x <= 380 and event.y >= 100 and event.y <= 200
          and data.menu == True):
        data.menu = False
        data.shooterList = []
        data.createOwn = True
    if (event.x >= 37 and event.x <= 68 and event.y <= 40 and event.y >= 10
            and data.createOwn):
        data.selectNode = True
    if (event.x >= 135 and event.x <= 185 and event.y <= 40 and event.y >= 10
            and data.createOwn):
        data.selectMuscle = True
    if (data.selectMuscle):
        if (len(data.newShooter.nodeList) >= 2):
            for node in data.newShooter.nodeList:
                if (distance(node.cx, event.x, node.cy, event.y) < node.r):
                    if (len(data.muscleConnectList) != 2):
                        data.muscleConnectList.append(node)
                    if (len(data.muscleConnectList) == 2):
                        data.preText = "Strength: "
                        data.canEnter = True
    if (event.x >= 250 and event.y <= 50 and data.createOwn and data.newShooter.nodeList != []):
        copyList = []
        for i in range(data.popSize // 2):
            copyShooter = copy.deepcopy(data.newShooter)
            copyList.append(copyShooter)
        mutateList = copy.deepcopy(copyList)
        for elem in mutateList:
            mutateShooter(elem, data.distance)
        data.shooterList.extend(copyList)
        data.shooterList.extend(mutateList)
        data.shoot1 = data.shooterList[0]
        data.createOwn = False


def leftMoved(event, canvas, data):
    if (data.selectNode):
        data.fakeBallPos = (event.x, event.y)


def leftReleased(event, canvas, data):
    if (data.selectNode):
        data.preText = "Friction: "
        data.textPos = (event.x, event.y - 20)
        data.canEnter = True


def keyPressed(event, data):
    if (data.canEnter):
        enterables = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if event.char in enterables:
            data.enterStuff += event.char
        if event.char == '.':
            if data.enterStuff.count('.') < 1:
                data.enterStuff += event.char
        if event.keysym == "Return" and data.enterStuff != "":
            if (data.preText == "Friction: "):
                xPos, yPos = data.fakeBallPos
                data.fakeBallPos = (None, None)
                newNodeCxB = numpy.random.randn()
                newNodeCyB = numpy.random.randn()
                newNodeCxW = (xPos - newNodeCxB) / data.distance
                newNodeCyW = (yPos - newNodeCyB) / data.distance
                newNodeFriction = float(data.enterStuff)
                if (newNodeFriction > 1):
                    newNodeFriction = 1
                elif (newNodeFriction < 0):
                    newNodeFriction = 0
                newNodeFrictionB = numpy.random.randn()
                newNodeFrictionW = (newNodeFriction - newNodeFrictionB) / data.distance
                data.newShooter.nodeList.append(Node([], newNodeCxW, newNodeCxB,
                                                     newNodeCyW, newNodeCyB, newNodeFrictionW, newNodeFrictionB,
                                                     data.distance))
                data.enterStuff = ""
                data.canEnter = False
                data.selectNode = False
            if (data.preText == "Strength: "):
                data.msStrength = int(data.enterStuff)
                data.enterStuff = ""
                data.preText = "Muscle Contraction Timer: "
            elif (data.preText == "Muscle Contraction Timer: "):
                data.msContractionTimer = int(data.enterStuff)
                data.enterStuff = ""
                data.preText = "Muscle Contraction Length: "
            elif (data.preText == "Muscle Contraction Length: "):
                data.msContractionLength = int(data.enterStuff)
                data.enterStuff = ""
                data.preText = "Muscle Extension Timer: "
            elif (data.preText == "Muscle Extension Timer: "):
                data.msExtensionTimer = int(data.enterStuff)
                data.enterStuff = ""
                data.preText = "Muscle Extension Length: "
            elif (data.preText == "Muscle Extension Length: "):
                data.msExtensionLength = int(data.enterStuff)
                data.enterStuff = ""
                data.preText = "Muscle Min Length: "
            elif (data.preText == "Muscle Min Length: "):
                data.msMinLength = int(data.enterStuff)
                data.enterStuff = ""
                data.preText = "Muscle Max Length: "
            elif (data.preText == "Muscle Max Length: "
                  and int(data.enterStuff) > data.msMinLength):
                # strengthW, strengthB, minLengthW, minLengthB, timerW, timerB, contractionLengthW, contractionLengthB, maxLengthW, maxLengthB, timer2W, timer2B, eccentricLengthW, eccentricLengthB
                data.msMaxLength = int(data.enterStuff)
                data.enterStuff = ""
                newMuscleStrengthB = numpy.random.randn()
                newMuscleTimerB = numpy.random.randn()
                newMuscleContractionLengthB = numpy.random.randn()
                newMuscleTimer2B = numpy.random.randn()
                newMuscleEccentricLengthB = numpy.random.randn()
                newMuscleMinLengthB = numpy.random.randn()
                newMuscleMaxLengthB = numpy.random.randn()
                newMuscleStrengthW = (data.msStrength - newMuscleStrengthB) / data.distance
                newMuscleTimerW = (data.msContractionTimer - newMuscleTimerB) / data.distance
                newMuscleContractionLengthW = (data.msContractionLength
                                               - newMuscleContractionLengthB) / data.distance
                newMuscleTimer2W = (data.msExtensionTimer - newMuscleTimer2B) / data.distance
                newMuscleEccentricLengthW = (data.msExtensionLength
                                             - newMuscleEccentricLengthB) / data.distance
                newMuscleMinLengthW = (data.msMinLength - newMuscleMinLengthB) / data.distance
                newMuscleMaxLengthW = (data.msMaxLength - newMuscleMaxLengthB) / data.distance
                data.newShooter.muscleList.append(Muscle(data.muscleConnectList[0],
                                                         data.muscleConnectList[1], newMuscleStrengthW,
                                                         newMuscleStrengthW,
                                                         newMuscleMinLengthW, newMuscleMinLengthB, newMuscleTimerW,
                                                         newMuscleTimerB, newMuscleContractionLengthW,
                                                         newMuscleContractionLengthB,
                                                         newMuscleMaxLengthW, newMuscleMaxLengthB, newMuscleTimer2W,
                                                         newMuscleTimer2B,
                                                         newMuscleEccentricLengthW, newMuscleEccentricLengthB,
                                                         data.distance))
                data.canEnter = False

        if event.keysym == "BackSpace":
            data.enterStuff = data.enterStuff[:-1]


def timerFired(canvas, data):
    if not data.next and not data.menu and not data.createOwn:
        data.counter += 1
        if data.counter % 120 == 0:
            data.shoot1.stop()
            data.ball1.stop()
            if (data.pos == data.popSize - 1):
                data.genEnd = True
            else:
                print(data.ball1.fitness)
                # for node in data.shoot1.nodeList:
                # print(node.cx, node.cy)
                data.pos += 1
                data.shoot1 = data.shooterList[data.pos]
                data.ball1 = data.ballList[data.pos]
            time.sleep(0.05)
            data.counter = 1
        if not (data.genEnd):
            data.shoot1.onTimerFired(data)
            data.ball1.onTimerFired(data)
        else:
            if data.stage == 0:
                data.minFit.append(leastFit(data.ballList))
                data.maxFit.append(fittestBall(data.ballList))
                data.averageFit.append(getAverageFitness(data.ballList))
            elif data.stage == 1:
                data.minFit2.append(leastFit(data.ballList))
                data.maxFit2.append(fittestBall(data.ballList))
                data.averageFit2.append(getAverageFitness(data.ballList))
            # canvas.config(width=500, height=400)
            # data.width = 500
            # data.distance = 500 / 80
            # print("Gen: " + str(data.gen) + str(getAverageFitness(data.ballList)))
            data.gen += 1
            canvas.config(width=400, height=400)
            data.next = True


def drawGround(canvas, data):
    canvas.create_rectangle(0, data.height - 30, data.width, data.height, fill="beige")


def redrawAll(canvas, data):
    if not data.menu:
        if data.createOwn:
            drawGround(canvas, data)
            data.hoop1.drawHoop(canvas, data)
            makeShapeCreator(canvas)
            data.newShooter.draw(canvas)
            makeDone(canvas)
        elif not data.next:
            data.shoot1.draw(canvas)
            data.ball1.draw(canvas)
            drawGround(canvas, data)
            data.hoop1.drawHoop(canvas, data)
            canvas.create_text(200, 50, text="Generation: %i" % (data.gen))
            canvas.create_text(200, 100, text="Creature: %i" % (data.pos + 1))
        else:
            genStats(canvas, data)
            makeNextButton(canvas, data)
            makeGraphs(canvas, data)
    else:
        makeMenu(canvas)
    if (data.fakeBallPos != (None, None)):
        xPos, yPos = data.fakeBallPos
        canvas.create_oval(xPos - 10, yPos - 10, xPos + 10, yPos + 10, fill="red")
    if (data.canEnter):
        textX, textY = data.textPos
        displayText = data.preText + data.enterStuff
        canvas.create_text(textX, textY, text=displayText)


####################################
# use the run function as-is
####################################
'''
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data, canvas)
        redrawAllWrapper(canvas, data)

    def mouseWrapper(mouseFn, event, canvas, data):
        mouseFn(event, canvas, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)
    def timerFiredWrapper(canvas, data):
        timerFired(canvas, data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mouseWrapper(leftPressed, event, canvas, data))
    root.bind("<B1-ButtonRelease>", lambda event:
                            mouseWrapper(leftReleased, event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(400, 400)
'''


def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

        # Note changes #1:

    def mouseWrapper(mouseFn, event, canvas, data):
        mouseFn(event, canvas, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(canvas, data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call init
    class Struct(object): pass

    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 10  # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events

    # Note changes #2:
    root.bind("<B1-ButtonRelease>", lambda event:
    mouseWrapper(leftReleased, event, canvas, data))
    root.bind("<Button-1>", lambda event:
    mouseWrapper(leftPressed, event, canvas, data))
    canvas.bind("<B1-Motion>", lambda event:
    mouseWrapper(leftMoved, event, canvas, data))
    root.bind("<Key>", lambda event:
    keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


run(400, 400)