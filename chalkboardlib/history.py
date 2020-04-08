import pygame
import chalkboardlib.globals as gb
import chalkboardlib.object

class Event:

    def __init__(self):
        pass

    def do(self):
        pass

    def undo(self):
        pass

class AddObjectsEvent(Event):

    objects = None

    def __init__(self, objs):
        self.objects = objs

    def do(self):
        for obj in self.objects:
            gb.OBJECTS.append(obj)

    def undo(self):
        for _ in range(len(self.objects)):
            gb.OBJECTS.pop()

def add_event(event):

    gb.REDO_BUFFER.clear()
    gb.UNDO_BUFFER.append(event)
    event.do()

def undo():

    if len(gb.UNDO_BUFFER) > 0:
        gb.UNDO_BUFFER[-1].undo()
        gb.REDO_BUFFER.append(gb.UNDO_BUFFER.pop())

def redo():

    if len(gb.REDO_BUFFER) > 0:
        gb.REDO_BUFFER[-1].do()
        gb.UNDO_BUFFER.append(gb.REDO_BUFFER.pop())