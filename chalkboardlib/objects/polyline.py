import pygame
from math import hypot
import chalkboardlib.globals as gb
from chalkboardlib.object import ScreenObject

class Polyline(ScreenObject):

    points = None
    thickness = 1
    color = (0, 0, 0)

    def __init__(self, x, y, color, thickness):
        super().__init__(x, y, x, y)
        self.points = [(x, y)]
        self.color = color
        self.thickness = thickness

    def insert(self, x, y):
        self.points.append((x, y))
        self.x1 = min(self.x1, x)
        self.y1 = min(self.y1, y)
        self.x2 = max(self.x2, x)
        self.y2 = max(self.y2, y)

    # remove some points to make it draw faster
    def reduce(self, epsilon):

        reduced_points = []

        # RDP algorithm for removing redundant points
        def RDP_reduce(a, b):

            if b-a < 2:
                for i in range(a, b+1):
                    reduced_points.append(self.points[i])
                return

            dist, i = 0.0, (a+b)//2
            x1, y1, x2, y2 = *self.points[a], *self.points[b]

            for j in range(a+1, b):
                h = hypot(y2-y1, x2-x1)
                if h == 0:
                    continue
                d = abs((y2-y1)*self.points[j][0]-(x2-x1)*self.points[j][1]+x2*y1-y2*x1) / h**2
                if d > dist:
                    i, dist = j, d

            if dist > epsilon:
                RDP_reduce(a, i)
                RDP_reduce(i, b)
            else:
                reduced_points.append(self.points[a])

        RDP_reduce(0, len(self.points)-1)
        reduced_points.append(self.points[-1])

        self.points = reduced_points

    def draw(self):
        if len(self.points) > 0:
            points_scaled = [(x*gb.VIEW_SCALE+gb.VIEW_X_OFFSET, y*gb.VIEW_SCALE+gb.VIEW_Y_OFFSET) for x, y in self.points]
            pygame.draw.lines(gb.SCREEN, self.color, False, points_scaled, max(1, int(self.thickness*gb.VIEW_SCALE)))

# works identical to a polyline, but makes it look smoother (at cost of drawing time)
class SmoothPolyline(Polyline):

    bezier_points = None

    def __init__(self, x, y, color, thickness):
        super().__init__(x, y, color, thickness)
        self.bezier_points = [(x, y)]

    def insert(self, x, y):
        super().insert(x, y)

    def refresh(self):
        self.reduce(gb.CONFIG["smooth-lines"]["epsilon"])

        