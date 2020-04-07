import pygame
import json
from os import path

import chalkboardlib.mode
import chalkboardlib.modes.freedraw
import chalkboardlib.globals as gb

# temporary, perhaps
DEFAULT_SIZE = (800, 500)

def run_configuration(config_path):

    with open(config_path, 'r') as f:
        gb.CONFIG = json.load(f)

    pygame.init()

    # configure window
    pygame.display.set_caption("Chalkboard")

    icon_path = path.join(path.dirname(__file__), "files/icon.png")
    icon_surface = pygame.image.load(icon_path)
    pygame.display.set_icon(icon_surface)

    # create screen instance
    gb.SCREEN = pygame.display.set_mode(DEFAULT_SIZE, pygame.HWSURFACE | pygame.RESIZABLE | pygame.DOUBLEBUF)

    # load default mode
    gb.MODES.append(chalkboardlib.modes.freedraw.FreeDrawMode())

    while len(gb.MODES) > 0:

        events = pygame.event.get()
        for ev in events:
            if len(gb.MODES) > 0:
                gb.MODES[-1].event(ev)

        if len(chalkboardlib.globals.MODES) > 0:
            gb.MODES[-1].tick()

        pygame.display.flip()

    pygame.quit()