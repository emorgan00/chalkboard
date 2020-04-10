import pygame
from math import hypot
import chalkboardlib.globals as gb
from chalkboardlib.object import ScreenObject
from chalkboardlib.util import onscreen

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

    # smooth only the last n segments
    def smooth_last(self, n):

        for i in range(max(len(self.points)-1-n, 1), len(self.points)-1):

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

    # shift recently drawn points closer together to avoid blockiness
    def smooth(self):
        self.smooth_last(len(self.points)-1)

    # run RDP reduction on only the last n segments
    def reduce_last(self, epsilon, n):

        reduced_points = self.points[:max(0, len(self.points)-1-n)]

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
                d = abs((y2-y1)*self.points[j][0]-(x2-x1)*self.points[j][1]+x2*y1-y2*x1) / h
                if d > dist:
                    i, dist = j, d

            if dist > epsilon or (i, j) == (0, len(self.points)-1):
                RDP_reduce(a, i)
                RDP_reduce(i, b)
            else:
                x, y = self.points[a][0], self.points[a][1]
                if len(reduced_points) == 0 or hypot(x-reduced_points[-1][0], y -reduced_points[-1][1]) > 0:
                    reduced_points.append(self.points[a])

        RDP_reduce(max(0, len(self.points)-1-n), len(self.points)-1)
        reduced_points.append(self.points[-1])

        self.points = reduced_points

    # remove some points to make it draw faster
    def reduce(self, epsilon):
        self.reduce_last(epsilon, len(self.points)-1)

    def refresh(self):
        if gb.CONFIG["compress-lines"]:
            self.reduce(gb.CONFIG["compress-lines-epsilon"]*self.thickness)

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

    polygons = None
    circle_points = None

    def __init__(self, x, y, color, thickness):
        super().__init__(x, y, color, thickness)
        self.update_polygon()

    def insert(self, x, y):
        super().insert(x, y)
        self.update_polygon()

    # create circle points + polygon points
    def update_polygon(self):

        self.polygons = []
        self.circle_points = []
        width = self.thickness/2

        # start and end always get circles
        self.circle_points.append(self.points[0])
        self.circle_points.append(self.points[-1])

        # rectangles as segments
        for i in range(len(self.points)-1):

            x1, y1, x2, y2 = *self.points[i], *self.points[i+1]
            dx, dy = x2-x1, y2-y1
            h = hypot(dx, dy)
            if h == 0:
                continue
            dx, dy = dx*width/h, dy*width/h

            # fill in for gaps caused by rotated rectangle
            bx, by = x2-dy, y2+dx
            if i < len(self.points)-2:
                x3, y3 = self.points[i+2][0], self.points[i+2][1]
                dx2, dy2 = x3-x2, y3-y2
                h2 = hypot(dx2, dy2)
                if h2 != 0:
                    dx2, dy2 = dx2*width/h2, dy2*width/h2

                    # extra circle for sharp turns
                    if width > 0 and (dx*dx2+dy*dy2)/width**2 < 0.2:
                        self.circle_points.append(self.points[i+1])

                    # check for rotate right vs. left
                    if dy*dx2 - dx*dy2 < 0:
                        bx, by = x2+dy2, y2-dx2
                    else:
                        bx, by = x2-dy2, y2+dx2

            self.polygons.append(((x1+dy, y1-dx), (x1-dy, y1+dx), (x2-dy, y2+dx), (bx, by), (x2+dy, y2-dx)))

    def refresh(self):
        super().refresh()
        self.update_polygon()

    def draw(self):

        width = int(self.thickness*gb.VIEW_SCALE/2)
        if not self.onscreen() or width > min(gb.SCREEN.get_width(), gb.SCREEN.get_height()):
            return

        if width > 0:
            for x, y in self.circle_points:
                x, y = int(x*gb.VIEW_SCALE+gb.VIEW_X_OFFSET), int(y*gb.VIEW_SCALE+gb.VIEW_Y_OFFSET)
                if onscreen(x-width, y-width, x+width, y+width):
                    pygame.gfxdraw.aacircle(gb.SCREEN, x, y, width, self.color)
                    pygame.gfxdraw.filled_circle(gb.SCREEN, x, y, width, self.color)

        for poly in self.polygons:
            scaled_points = [(x*gb.VIEW_SCALE+gb.VIEW_X_OFFSET, y*gb.VIEW_SCALE+gb.VIEW_Y_OFFSET) for x, y in poly]
            min_x = min(x for x, _ in scaled_points)-width
            max_x = max(x for x, _ in scaled_points)+width
            min_y = min(y for _, y in scaled_points)-width
            max_y = max(y for _, y in scaled_points)+width
            if onscreen(min_x, min_y, max_x, max_y):
                pygame.gfxdraw.aapolygon(gb.SCREEN, scaled_points, self.color)
                pygame.gfxdraw.filled_polygon(gb.SCREEN, scaled_points, self.color)