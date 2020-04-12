import pygame
import pygame.gfxdraw
import chalkboardlib.globals as gb
from chalkboardlib.util import key_string, parse_color
from chalkboardlib.mode import InteractMode
from chalkboardlib.modes.control import register_mode, check_for_mode_switch
from chalkboardlib.history import *

@register_mode("erase")
class EraseMode(InteractMode):

    thickness = None
    object_buffer = None
    active_objects = None

    def load(self):
        super().load()
        if EraseMode.thickness is None:
            EraseMode.thickness = gb.CONFIG["default-erase-thickness"]

    def tick(self):
        super().tick()

        gb.SCREEN.fill(parse_color(gb.CONFIG["colors"]["background"]))

        if self.active_objects is not None:

            # square around mouse
            x1, y1 = gb.MOUSE_X-self.thickness/2, gb.MOUSE_Y-self.thickness/2
            x2, y2 = gb.MOUSE_X+self.thickness/2, gb.MOUSE_Y+self.thickness/2

            for i, obj in enumerate(gb.OBJECTS):

                if self.active_objects[i]:
                    if x1 <= obj.x2 and x2 >= obj.x1 and y1 <= obj.y2 and y2 >= obj.y1:
                        newobjs = obj.erase(gb.MOUSE_X, gb.MOUSE_Y, self.thickness/2)
                        if newobjs is not None:
                            self.active_objects[i] = False
                            for newobj in newobjs:
                                self.object_buffer.append(newobj)

                if self.active_objects[i]:
                    obj.draw()

        else:
            for obj in gb.OBJECTS:
                obj.draw()

        # brush size hint
        radius = int(EraseMode.thickness/2*gb.VIEW_SCALE)
        if radius*2 < gb.SCREEN.get_width()+gb.SCREEN.get_height():
            pygame.gfxdraw.aacircle(gb.SCREEN, *pygame.mouse.get_pos(), radius, parse_color(gb.CONFIG["colors"]["1"]))

    def commit(self):

        if self.active_objects is not None:
            indices = [i for i, x in enumerate(self.active_objects) if not x]
            add_event(GroupedEvent([RemoveObjectsEvent(indices), AddObjectsEvent(self.object_buffer)]))
            self.object_buffer, self.active_objects = None, None

    def event(self, ev):
        super().event(ev)

        if check_for_mode_switch(ev):
            self.commit()

        if ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:
                self.object_buffer, self.active_objects = [], [True]*len(gb.OBJECTS)

        elif ev.type == pygame.MOUSEBUTTONUP:
            if ev.button == 1 and self.object_buffer is not None:
                self.commit()

        elif ev.type == pygame.KEYDOWN:
            s = key_string(ev)

            # size selection
            if s == gb.CONFIG["controls"]["increase-size"]:
                EraseMode.thickness *= gb.CONFIG["zoom-ratio"]
            elif s == gb.CONFIG["controls"]["decrease-size"]:
                EraseMode.thickness /= gb.CONFIG["zoom-ratio"]

            # undoing while we are in the middle of an erase could
            # cause problems, so we just forbid it.
            if self.active_objects is None:
                # undo, redo
                if s == gb.CONFIG["controls"]["undo"]:
                    chalkboardlib.history.undo()
                elif s == gb.CONFIG["controls"]["redo"]:
                    chalkboardlib.history.redo()