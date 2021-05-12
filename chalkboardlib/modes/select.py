import pygame
import pygame.gfxdraw
from copy import deepcopy
import chalkboardlib.globals as gb
from chalkboardlib.util import key_string, parse_color
from chalkboardlib.mode import InteractMode
from chalkboardlib.modes.control import register_mode, check_for_mode_switch
from chalkboardlib.history import *

class SelectMode(InteractMode):

    object_buffer = None
    index_buffer = None
    selection_window = (0, 0, 0, 0)
    selection_anchor = (0, 0)
    
    selection_mode = 0
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

        if SelectMode.selection_mode == 0 \
        or SelectMode.selection_mode == 2 and not SelectMode.in_window(gb.MOUSE_X, gb.MOUSE_Y):

            x, y = pygame.mouse.get_pos()
            height = gb.CONFIG["cursor-size"]
            color = parse_color(gb.CONFIG["colors"]["cursor"])
            if height < gb.SCREEN.get_width()+gb.SCREEN.get_height():
                pygame.gfxdraw.vline(gb.SCREEN, x, y-height, y+height, color)
                pygame.gfxdraw.hline(gb.SCREEN, x-height, x+height, y, color)

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
        height = gb.CONFIG["cursor-size"]
        color = parse_color(gb.CONFIG["colors"]["cursor"])

        if height < gb.SCREEN.get_width()+gb.SCREEN.get_height():

            x, y = map(int, min(p1, p2))
            pygame.gfxdraw.hline(gb.SCREEN, x, x+height, y, color)
            x, y = map(int, max(p1, p2))
            pygame.gfxdraw.hline(gb.SCREEN, x-height, x, y, color)
            y, x = map(int, min(p1[::-1], p2[::-1]))
            pygame.gfxdraw.vline(gb.SCREEN, x, y, y+height, color)
            y, x = map(int, max(p1[::-1], p2[::-1]))
            pygame.gfxdraw.vline(gb.SCREEN, x, y-height, y, color)

        if SelectMode.selection_mode == 1:
            for obj in gb.OBJECTS:
                if obj.intersects(*SelectMode.selection_window):
                    obj.highlight()
        else:
            for i in range(len(SelectMode.index_buffer)):
                j, obj = SelectMode.index_buffer[i], SelectMode.object_buffer[i]
                if j < len(gb.OBJECTS) and gb.OBJECTS[j] == obj:
                    obj.highlight()

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
                    SelectMode.object_buffer = []
                    SelectMode.index_buffer = []
                    for i, obj in enumerate(gb.OBJECTS):
                        if obj.intersects(*SelectMode.selection_window):
                            SelectMode.object_buffer.append(obj)
                            SelectMode.index_buffer.append(i)

        elif ev.type == pygame.KEYDOWN:
            s = key_string(ev)

            # undo, redo
            if SelectMode.selection_mode != 1:

                if s == gb.CONFIG["controls"]["undo"]:
                    chalkboardlib.history.undo()
                elif s == gb.CONFIG["controls"]["redo"]:
                    chalkboardlib.history.redo()

            if SelectMode.selection_mode == 2:

                if s == gb.CONFIG["controls"]["discard-selection"]:
                    SelectMode.selection_mode = 0
                elif s == gb.CONFIG["controls"]["delete-selection"]:
                    add_event(RemoveObjectsEvent(SelectMode.index_buffer))
                    SelectMode.selection_mode = 0
                elif s == gb.CONFIG["controls"]["paste-selection"]:
                    add_event(AddObjectsEvent([
                        deepcopy(obj) for obj in self.object_buffer
                    ]))