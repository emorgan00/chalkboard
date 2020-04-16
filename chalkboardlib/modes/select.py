import pygame
import pygame.gfxdraw
import chalkboardlib.globals as gb
from chalkboardlib.util import key_string, parse_color
from chalkboardlib.mode import InteractMode
from chalkboardlib.modes.control import register_mode, check_for_mode_switch
from chalkboardlib.history import *

@register_mode("move")
class SelectMode(InteractMode):

    index_buffer = None
    selection_mode = 0
    selection_window = (0, 0, 0, 0)
    selection_anchor = (0, 0)
    # 0: no selection
    # 1: currently selecting
    # 2: active selection

    def load(self):
        super().load()

    def tick(self):
        super().tick()

        gb.SCREEN.fill(parse_color(gb.CONFIG["colors"]["background"]))
        for obj in gb.OBJECTS:
            obj.draw()

        if SelectMode.selection_mode in (0, 2):

            x, y = pygame.mouse.get_pos()
            height = 15
            if height < gb.SCREEN.get_width()+gb.SCREEN.get_height():
                pygame.gfxdraw.vline(gb.SCREEN, x, y-height, y+height, gb.ACTIVE_COLOR)
                pygame.gfxdraw.hline(gb.SCREEN, x-height, x+height, y, gb.ACTIVE_COLOR)

        if SelectMode.selection_mode == 1:

            x1 = min(gb.MOUSE_X, SelectMode.selection_anchor[0])
            y1 = min(gb.MOUSE_Y, SelectMode.selection_anchor[1])
            x2 = max(gb.MOUSE_X, SelectMode.selection_anchor[0])
            y2 = max(gb.MOUSE_Y, SelectMode.selection_anchor[1])
            SelectMode.selection_window = (x1, y1, x2, y2)

        if SelectMode.selection_mode in (1, 2):
            SelectMode.draw_selection()

    def draw_selection():

        x1, y1, x2, y2 = SelectMode.selection_window
        x3, y3 = SelectMode.selection_anchor
        x1, x2, x3 = (z*gb.VIEW_SCALE+gb.VIEW_X_OFFSET for z in (x1, x2, x3))
        y1, y2, y3 = (z*gb.VIEW_SCALE+gb.VIEW_Y_OFFSET for z in (y1, y2, y3))
        p1, p2 = (x3, y3), (x1+x2-x3, y1+y2-y3)
        height = 15

        if height < gb.SCREEN.get_width()+gb.SCREEN.get_height():

            x, y = map(int, min(p1, p2))
            pygame.gfxdraw.hline(gb.SCREEN, x, x+height, y, gb.ACTIVE_COLOR)
            x, y = map(int, max(p1, p2))
            pygame.gfxdraw.hline(gb.SCREEN, x-height, x, y, gb.ACTIVE_COLOR)
            y, x = map(int, min(p1[::-1], p2[::-1]))
            pygame.gfxdraw.vline(gb.SCREEN, x, y, y+height, gb.ACTIVE_COLOR)
            y, x = map(int, max(p1[::-1], p2[::-1]))
            pygame.gfxdraw.vline(gb.SCREEN, x, y-height, y, gb.ACTIVE_COLOR)

        for obj in gb.OBJECTS:
            if obj.intersects(*SelectMode.selection_window):
                obj.debug()

    def in_window(x, y):
        x1, y1, x2, y2 = SelectMode.selection_window
        return x >= x1 and x <= x2 and y >= y1 and y <= y2

    def new_selection():
        SelectMode.selection_mode = 1
        SelectMode.selection_anchor = (gb.MOUSE_X, gb.MOUSE_Y)

    def event(self, ev):
        super().event(ev)

        if SelectMode.selection_mode != 1:
            check_for_mode_switch(ev)

        if ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:
                if SelectMode.selection_mode == 0:
                    SelectMode.new_selection()
                elif SelectMode.selection_mode == 2:
                    if not SelectMode.in_window(gb.MOUSE_X, gb.MOUSE_Y):
                        SelectMode.new_selection()

        elif ev.type == pygame.MOUSEBUTTONUP:
            if ev.button == 1:
                if SelectMode.selection_mode == 1:

                    SelectMode.selection_mode = 2
                    SelectMode.index_buffer = []
                    for j, obj in enumerate(gb.OBJECTS):
                        if obj.intersects(*SelectMode.selection_window):
                            SelectMode.index_buffer.append(j)

        elif ev.type == pygame.KEYDOWN:
            s = key_string(ev)

            # undo, redo
            if SelectMode.selection_mode != 1:
                if s == gb.CONFIG["controls"]["undo"]:
                    chalkboardlib.history.undo()
                elif s == gb.CONFIG["controls"]["redo"]:
                    chalkboardlib.history.redo()

            if SelectMode.selection_mode == 2:
                if s == gb.CONFIG["controls"]["quit"]:
                    SelectMode.selection_mode = 0