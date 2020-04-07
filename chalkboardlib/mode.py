import pygame
import chalkboardlib.globals as gb
import chalkboardlib.object
from chalkboardlib.util import key_string, parse_color

class Mode:

    def __init__(self):
        pass

    # ask to destroy this mode at end of tick
    def kill(self):
        gb.MODES.pop()

    # ask to spawn a new mode at end of tick
    def spawn(self, mode):
        gb.MODES.append(mode)
        gb.MODES[-1].load()

    def load(self):
        pass

    def tick(self):
        pass

    def event(self, ev):

        # window-level events
        if ev.type == pygame.VIDEORESIZE:
            gb.SCREEN = pygame.display.set_mode(ev.dict["size"], pygame.HWSURFACE | pygame.RESIZABLE | pygame.DOUBLEBUF)

        elif ev.type == pygame.KEYDOWN:
            s = key_string(ev)

            if s == gb.CONFIG["controls"]["quit"]:
                self.kill()
                if len(gb.MODES) > 0:
                    gb.MODES[-1].event(ev)

        elif ev.type == pygame.QUIT:
            # hacky solution, should be more robust
            gb.MODES.clear()

# describes a Mode which supports basic interaction with the drawing environment
class DrawMode(Mode):

    def load(self):
        super().load()
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)

    def tick(self):
        super().tick()

    def event(self, ev):
        super().event(ev)

        if ev.type == pygame.KEYDOWN:
            s = key_string(ev)

            # color selection
            if s == "1":
                gb.ACTIVE_COLOR = parse_color(gb.CONFIG["colors"]["1"])
            if s == "2":
                gb.ACTIVE_COLOR = parse_color(gb.CONFIG["colors"]["2"])

            # undo, redo
            if s == gb.CONFIG["controls"]["undo"]:
                chalkboardlib.object.undo()
            if s == gb.CONFIG["controls"]["redo"]:
                chalkboardlib.object.redo()


# describes a Mode which is always at the outermost level
class BaseDrawMode(DrawMode):

    def load(self):
        super().load()

    def tick(self):
        super().tick()

    def event(self, ev):
        super().event(ev)