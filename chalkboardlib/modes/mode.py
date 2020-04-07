import pygame

class Mode:

    screen = None
    objects = []
    config = {}
    active = True

    def __init__(self, screen, objects, config):
        
        self.screen = screen
        self.object = objects
        self.config = config

    # ask to destroy this mode at end of tick
    def kill(self):
        self.active = False

    def load(self):
        pass

    def tick(self):
        pass

    def event(self, ev):
        pass

# describes a Mode which is always at the outermost level
class BaseMode(Mode):

    def event(self, ev):
        super().event(ev)