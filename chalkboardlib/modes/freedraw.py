import pygame
import chalkboardlib.globals as gb
from chalkboardlib.util import key_string, parse_color
from chalkboardlib.mode import Mode, DrawMode, BaseDrawMode

class FreeDrawMode(BaseDrawMode):

    def tick(self):

        gb.SCREEN.fill(parse_color(gb.CONFIG["colors"]["background"]))

    def event(self, ev):
        super().event(ev)

        if ev.type == pygame.KEYDOWN:
            print(key_string(ev.key))