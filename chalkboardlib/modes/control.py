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
                
                if gb.CONFIG["revert-mode"]:
                    if isinstance(gb.MODES[-1], gb.REGISTERED_MODES[name]) and len(gb.MODES) > 1:
                        gb.MODES[-1].kill()
                    else:
                        gb.MODES.append(gb.REGISTERED_MODES[name]())
                        gb.MODES[-1].load()

                        # note: this could cause problems in the future
                        if len(gb.MODES) > 50:
                            gb.MODES.pop(0)

                else:
                    gb.MODES[-1].kill()
                    gb.MODES.append(gb.REGISTERED_MODES[name]())
                    gb.MODES[-1].load()

                break