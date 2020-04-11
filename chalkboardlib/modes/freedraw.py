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

    thickness = None
    object_buffer = None

    def load(self):
        super().load()
        if FreeDrawMode.thickness is None:
            FreeDrawMode.thickness = gb.CONFIG["default-line-thickness"]

    def tick(self):
        super().tick()

        if self.object_buffer is not None:
            self.object_buffer.draw()

        # brush size hint
        radius = int(FreeDrawMode.thickness/2*gb.VIEW_SCALE)
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
                    self.object_buffer = SmoothPolyline(gb.MOUSE_X, gb.MOUSE_Y, gb.ACTIVE_COLOR, FreeDrawMode.thickness)
                else:
                    self.object_buffer = Polyline(gb.MOUSE_X, gb.MOUSE_Y, gb.ACTIVE_COLOR, FreeDrawMode.thickness)

        elif ev.type == pygame.MOUSEBUTTONUP:
            if ev.button == 1 and self.object_buffer is not None:
                add_event(AddObjectsEvent([self.object_buffer]))
                self.object_buffer = None

        elif ev.type == pygame.MOUSEMOTION:
            if self.object_buffer is not None:

                self.object_buffer.insert(gb.MOUSE_X, gb.MOUSE_Y)

                # remove duplicate points (compress w/ epsilon < 0)
                self.object_buffer.reduce_last(-1.0, 10)

                if gb.CONFIG["smooth-lines"]:
                    self.object_buffer.smooth_last(gb.CONFIG["smooth-lines-degree"])

        elif ev.type == pygame.KEYDOWN:
            s = key_string(ev)

            # size selection
            if s == gb.CONFIG["controls"]["increase-thickness"]:
                FreeDrawMode.thickness *= gb.CONFIG["zoom-ratio"]
            elif s == gb.CONFIG["controls"]["decrease-thickness"]:
                FreeDrawMode.thickness /= gb.CONFIG["zoom-ratio"]