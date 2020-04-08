import pygame
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

    def draw(self):
        points_scaled = [(x*gb.VIEW_SCALE+gb.VIEW_X_OFFSET, y*gb.VIEW_SCALE+gb.VIEW_Y_OFFSET) for x, y in self.points]
        pygame.draw.lines(gb.SCREEN, self.color, False, points_scaled, max(1, int(self.thickness*gb.VIEW_SCALE)))