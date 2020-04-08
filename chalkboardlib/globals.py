import pygame

# the pygame screen surface
SCREEN = None
FULLSCREEN = False
SCREEN_SIZE = (0, 0)

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

# view settings
VIEW_X_OFFSET = 0.0
VIEW_Y_OFFSET = 0.0
VIEW_SCALE = 1.0

# true mouse coordinates correcting for panning + scaling
MOUSE_X = 0.0
MOUSE_Y = 0.0