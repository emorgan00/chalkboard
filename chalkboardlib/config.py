import pygame
import json
from os import path

import chalkboardlib.modes.mode
import chalkboardlib.modes.basic

# temporary, perhaps
DEFAULT_SIZE = (800, 500)

def run_configuration(config_path):

    with open(config_path, 'r') as f:
        config_dict = json.load(f)

    pygame.init()

    # configure window
    pygame.display.set_caption("Chalkboard")

    icon_path = path.join(path.dirname(__file__), "files/icon.png")
    icon_surface = pygame.image.load(icon_path)
    pygame.display.set_icon(icon_surface)

    # create screen instance
    screen = pygame.display.set_mode(DEFAULT_SIZE, pygame.HWSURFACE | pygame.RESIZABLE | pygame.DOUBLEBUF)

    # load default mode
    objects = []
    modes = [chalkboardlib.modes.basic.Basic(screen, objects, config_dict)]
    modes[-1].load()

    while len(modes) > 0:

        events = pygame.event.get()
        for ev in events:

            # handle top-level events outside of mode
            if ev.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(ev.dict['size'], pygame.HWSURFACE | pygame.RESIZABLE | pygame.DOUBLEBUF)

            elif ev.type == pygame.QUIT:
                for mode in modes:
                    mode.kill()
                break

            else:
                modes[-1].event(ev)

        if len(modes) > 0:
            modes[-1].tick()
        while len(modes) > 0 and not modes[-1].active:
            modes.pop()

    pygame.quit()