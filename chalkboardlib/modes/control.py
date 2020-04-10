import pygame
from chalkboardlib.util import key_string
import chalkboardlib.globals as gb

# use as decorator on a mode class to make it reachable by hotkey
def register_mode(name):

    def class_wrapper(mode):
        gb.REGISTERED_MODES[name] = mode
        return mode

    return class_wrapper

def check_for_mode_switch(ev):

    if ev.type == pygame.KEYDOWN and len(gb.MODES) > 0:
        s = key_string(ev)

        for name in gb.REGISTERED_MODES:
            if s == gb.CONFIG["controls"][name]:
                gb.MODES[-1].kill()
                gb.MODES.append(gb.REGISTERED_MODES[name]())
                print("switched to", name)
                break