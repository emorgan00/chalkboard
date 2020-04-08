import pygame
import chalkboardlib.globals as gb
import chalkboardlib.object
from chalkboardlib.util import key_string, parse_color
from chalkboardlib.mode import Mode, DrawMode, BaseDrawMode
from chalkboardlib.objects.polyline import Polyline
from chalkboardlib.history import add_event, AddObjectsEvent

class FreeDrawMode(BaseDrawMode):

    object_buffer = None

    def load(self):
        super().load()

    def tick(self):
        super().tick()

        if self.object_buffer is not None:
            self.object_buffer.insert(gb.MOUSE_X, gb.MOUSE_Y)
            self.object_buffer.draw()

    def event(self, ev):
        super().event(ev)

        if ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:
                self.object_buffer = Polyline(gb.MOUSE_X, gb.MOUSE_Y, gb.ACTIVE_COLOR, gb.LINE_THICKNESS)

        elif ev.type == pygame.MOUSEBUTTONUP:
            if ev.button == 1:
                add_event(AddObjectsEvent([self.object_buffer]))
                self.object_buffer = None