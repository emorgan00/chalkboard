import pygame
import chalkboardlib.globals as gb

# describes a visual object that appears on screen
class ScreenObject:

    x1, y1, x2, y2 = 0, 0, 0, 0

    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2

    def visible(self):
        return True

    def draw(self):
        pass