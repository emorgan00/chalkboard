import pygame
import pygame.gfxdraw
import chalkboardlib.globals as gb
from chalkboardlib.util import key_string, parse_color
from chalkboardlib.modes.select import SelectMode
from chalkboardlib.modes.control import register_mode, check_for_mode_switch
from chalkboardlib.history import *

@register_mode("move")
class MoveMode(SelectMode):

    def load(self):
        super().load()

    def tick(self):
        super().tick()

        if SelectMode.selection_mode == 2:

            x, y = pygame.mouse.get_pos()
            height = 10
            if height < gb.SCREEN.get_width()+gb.SCREEN.get_height():
                pygame.gfxdraw.vline(gb.SCREEN, x, y-height, y+height, gb.ACTIVE_COLOR)
                pygame.gfxdraw.hline(gb.SCREEN, x-height, x+height, y, gb.ACTIVE_COLOR)

    def event(self, ev):
        super().event(ev)

        if ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:
                if SelectMode.selection_mode == 2:
                    pass