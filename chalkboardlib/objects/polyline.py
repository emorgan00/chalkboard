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
        self.x1 = min(self.x1, x-self.thickness)
        self.y1 = min(self.y1, y-self.thickness)
        self.x2 = max(self.x2, x+self.thickness)
        self.y2 = max(self.y2, y+self.thickness)

    def smooth(self):

        # shift recently drawn points closer together to avoid blockiness
        for i in range(max(len(self.points)-5, 1), len(self.points)-1):

            x1, y1 = self.points[i-1][0], self.points[i-1][1]
            x2, y2 = self.points[i][0], self.points[i][1]
            x3, y3 = self.points[i+1][0], self.points[i+1][1]

            dx, dy = x2-x1, y2-y1
            h = hypot(dx, dy)
            if h == 0: continue
            dx, dy = dx/h, dy/h

            dx2, dy2 = x3-x2, y3-y2
            h = hypot(dx, dy)
            if h == 0: continue
            dx2, dy2 = dx2/h, dy2/h

            if dx*dx2+dy*dy2 > 0.2:
                self.points[i] = ((x1+x2+x3)/3, (y1+y2+y3)/3)

    # remove some points to make it draw faster
    def reduce(self, epsilon):

        reduced_points = []

        # RDP algorithm for removing redundant points
        def RDP_reduce(a, b):

            if b-a < 2:
                for i in range(a, b+1):
                    x, y = self.points[i][0], self.points[i][1]
                    if len(reduced_points) == 0 or hypot(x-reduced_points[-1][0], y -reduced_points[-1][1]) > 0:
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

            if dist > epsilon or (i, j) == (0, len(self.points)-1):
                RDP_reduce(a, i)
                RDP_reduce(i, b)
            else:
                x, y = self.points[a][0], self.points[a][1]
                if len(reduced_points) == 0 or hypot(x-reduced_points[-1][0], y -reduced_points[-1][1]) > 0:
                    reduced_points.append(self.points[a])

        RDP_reduce(0, len(self.points)-1)
        reduced_points.append(self.points[-1])

        self.points = reduced_points

    def draw(self):

        if not self.onscreen():
            return

        points_scaled = [(x*gb.VIEW_SCALE+gb.VIEW_X_OFFSET, y*gb.VIEW_SCALE+gb.VIEW_Y_OFFSET) for x, y in self.points]
        width = max(1, int(self.thickness*gb.VIEW_SCALE))

        if len(self.points) > 0:
            pygame.draw.lines(gb.SCREEN, self.color, False, points_scaled, width)
        else:
            x, y = points_scaled[0]
            pygame.gfxdraw.aacircle(gb.SCREEN, int(x), int(y), width//2, self.color)
            pygame.gfxdraw.filled_circle(gb.SCREEN, int(x), int(y), width//2, self.color)

# works identical to a polyline, but makes it look smoother (at cost of drawing time)
class SmoothPolyline(Polyline):

    def __init__(self, x, y, color, thickness):
        super().__init__(x, y, color, thickness)

    def insert(self, x, y):
        super().insert(x, y)

    def refresh(self):
        self.reduce(gb.CONFIG["smooth-lines"]["epsilon"])

    def draw(self):

        width = int(self.thickness*gb.VIEW_SCALE/2)
        if not self.onscreen() or width > min(gb.SCREEN.get_width(), gb.SCREEN.get_height()):
            return

        points_scaled = [(x*gb.VIEW_SCALE+gb.VIEW_X_OFFSET, y*gb.VIEW_SCALE+gb.VIEW_Y_OFFSET) for x, y in self.points]

        # circles at end points
        if width > 0:
            x, y = points_scaled[0][0], points_scaled[0][1]
            pygame.gfxdraw.aacircle(gb.SCREEN, int(x), int(y), width, self.color)
            pygame.gfxdraw.filled_circle(gb.SCREEN, int(x), int(y), width, self.color)
            x, y = points_scaled[-1][0], points_scaled[-1][1]
            pygame.gfxdraw.aacircle(gb.SCREEN, int(x), int(y), width, self.color)
            pygame.gfxdraw.filled_circle(gb.SCREEN, int(x), int(y), width, self.color)

        # rectangles as segments
        for i in range(len(points_scaled)-1):

            x1, y1, x2, y2 = *points_scaled[i], *points_scaled[i+1]
            dx, dy = x2-x1, y2-y1
            h = hypot(dx, dy)
            if h == 0:
                continue
            dx, dy = dx*width/h, dy*width/h

            # fill in for gaps caused by rotated rectangle
            bx, by = x2-dy, y2+dx
            if i < len(points_scaled)-2:
                x3, y3 = points_scaled[i+2][0], points_scaled[i+2][1]
                dx2, dy2 = x3-x2, y3-y2
                h2 = hypot(dx2, dy2)
                if h2 != 0:
                    dx2, dy2 = dx2*width/h2, dy2*width/h2

                    # extra circle for sharp turns
                    if width > 0 and (dx*dx2+dy*dy2)/width**2 < 0.2:
                        pygame.gfxdraw.aacircle(gb.SCREEN, int(x2), int(y2), width, self.color)
                        pygame.gfxdraw.filled_circle(gb.SCREEN, int(x2), int(y2), width, self.color)

                    # check for rotate right vs. left
                    if dy*dx2 - dx*dy2 < 0:
                        bx, by = x2+dy2, y2-dx2
                    else:
                        bx, by = x2-dy2, y2+dx2

            polygon_points = ((x1+dy, y1-dx), (x1-dy, y1+dx), (x2-dy, y2+dx), (bx, by), (x2+dy, y2-dx))

            pygame.gfxdraw.aapolygon(gb.SCREEN, polygon_points, self.color)
            pygame.gfxdraw.filled_polygon(gb.SCREEN, polygon_points, self.color)