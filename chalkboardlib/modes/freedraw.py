import pygame
import pygame.gfxdraw
import chalkboardlib.globals as gb
import chalkboardlib.object
from chalkboardlib.util import key_string, parse_color
from chalkboardlib.mode import Mode, DrawMode, BaseDrawMode
from chalkboardlib.objects.polyline import Polyline, SmoothPolyline
from chalkboardlib.history import add_event, AddObjectsEvent

class FreeDrawMode(BaseDrawMode):

    object_buffer = None

    def load(self):
        super().load()

    def tick(self):
        super().tick()

        if self.object_buffer is not None:
            self.object_buffer.insert(gb.MOUSE_X, gb.MOUSE_Y)
            # self.object_buffer.reduce(0.007)
            self.object_buffer.draw()

        # brush size hint
        pygame.gfxdraw.aacircle(gb.SCREEN, *pygame.mouse.get_pos(), int(gb.LINE_THICKNESS/2*gb.VIEW_SCALE), gb.ACTIVE_COLOR)

    def event(self, ev):
        super().event(ev)

        if ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:
                if gb.CONFIG["smooth-lines"]["toggle"]:
                    self.object_buffer = SmoothPolyline(gb.MOUSE_X, gb.MOUSE_Y, gb.ACTIVE_COLOR, gb.LINE_THICKNESS)
                else:
                    self.object_buffer = Polyline(gb.MOUSE_X, gb.MOUSE_Y, gb.ACTIVE_COLOR, gb.LINE_THICKNESS)

        elif ev.type == pygame.MOUSEBUTTONUP:
            if ev.button == 1:
                add_event(AddObjectsEvent([self.object_buffer]))
                self.object_buffer = None