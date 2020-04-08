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
        
        # update mouse coordinates
        mx, my = pygame.mouse.get_pos()
        gb.MOUSE_X = (mx-gb.VIEW_X_OFFSET)/gb.VIEW_SCALE
        gb.MOUSE_Y = (my-gb.VIEW_Y_OFFSET)/gb.VIEW_SCALE

    def event(self, ev):

        # window-level events
        if ev.type == pygame.VIDEORESIZE:
            gb.SCREEN_SIZE = ev.dict["size"]
            gb.SCREEN = pygame.display.set_mode(gb.SCREEN_SIZE, pygame.HWSURFACE | pygame.RESIZABLE | pygame.DOUBLEBUF)

        elif ev.type == pygame.KEYDOWN:
            s = key_string(ev)

            if s == gb.CONFIG["controls"]["quit"]:
                self.kill()
                if len(gb.MODES) > 0:
                    gb.MODES[-1].event(ev)

            if s == gb.CONFIG["controls"]["fullscreen"]:
                if gb.FULLSCREEN:
                    gb.SCREEN = pygame.display.set_mode(gb.SCREEN_SIZE, pygame.HWSURFACE | pygame.RESIZABLE | pygame.DOUBLEBUF)
                else:
                    gb.SCREEN = pygame.display.set_mode(gb.CONFIG["fullscreen-window-size"], pygame.HWSURFACE | pygame.FULLSCREEN | pygame.DOUBLEBUF)
                gb.FULLSCREEN = not gb.FULLSCREEN

        elif ev.type == pygame.QUIT:
            # hacky solution, should be more robust
            gb.MODES.clear()

# describes a Mode which supports basic interaction with the drawing environment
class DrawMode(Mode):

    scroll_down = False

    def load(self):
        super().load()
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        self.scroll_down = False

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

        # panning and zooming
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 2:
                self.scroll_down = True
            elif ev.button == 4:
                gb.VIEW_X_OFFSET -= gb.MOUSE_X*gb.VIEW_SCALE*0.2
                gb.VIEW_Y_OFFSET -= gb.MOUSE_Y*gb.VIEW_SCALE*0.2
                gb.VIEW_SCALE *= 1.2
            elif ev.button == 5:
                gb.VIEW_SCALE /= 1.2
                gb.VIEW_X_OFFSET += gb.MOUSE_X*gb.VIEW_SCALE*0.2
                gb.VIEW_Y_OFFSET += gb.MOUSE_Y*gb.VIEW_SCALE*0.2

        elif ev.type == pygame.MOUSEBUTTONUP:
            if ev.button == 2:
                self.scroll_down = False

        elif ev.type == pygame.MOUSEMOTION:
            if self.scroll_down:
                rx, ry = ev.rel
                gb.VIEW_X_OFFSET += rx
                gb.VIEW_Y_OFFSET += ry

# describes a Mode which is always at the outermost level
class BaseDrawMode(DrawMode):

    def load(self):
        super().load()

    def tick(self):
        super().tick()

    def event(self, ev):
        super().event(ev)