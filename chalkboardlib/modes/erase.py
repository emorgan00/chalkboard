import pygame
import pygame.gfxdraw
import chalkboardlib.globals as gb
from chalkboardlib.util import key_string, parse_color
from chalkboardlib.mode import DrawMode
from chalkboardlib.modes.control import register_mode, check_for_mode_switch

@register_mode("erase")
class EraseMode(DrawMode):

    thickness = None

    def load(self):
        super().load()
        if EraseMode.thickness is None:
            EraseMode.thickness = gb.CONFIG["default-erase-thickness"]

    def tick(self):
        super().tick()

        # brush size hint
        radius = int(EraseMode.thickness/2*gb.VIEW_SCALE)
        if radius*2 < gb.SCREEN.get_width()+gb.SCREEN.get_height():
            pygame.gfxdraw.aacircle(gb.SCREEN, *pygame.mouse.get_pos(), radius, parse_color(gb.CONFIG["colors"]["1"]))

    def event(self, ev):
        super().event(ev)

        check_for_mode_switch(ev)

        if ev.type == pygame.KEYDOWN:
            s = key_string(ev)

            # size selection
            if s == gb.CONFIG["controls"]["increase-thickness"]:
                gb.LINE_THICKNESS /= gb.CONFIG["zoom-ratio"]
                EraseMode.thickness *= gb.CONFIG["zoom-ratio"]
            elif s == gb.CONFIG["controls"]["decrease-thickness"]:
                gb.LINE_THICKNESS *= gb.CONFIG["zoom-ratio"]
                EraseMode.thickness /= gb.CONFIG["zoom-ratio"]

        # create / commit new lines
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:
                pass

        elif ev.type == pygame.MOUSEBUTTONUP:
            if ev.button == 1:
                pass