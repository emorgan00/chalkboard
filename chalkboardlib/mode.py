import pygame
import chalkboardlib.globals as gb
from chalkboardlib.util import key_string

class Mode:

    def __init__(self):
        pass

    # ask to destroy this mode at end of tick
    def kill(self):
        gb.MODES.pop()

    # ask to spawn a new mode at end of tick
    def spawn(self, mode):
        gb.MODES.append(mode)

    def tick(self):
        pass

    def event(self, ev):

        # window-level events
        if ev.type == pygame.VIDEORESIZE:
            gb.SCREEN = pygame.display.set_mode(ev.dict["size"], pygame.HWSURFACE | pygame.RESIZABLE | pygame.DOUBLEBUF)

        elif ev.type == pygame.KEYDOWN:
            s = key_string(ev.key)

            if s == gb.CONFIG["controls"]["quit"]:
                self.kill()
                if len(gb.MODES) > 0:
                    gb.MODES[-1].event(ev)

        elif ev.type == pygame.QUIT:
            # hacky solution, should be more robust
            print("test")
            import sys
            sys.stdout.flush()
            gb.MODES.clear()

# describes a Mode which supports basic interaction with the drawing environment
class DrawMode(Mode):

    def event(self, ev):
        super().event(ev)

# describes a Mode which is always at the outermost level
class BaseDrawMode(DrawMode):

    def event(self, ev):
        super().event(ev)