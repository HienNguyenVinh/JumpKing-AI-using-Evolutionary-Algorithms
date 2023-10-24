from collections import namedtuple
import pygame
from .settings import *

Point = namedtuple("Point", ["x", "y"])

def AreLinesColliding(a1, b1, a2, b2):
    uA = ((b2[0] - a2[0]) * (a1[1] - a2[1]) - (b2[1] - a2[1]) * (a1[0] - a2[0])) / ((b2[1] - a2[1]) * (b1[0] - a1[0]) - (b2[0] - a2[0]) * (b1[1] - a1[1]))
    uB = ((b1[0] - a1[0]) * (a1[1] - a2[1]) - (b1[1] - a1[1]) * (a1[0] - a2[0])) / ((b2[1] - a2[1]) * (b1[0] - a1[0]) - (b2[0] - a2[0]) * (b1[1] - a1[1]))
    if(uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1):
        intersectionX = a1[0] + (uA * (b1[0] - a1[0]))
        intersectionY = a1[1] + (uA * (b1[1] - a1[1]))
        return [True, intersectionX, intersectionY]
    return [False, 0, 0]

class DiagonalCollisionInfo:
    def __init__(self):
        self.collisionPoints = []
        self.collidePlayerL = False
        self.collidePlayerR = False
        self.collidePlayerT = False
        self.collidePlayerB = False


class Line:
    def __str__(self):
        return f"{self.__class__.__name__}({self.x1}, {self.y1}, {self.x2}, {self.y2})"

    def __repr__(self):
        return self.__str__()

    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1 = x1 * alpha, y1 * alpha
        self.x2, self.y2 = x2 * alpha, y2 * alpha

        self.isHorizontal = y1 == y2
        self.isVertical = x1 == x2
        self.isDiagonal = not (self.isHorizontal or self.isVertical)

        self.center = Point((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)

        self.EnsureCoordnates()

    def SetDiagonalCollisionInfo(self, info):
        self.diagonalCollisionInfo = info

    def GetType(self):
        return (self.x1, self.y1, self.x2, self.y2)

    # make sure that p1 is always in the lower left corner and p2 is always in the upper right corner of the line.
    def EnsureCoordnates(self):
        if not self.isDiagonal:
            if self.x1 > self.x2 or self.y1 > self.y2:
                self.x1, self.x2 = self.x2, self.x1
                self.y1, self.y2 = self.y2, self.y1
        self.p1 = Point(self.x1, self.y1)
        self.p2 = Point(self.x2, self.y2)
        self.p3 = Point((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)

    def Draw(self, window):
        pygame.draw.line(window, (255, 255, 255), self.p1, self.p2, 1)
