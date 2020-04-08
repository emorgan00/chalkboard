import pygame

# given an event.key, return a string representation
KEY_STRING = {
    pygame.K_BACKSPACE: "\b",
    pygame.K_TAB: "\t",
    pygame.K_SPACE: " ",
    pygame.K_ESCAPE: "^[",

    pygame.K_a: "a",
    pygame.K_b: "b",
    pygame.K_c: "c",
    pygame.K_d: "d",
    pygame.K_e: "e",
    pygame.K_f: "f",
    pygame.K_g: "g",
    pygame.K_h: "h",
    pygame.K_i: "i",
    pygame.K_j: "j",
    pygame.K_k: "k",
    pygame.K_l: "l",
    pygame.K_m: "m",
    pygame.K_n: "n",
    pygame.K_o: "o",
    pygame.K_p: "p",
    pygame.K_q: "q",
    pygame.K_r: "r",
    pygame.K_s: "s",
    pygame.K_t: "t",
    pygame.K_u: "u",
    pygame.K_v: "v",
    pygame.K_w: "w",
    pygame.K_x: "x",
    pygame.K_y: "y",
    pygame.K_z: "z",

    pygame.K_0: "0",
    pygame.K_1: "1",
    pygame.K_2: "2",
    pygame.K_3: "3",
    pygame.K_4: "4",
    pygame.K_5: "5",
    pygame.K_6: "6",
    pygame.K_7: "7",
    pygame.K_8: "8",
    pygame.K_9: "9"
}

def key_string(ev):
    out = ""
    if ev.mod & pygame.KMOD_CTRL:
        out += "ctrl+"
    if ev.mod & pygame.KMOD_SHIFT:
        out += "shift+"
    if ev.key in KEY_STRING:
        out += KEY_STRING[ev.key]
    return out

# accepts a string of format "#000000", returns a pygame-compatible color
def parse_color(s):
    if len(s) != 7 or s[0] != "#":
        raise ValueError(f"Invalid color format: {repr(s)}")
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16))