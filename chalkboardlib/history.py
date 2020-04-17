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

    indices = None
    objects = None

    def __init__(self, inds):
        self.indices = inds

    # note: runs in O(n) time where n is
    # the number of existing objects
    def do(self):
        new_objects, self.objects = [], []

        i = 0
        for j, obj in enumerate(gb.OBJECTS):
            if i < len(self.indices) and j == self.indices[i]:
                i += 1
                self.objects.append(obj)
            else:
                new_objects.append(obj)

        gb.OBJECTS = new_objects

    # also O(n)
    def undo(self):
        new_objects = []

        i = 0
        for j, obj in enumerate(gb.OBJECTS):
            while i < len(self.indices) and j == self.indices[i]:
                new_objects.append(self.objects[i])
                i += 1
            new_objects.append(obj)

        while i < len(self.objects):
            new_objects.append(self.objects[i])
            i += 1

        gb.OBJECTS = new_objects

class MoveObjectsEvent(Event):

    indices = None
    dx, dy = 0, 0

    def __init__(self, inds, dx, dy):
        self.indices = inds
        self.dx, self.dy = dx, dy

    def do(self):
        for i in self.indices:
            if i < len(gb.OBJECTS):
                gb.OBJECTS[i].translate(self.dx, self.dy)

    def undo(self):
        for i in self.indices:
            if i < len(gb.OBJECTS):
                gb.OBJECTS[i].translate(-self.dx, -self.dy)

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