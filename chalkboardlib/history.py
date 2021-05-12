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
            obj.refresh()
            gb.OBJECTS.append(obj)

    def undo(self):
        for _ in range(len(self.objects)):
            gb.OBJECTS.pop()

class RemoveObjectsEvent(Event):

    objects = None

    def __init__(self, inds):
        self.objects = [gb.OBJECTS[i] for i in inds]

    # note: runs in O(n) time where n is
    # the number of existing objects
    def do(self):
        s = set(id(x) for x in self.objects)
        gb.OBJECTS = [obj for obj in gb.OBJECTS if id(obj) not in s]

    def undo(self):
        for obj in self.objects:
            gb.OBJECTS.append(obj)

class MoveObjectsEvent(Event):

    objects = None
    dx, dy = 0, 0

    def __init__(self, inds, dx, dy):
        self.objects = [gb.OBJECTS[i] for i in inds]
        self.dx, self.dy = dx, dy

    def do(self):
        s = set(id(x) for x in self.objects)
        for obj in gb.OBJECTS:
            if id(obj) in s:
                obj.translate(self.dx, self.dy)

    def undo(self):
        s = set(id(x) for x in self.objects)
        for obj in gb.OBJECTS:
            if id(obj) in s:
                obj.translate(-self.dx, -self.dy)

class GroupedEvent(Event):

    events = None

    def __init__(self, events):
        self.events = events

    def do(self):
        for ev in self.events:
            ev.do()

    def undo(self):
        for ev in reversed(self.events):
            ev.undo()

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