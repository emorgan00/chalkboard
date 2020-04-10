import pygame
import commentjson
from os import path, environ

import chalkboardlib.mode
import chalkboardlib.modes.freedraw
import chalkboardlib.globals as gb
from chalkboardlib.util import parse_color

def run_configuration(config_path):

    with open(config_path, 'r') as f:
        gb.CONFIG = commentjson.load(f)

    # load various settings
    gb.ACTIVE_COLOR = parse_color(gb.CONFIG["colors"]["1"])
    gb.LINE_THICKNESS = gb.CONFIG["default-line-thickness"]
    gb.SCREEN_SIZE = gb.CONFIG["default-window-size"]
    gb.SCREEN_MODE = pygame.HWSURFACE | pygame.RESIZABLE | pygame.DOUBLEBUF
    if not gb.CONFIG["window-frame"]:
        gb.SCREEN_MODE |= pygame.NOFRAME

    pygame.init()
    # environ['SDL_VIDEO_CENTERED'] = '1'

    # configure window
    pygame.display.set_caption("Chalkboard")

    icon_path = path.join(path.dirname(__file__), "files/icon.png")
    icon_surface = pygame.image.load(icon_path)
    pygame.display.set_icon(icon_surface)

    # create screen instance
    gb.SCREEN = pygame.display.set_mode(gb.SCREEN_SIZE, gb.SCREEN_MODE)

    # load default mode
    gb.MODES.append(chalkboardlib.modes.freedraw.FreeDrawMode())
    gb.MODES[-1].load()
    gb.OBJECTS, gb.UNDO_BUFFER, gb.REDO_BUFFER = [], [], []

    while len(gb.MODES) > 0:

        events = pygame.event.get()
        for ev in events:
            if len(gb.MODES) > 0:
                gb.MODES[-1].event(ev)

        if len(chalkboardlib.globals.MODES) > 0:
            gb.MODES[-1].tick()

        pygame.display.flip()

    pygame.quit()