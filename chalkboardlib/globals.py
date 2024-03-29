import pygame

# the pygame screen surface
SCREEN = None
FULLSCREEN = False
SCREEN_SIZE = (0, 0)
SCREEN_MODE = pygame.HWSURFACE | pygame.RESIZABLE | pygame.DOUBLEBUF

# current configuration (e.g. configs/default.json)
CONFIG_PATH = ""
CONFIG = {}
REGISTERED_MODES = {}

# mode, object master lists
MODES = []
OBJECTS = []
UNDO_BUFFER = []
REDO_BUFFER = []

# draw settings
ACTIVE_COLOR = (0, 0, 0)

# view settings
VIEW_X_OFFSET = 0.0
VIEW_Y_OFFSET = 0.0
VIEW_SCALE = 1.0

# true mouse coordinates after correcting for panning + scaling
MOUSE_X = 0.0
MOUSE_Y = 0.0