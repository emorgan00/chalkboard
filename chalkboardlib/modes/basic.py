import pygame
from chalkboardlib.modes.mode import Mode, BaseMode

class Basic(BaseMode):

    # abstract
    def load(self):
        print('loaded basic')

    # abstract
    def tick(self):
        print('ticking basic')