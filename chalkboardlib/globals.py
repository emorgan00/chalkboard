import pygame

# the pygame screen surface
SCREEN = None

# current configuration (e.g. configs/default.json)
CONFIG = {}

# mode, object master lists
MODES = []
OBJECTS = []

UNDO_BUFFER = []
REDO_BUFFER = []

# draw settings
ACTIVE_COLOR = (0, 0, 0)
LINE_THICKNESS = 1