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
    cursor_pos = (0, 0)
    color = (0, 0, 0)

    def __init__(self, x, y, font_size, color):
        super().__init__(x, y, x, y+font_size)
        self.font_size = font_size
        self.color = color
        self.text = [""]

        self.edit_mode = True
        self.create_time = time.time_ns()
        self.cursor_pos = (0, 0)

    # static
    def get_font_object(size):

        height = int(size)
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
        self.refresh_size()

    def refresh_size(self):

        height = TextBox.get_font_object(self.font_size).size(self.text[-1])[1]
        self.x2 = self.x1
        for line in self.text:
            width = TextBox.get_font_object(self.font_size).size(self.text[-1])[0]
            self.x2 = max(self.x2, self.x1+width)
        self.y2 = self.y1+height*len(self.text)

    def newline(self):
        x, y = self.cursor_pos
        self.text.insert(x+1, self.text[x][y:])
        self.text[x] = self.text[x][:y]
        self.cursor_pos = (x+1, 0)
        self.refresh_size()

    def backspace(self):
        x, y = self.cursor_pos
        y = min(y, len(self.text[x]))
        if y == 0:
            if x != 0:
                y = len(self.text[x-1])
                self.text[x-1] += self.text[x]
                self.text.pop(x)
                self.cursor_pos = (x-1, y)
        else:
            self.text[x] = self.text[x][:y-1] + self.text[x][y:]
            self.cursor_pos = (x, y-1)
        self.refresh_size()

    def insert(self, char):
        x, y = self.cursor_pos
        self.text[x] = self.text[x][:y] + char + self.text[x][y:]
        self.cursor_pos = (x, y+len(char))
        self.refresh_size()

    def cursor_left(self):
        x, y = self.cursor_pos
        y = min(y, len(self.text[x]))
        if y == 0:
            if x != 0:
                self.cursor_pos = (x-1, len(self.text[x-1]))
        else:
            self.cursor_pos = (x, y-1)

    def cursor_right(self):
        x, y = self.cursor_pos
        if y == len(self.text[x]):
            if x < len(self.text)-1:
                self.cursor_pos = (x+1, 0)
        elif y < len(self.text[x]):
            self.cursor_pos = (x, y+1)

    def cursor_up(self):
        x, y = self.cursor_pos
        if x != 0:
            self.cursor_pos = (x-1, y)

    def cursor_down(self):
        x, y = self.cursor_pos
        if x != len(self.text)-1:
            self.cursor_pos = (x+1, y)
        else:
            self.cursor_pos = (x, len(self.text[x]))

    def draw(self):

        if not self.onscreen():
            return

        if gb.CONFIG["debug-mode"]:
            self.debug()

        x_s, y_s = self.x1*gb.VIEW_SCALE+gb.VIEW_X_OFFSET, self.y1*gb.VIEW_SCALE+gb.VIEW_Y_OFFSET

        height = self.font_size*gb.VIEW_SCALE
        obj = TextBox.get_font_object(self.font_size*gb.VIEW_SCALE)
        for i, line in enumerate(self.text):

            if i == len(self.text)-1 and self.edit_mode:
                elapsed_time = int((time.time_ns()-self.create_time)/300000000)
                if elapsed_time%2 == 0:
                    
                    subline = self.text[self.cursor_pos[0]][:self.cursor_pos[1]]
                    cursor_x, cursor_y = None, height*self.cursor_pos[0]

                    if gb.CONFIG["smooth-scale-text"] and height < gb.CONFIG["smooth-scale-text-threshold"]:
                        cursor_x = TextBox.get_font_object(self.font_size).size(subline)[0]
                        cursor_x = cursor_x*gb.VIEW_SCALE

                    else:
                        cursor_x = obj.size(subline)[0]

                    if height < gb.SCREEN.get_width()+gb.SCREEN.get_height():
                        pygame.gfxdraw.vline(gb.SCREEN, int(x_s+cursor_x), int(y_s+cursor_y), int(y_s+cursor_y+height), self.color)

            screen_size = gb.SCREEN.get_size()
            if len(line) > 0:
                expected_size = obj.size(line)
                if expected_size[0] < 4*screen_size[0] and expected_size[1] < 2*screen_size[1]:

                    text_surface = obj.render(line, True, self.color)

                    # smooth scaling
                    if gb.CONFIG["smooth-scale-text"] and height < gb.CONFIG["smooth-scale-text-threshold"]:

                        dx_s, dy_s = TextBox.get_font_object(self.font_size).size(line)
                        dx_s, dy_s = dx_s*gb.VIEW_SCALE, dy_s*gb.VIEW_SCALE
                        text_surface = pygame.transform.smoothscale(text_surface, (int(dx_s), int(dy_s)))

                    gb.SCREEN.blit(text_surface, (int(x_s), int(y_s+height*i)))

    def erase(self, x, y, r):
        return super().erase(x, y, r)

