import pygame
import chalkboardlib.globals as gb

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
        w, h = gb.SCREEN.get_width(), gb.SCREEN.get_height()
        return x1_s < w and y1_s < h and x2_s > 0 and y2_s > 0

    def draw(self):
        pass

    # called when this object is committed to the screen
    def refresh(self):
        pass