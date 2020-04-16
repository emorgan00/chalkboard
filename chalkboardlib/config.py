import pygame
from os import path, environ

import chalkboardlib.mode
import chalkboardlib.globals as gb
from chalkboardlib.util import parse_color, key_string, load_configuration

# load all builtin modes
import chalkboardlib.modes.freedraw
import chalkboardlib.modes.erase
import chalkboardlib.modes.text
import chalkboardlib.modes.select

def run_configuration(config_path):

    pygame.init()
    gb.CONFIG_PATH = config_path
    load_configuration(config_path)
    # environ['SDL_VIDEO_CENTERED'] = '1'

    # load various settings
    gb.ACTIVE_COLOR = parse_color(gb.CONFIG["colors"]["1"])
    gb.LINE_THICKNESS = gb.CONFIG["default-line-thickness"]
    gb.SCREEN_SIZE = gb.CONFIG["default-window-size"]
    gb.SCREEN_MODE = pygame.HWSURFACE | pygame.RESIZABLE | pygame.DOUBLEBUF
    if not gb.CONFIG["window-frame"]:
        gb.SCREEN_MODE |= pygame.NOFRAME

    # create screen instance
    gb.SCREEN = pygame.display.set_mode(gb.SCREEN_SIZE, gb.SCREEN_MODE)

    # configure window
    pygame.display.set_caption("Chalkboard")

    icon_path = path.join(path.dirname(__file__), "files/icon.png")
    icon_surface = pygame.image.load(icon_path)
    pygame.display.set_icon(icon_surface)

    # load default mode
    gb.MODES.append(gb.REGISTERED_MODES["freedraw"]())
    gb.MODES[-1].load()
    gb.OBJECTS, gb.UNDO_BUFFER, gb.REDO_BUFFER = [], [], []

    clock = pygame.time.Clock()
    while len(gb.MODES) > 0:

        events = pygame.event.get()
        for ev in events:
            if len(gb.MODES) > 0:
                gb.MODES[-1].event(ev)

        if len(chalkboardlib.globals.MODES) > 0:
            gb.MODES[-1].tick()

        if pygame.display.get_active():
            pygame.display.flip()
        clock.tick(gb.CONFIG["fps-cap"])

    pygame.quit()