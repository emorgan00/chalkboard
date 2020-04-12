import pygame
import time
import chalkboardlib.globals as gb
from chalkboardlib.object import ScreenObject

class TextBox(ScreenObject):

    # static
    font_objects = {}

    font_size = None
    text = None
    edit_mode = True
    create_time = None
    color = (0, 0, 0)

    def __init__(self, x, y, font_size, color):
        super().__init__(x, y, x, y+font_size)
        self.font_size = font_size
        self.color = color
        self.text = [""]

        self.edit_mode = True
        self.create_time = time.time_ns()

    # static
    def get_font_object(size):

        height = int(size*gb.VIEW_SCALE)
        font_id = None
        
        if gb.CONFIG["custom-font"]:
            font_id = (gb.CONFIG["font-path"], height)
            if font_id not in TextBox.font_objects:
                TextBox.font_objects[font_id] = pygame.font.Font(*font_id)

        else:
            font_id = (gb.CONFIG["font-name"], height)
            if font_id not in TextBox.font_objects:
                TextBox.font_objects[font_id] = pygame.font.SysFont(*font_id)

        return TextBox.font_objects[font_id]

    def refresh(self):
        pass

    def newline(self):
        self.text.append("")

    def backspace(self):
        if len(self.text[-1]) == 0:
            if len(self.text) > 1:
                self.text.pop()
        else:
            self.text[-1] = self.text[-1][:-1]

    def insert(self, char):
        self.text[-1] += char
        width, height = TextBox.get_font_object(self.font_size).size(self.text[-1])
        self.x2 = max(self.x2, self.x1+width)
        self.y2 = max(self.y2, self.y1+height*len(self.text))

    def draw(self):

        if not self.onscreen():
            return

        x_s, y_s = self.x1*gb.VIEW_SCALE+gb.VIEW_X_OFFSET, self.y1*gb.VIEW_SCALE+gb.VIEW_Y_OFFSET

        height = int(self.font_size*gb.VIEW_SCALE)
        obj = TextBox.get_font_object(self.font_size)
        for i, line in enumerate(self.text):

            if i == len(self.text)-1 and self.edit_mode:
                elapsed_time = int((time.time_ns()-self.create_time)/300000000)
                if elapsed_time%2 == 0:
                    line = line+"_"

            screen_size = gb.SCREEN.get_size()
            if len(line) > 0:
                expected_size = obj.size(line)
                if expected_size[0] < 4*screen_size[0] and expected_size[1] < 2*screen_size[1]:
                    text_surface = obj.render(line, True, self.color)
                    gb.SCREEN.blit(text_surface, (int(x_s), int(y_s+height*i)))

    def erase(self, x, y, r):
        return super().erase(x, y, r)

