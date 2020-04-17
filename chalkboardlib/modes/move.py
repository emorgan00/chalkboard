import pygame
import pygame.gfxdraw
import chalkboardlib.globals as gb
from chalkboardlib.util import key_string, parse_color
from chalkboardlib.modes.select import SelectMode
from chalkboardlib.modes.control import register_mode, check_for_mode_switch
from chalkboardlib.history import *

@register_mode("move")
class MoveMode(SelectMode):

    moving = False

    def load(self):
        super().load()
        self.moving = False

    def tick(self):
        super().tick()

        if SelectMode.selection_mode == 2:

            if SelectMode.in_window(gb.MOUSE_X, gb.MOUSE_Y):
                x, y = pygame.mouse.get_pos()
                h = int(gb.CONFIG["cursor-size"]*0.707)
                sh = int(gb.CONFIG["cursor-size"]*0.707*0.50)
                color = parse_color(gb.CONFIG["colors"]["cursor"])

                if h < gb.SCREEN.get_width()+gb.SCREEN.get_height():

                    # arrow icon thing
                    pygame.gfxdraw.line(gb.SCREEN, x-h, y-h, x+h, y+h, color)
                    pygame.gfxdraw.line(gb.SCREEN, x+h, y-h, x-h, y+h, color)

                    pygame.gfxdraw.vline(gb.SCREEN, x-h, y-h, y-sh, color)
                    pygame.gfxdraw.vline(gb.SCREEN, x-h, y+sh, y+h, color)
                    pygame.gfxdraw.vline(gb.SCREEN, x+h, y-h, y-sh, color)
                    pygame.gfxdraw.vline(gb.SCREEN, x+h, y+sh, y+h, color)

                    pygame.gfxdraw.hline(gb.SCREEN, x-h, x-sh, y-h, color)
                    pygame.gfxdraw.hline(gb.SCREEN, x+sh, x+h, y-h, color)
                    pygame.gfxdraw.hline(gb.SCREEN, x-h, x-sh, y+h, color)
                    pygame.gfxdraw.hline(gb.SCREEN, x+sh, x+h, y+h, color)

    def event(self, ev):
        super().event(ev)

        if ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:
                if SelectMode.selection_mode == 2:
                    if SelectMode.in_window(gb.MOUSE_X, gb.MOUSE_Y):
                        self.moving = True

        elif ev.type == pygame.MOUSEBUTTONUP:
            if ev.button == 1:
                self.moving = False

        elif ev.type == pygame.MOUSEMOTION:
            if SelectMode.selection_mode == 2 and self.moving:

                dx, dy = ev.rel[0]/gb.VIEW_SCALE, ev.rel[1]/gb.VIEW_SCALE

                for i in range(len(SelectMode.index_buffer)):
                    j, obj = SelectMode.index_buffer[i], SelectMode.object_buffer[i]
                    if j < len(gb.OBJECTS) and gb.OBJECTS[j] == obj:

                        obj.translate(dx, dy)

                x1, y1, x2, y2 = SelectMode.selection_window
                x3, y3 = SelectMode.selection_anchor
                SelectMode.selection_window = (x1+dx, y1+dy, x2+dx, y2+dy)
                SelectMode.selection_anchor = (x3+dx, y3+dy)