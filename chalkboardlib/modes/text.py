import pygame
import pygame.gfxdraw
import chalkboardlib.globals as gb
from chalkboardlib.util import key_string, key_character, parse_color
from chalkboardlib.mode import InteractMode
from chalkboardlib.modes.control import register_mode, check_for_mode_switch
from chalkboardlib.objects.textbox import TextBox
from chalkboardlib.history import *

@register_mode("text")
class TextMode(InteractMode):

    font_size = None
    object_buffer = None

    def load(self):
        super().load()
        if TextMode.font_size is None:
            TextMode.font_size = gb.CONFIG["default-font-size"]

    def tick(self):
        super().tick()

        gb.SCREEN.fill(parse_color(gb.CONFIG["colors"]["background"]))
        for obj in gb.OBJECTS:
            obj.draw()

        if self.object_buffer is None:

            height = TextBox.get_font_object(self.font_size*gb.VIEW_SCALE).get_height()
            x, y = pygame.mouse.get_pos()
            if height < gb.SCREEN.get_width()+gb.SCREEN.get_height():
                pygame.gfxdraw.vline(gb.SCREEN, x, y, y+height, gb.ACTIVE_COLOR)

        else:
            if not gb.CONFIG["freeze-text"]:
                dx = gb.MOUSE_X - self.object_buffer.x1
                dy = gb.MOUSE_Y - self.object_buffer.y1
                self.object_buffer.translate(dx, dy)
            self.object_buffer.draw()

    def commit_text(self):

        self.object_buffer.edit_mode = False

        # remove empty lines
        while len(self.object_buffer.text) > 0 and len(self.object_buffer.text[-1]) == 0:
            self.object_buffer.text.pop()
        if len(self.object_buffer.text) > 0:
            add_event(AddObjectsEvent([self.object_buffer]))

        self.object_buffer = None

    def event(self, ev):
        super().event(ev)

        if self.object_buffer is None:
            check_for_mode_switch(ev)

        if ev.type == pygame.MOUSEBUTTONUP:
            if ev.button == 1:

                if self.object_buffer is None:
                    self.object_buffer = TextBox(gb.MOUSE_X, gb.MOUSE_Y, TextMode.font_size, gb.ACTIVE_COLOR)
                else:
                    self.commit_text()

        elif ev.type == pygame.KEYDOWN:
            s = key_string(ev)

            if self.object_buffer is None:

                # color selection
                for i in range(10):
                    if s == gb.CONFIG["controls"][f"color-{i}"]:
                        gb.ACTIVE_COLOR = parse_color(gb.CONFIG["colors"][str(i)])
                        break

                # undo, redo
                if s == gb.CONFIG["controls"]["undo"]:
                    chalkboardlib.history.undo()
                elif s == gb.CONFIG["controls"]["redo"]:
                    chalkboardlib.history.redo()

                # size selection
                elif s == gb.CONFIG["controls"]["increase-size"]:
                    TextMode.font_size *= gb.CONFIG["zoom-ratio"]
                elif s == gb.CONFIG["controls"]["decrease-size"]:
                    TextMode.font_size /= gb.CONFIG["zoom-ratio"]

            # text object control
            else:

                if s == gb.CONFIG["controls"]["write-newline"]:
                    self.object_buffer.newline()

                elif s == "backspace":
                    self.object_buffer.backspace()

                elif s == gb.CONFIG["controls"]["commit-text"]:
                    self.commit_text()

                elif s == gb.CONFIG["controls"]["discard-text"]:
                    self.object_buffer = None

                elif s == gb.CONFIG["controls"]["move-cursor-up"]:
                    self.object_buffer.cursor_up()

                elif s == gb.CONFIG["controls"]["move-cursor-down"]:
                    self.object_buffer.cursor_down()

                elif s == gb.CONFIG["controls"]["move-cursor-left"]:
                    self.object_buffer.cursor_left()

                elif s == gb.CONFIG["controls"]["move-cursor-right"]:
                    self.object_buffer.cursor_right()

                else:
                    self.object_buffer.insert(key_character(ev))

