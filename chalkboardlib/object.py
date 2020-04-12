import pygame
from math import hypot
import chalkboardlib.globals as gb
from chalkboardlib.util import onscreen

# describes a visual object that appears on screen
class ScreenObject:

    x1, y1, x2, y2 = 0, 0, 0, 0

    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2

    # returns true if this object intersects the visible part of the screen
    def onscreen(self):
        x1_s, y1_s = self.x1*gb.VIEW_SCALE+gb.VIEW_X_OFFSET, self.y1*gb.VIEW_SCALE+gb.VIEW_Y_OFFSET
        x2_s, y2_s = self.x2*gb.VIEW_SCALE+gb.VIEW_X_OFFSET, self.y2*gb.VIEW_SCALE+gb.VIEW_Y_OFFSET
        return onscreen(x1_s, y1_s, x2_s, y2_s)

    def contains_point(self, x, y):
        return x >= self.x1 and x <= self.x2 and y >= self.y1 and y <= self.y2

    def draw(self):
        pass

    # should return a list of new objects created by erasing this one.
    # or, return None to indicate nothing happens.
    # return an empty list to delete this object altogether.
    def erase(self, x, y, r):

        def line_intersects(a, b):

            h = hypot(a[1]-b[1], a[0]-b[0])
            if h == 0:
                return False
            d = abs((b[1]-a[1])*x-(b[0]-a[0])*y+b[0]*a[1]-b[1]*a[0]) / h
            return d < r
        
        intersects = self.contains_point(x, y)
        points = ((self.x1, self.y1), (self.x2, self.y1), (self.x2, self.y2), (self.x2, self.y1))
        for i in range(4):
            intersects = intersects or line_intersects(points[i], points[(i+1)%4])

        return [] if intersects else None

    # called when this object is committed to the screen
    def refresh(self):
        pass