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

def add_object(obj):

    gb.REDO_BUFFER.clear()
    gb.OBJECTS.append(obj)
    gb.UNDO_BUFFER.append(1)

def add_objects(objs):

    gb.REDO_BUFFER.clear()
    for obj in objs:
        gb.OBJECTS.append(obj)
    gb.UNDO_BUFFER.append(len(objs))

def undo():

    if len(gb.UNDO_BUFFER) > 0:
        gb.REDO_BUFFER.append([])
        for _ in range(gb.UNDO_BUFFER.pop()):
            gb.REDO_BUFFER[-1].append(gb.OBJECTS.pop())

def redo():

    if len(gb.REDO_BUFFER) > 0:
        gb.UNDO_BUFFER.append(len(gb.REDO_BUFFER[-1]))
        for obj in gb.REDO_BUFFER.pop():
            gb.OBJECTS.append(obj)