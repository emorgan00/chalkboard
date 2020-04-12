import pygame
import chalkboardlib.globals as gb
import chalkboardlib.object
import chalkboardlib.history
from chalkboardlib.util import key_string, parse_color, load_configuration

class Mode:

    def __init__(self):
        pass

    # ask to destroy this mode at end of tick
    def kill(self):
        gb.MODES.pop()

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
            gb.SCREEN = pygame.display.set_mode(gb.SCREEN_SIZE, gb.SCREEN_MODE)

        elif ev.type == pygame.KEYDOWN:
            s = key_string(ev)

            if s == gb.CONFIG["controls"]["reload-config"]:
                load_configuration(gb.CONFIG_PATH)

            elif s == gb.CONFIG["controls"]["fullscreen"]:
                if gb.FULLSCREEN:
                    gb.SCREEN = pygame.display.set_mode(gb.SCREEN_SIZE, gb.SCREEN_MODE)
                else:
                    gb.SCREEN = pygame.display.set_mode(gb.CONFIG["fullscreen-window-size"], pygame.HWSURFACE | pygame.FULLSCREEN | pygame.DOUBLEBUF)
                gb.FULLSCREEN = not gb.FULLSCREEN

        elif ev.type == pygame.QUIT:
            self.kill()
            if len(gb.MODES) > 0:
                gb.MODES[-1].event(ev)

# describes a Mode which supports basic interaction with the drawing environment
class InteractMode(Mode):

    def load(self):
        super().load()

        # invisible cursor
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

    def tick(self):
        super().tick()

    def event(self, ev):
        super().event(ev)

        # panning and zooming
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 4:
                gb.VIEW_X_OFFSET -= gb.MOUSE_X*gb.VIEW_SCALE*(gb.CONFIG["zoom-ratio"]-1.0)
                gb.VIEW_Y_OFFSET -= gb.MOUSE_Y*gb.VIEW_SCALE*(gb.CONFIG["zoom-ratio"]-1.0)
                gb.VIEW_SCALE *= gb.CONFIG["zoom-ratio"]
            elif ev.button == 5:
                gb.VIEW_SCALE /= gb.CONFIG["zoom-ratio"]
                gb.VIEW_X_OFFSET += gb.MOUSE_X*gb.VIEW_SCALE*(gb.CONFIG["zoom-ratio"]-1.0)
                gb.VIEW_Y_OFFSET += gb.MOUSE_Y*gb.VIEW_SCALE*(gb.CONFIG["zoom-ratio"]-1.0)

        elif ev.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[1]:
                rx, ry = ev.rel
                gb.VIEW_X_OFFSET += rx
                gb.VIEW_Y_OFFSET += ry