from collections import namedtuple
import pygame

Point = namedtuple("Point", ["x", "y"])


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
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2

        self.isHorizontal = y1 == y2
        self.isVertical = x1 == x2
        self.isDiagonal = not (self.isHorizontal or self.isVertical)

        self.center = Point((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)

        self.EnsureCoordnates()

    def SetDiagonalCollisionInfo(self, info):
        self.diagonalCollisionInfo = info

    def GetType(self):
        return (self.x1, self.y1, self.x2, self.y2)

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