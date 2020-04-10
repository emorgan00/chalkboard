import pygame
import chalkboardlib.globals as gb

def key_string(ev):

    out = ""
    if ev.mod & pygame.KMOD_CTRL:
        out += "ctrl+"
    if ev.mod & pygame.KMOD_SHIFT:
        out += "shift+"
    out += pygame.key.name(ev.key)
    return out

# accepts a string of format "#000000", returns a pygame-compatible color
def parse_color(s):
    if len(s) != 7 or s[0] != "#":
        raise ValueError(f"Invalid color format: {repr(s)}")
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16))

# returns true if rectangle is at least partially on screen
def onscreen(x1, y1, x2, y2):
    w, h = gb.SCREEN.get_width(), gb.SCREEN.get_height()
    return x1 < w and y1 < h and x2 > 0 and y2 > 0