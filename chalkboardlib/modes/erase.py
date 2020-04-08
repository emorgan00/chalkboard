import pygame
import chalkboardlib.globals as gb
import chalkboardlib.object
from chalkboardlib.util import key_string
from chalkboardlib.mode import Mode, DrawMode, BaseDrawMode
from chalkboardlib.objects.polyline import Polyline
from chalkboardlib.history import add_event, AddObjectsEvent

class EraseMode(BaseDrawMode):

    object_buffer = []

    def load(self):
        super().load()
        self.object_buffer = []

    def tick(self):
        super().tick()

    def event(self, ev):
        super().event(ev)

        if ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:
                pass

        elif ev.type == pygame.MOUSEBUTTONUP:
            if ev.button == 1:
                pass