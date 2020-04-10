import pygame

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