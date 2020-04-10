import pygame
import pygame.gfxdraw
import chalkboardlib.globals as gb
import chalkboardlib.object
from chalkboardlib.util import key_string, parse_color
from chalkboardlib.mode import DrawMode
from chalkboardlib.modes.control import register_mode, check_for_mode_switch
from chalkboardlib.objects.polyline import Polyline, SmoothPolyline
from chalkboardlib.history import add_event, AddObjectsEvent

@register_mode("freedraw")
class FreeDrawMode(DrawMode):

    object_buffer = None

    def load(self):
        super().load()

    def tick(self):
        super().tick()

        if self.object_buffer is not None:

            self.object_buffer.insert(gb.MOUSE_X, gb.MOUSE_Y)

            # remove duplicate points (compress w/ epsilon < 0)
            self.object_buffer.reduce_last(-1.0, 10)

            if gb.CONFIG["smooth-lines"]:
                self.object_buffer.smooth_last(gb.CONFIG["smooth-lines-degree"])
            self.object_buffer.draw()

        # brush size hint
        radius = int(gb.LINE_THICKNESS/2*gb.VIEW_SCALE)
        if radius*2 < gb.SCREEN.get_width()+gb.SCREEN.get_height():
            pygame.gfxdraw.aacircle(gb.SCREEN, *pygame.mouse.get_pos(), radius, gb.ACTIVE_COLOR)

    def event(self, ev):
        super().event(ev)

        if self.object_buffer is None:
            check_for_mode_switch(ev)

        # create / commit new lines
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:
                if gb.CONFIG["fancy-lines"]:
                    self.object_buffer = SmoothPolyline(gb.MOUSE_X, gb.MOUSE_Y, gb.ACTIVE_COLOR, gb.LINE_THICKNESS)
                else:
                    self.object_buffer = Polyline(gb.MOUSE_X, gb.MOUSE_Y, gb.ACTIVE_COLOR, gb.LINE_THICKNESS)

        elif ev.type == pygame.MOUSEBUTTONUP:
            if ev.button == 1 and self.object_buffer is not None:
                add_event(AddObjectsEvent([self.object_buffer]))
                self.object_buffer = None