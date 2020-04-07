import pygame
import chalkboardlib.globals as gb
import chalkboardlib.object
from chalkboardlib.util import key_string, parse_color
from chalkboardlib.mode import Mode, DrawMode, BaseDrawMode
from chalkboardlib.objects.polyline import Polyline

class FreeDrawMode(BaseDrawMode):

    mouse_down = False
    object_buffer = None

    def load(self):
        super().load()

    def tick(self):
        super().tick()

        gb.SCREEN.fill(parse_color(gb.CONFIG["colors"]["background"]))
        for obj in gb.OBJECTS:
            obj.draw()

        if self.mouse_down:
            self.object_buffer.insert(*pygame.mouse.get_pos())
            self.object_buffer.draw()

    def event(self, ev):
        super().event(ev)

        if ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:
                self.mouse_down = True
                self.object_buffer = Polyline(*pygame.mouse.get_pos(), gb.ACTIVE_COLOR, gb.LINE_THICKNESS)

        elif ev.type == pygame.MOUSEBUTTONUP:
            if ev.button == 1:
                self.mouse_down = False
                chalkboardlib.object.add_object(self.object_buffer)
                self.object_buffer = None