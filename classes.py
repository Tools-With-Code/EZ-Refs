#  ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####


import pygame
import os
from constants import *

pygame.font.init()


class TextInput:
    def __init__(
            self,
            loc=(0, 0),
            size=(100, 50),
            bg_color=(255, 255, 255),
            border_color=(0, 0, 0),
            border_thickness=5,
            initial_string="",
            font_family="",
            font_size=35,
            antialias=True,
            text_color=(0, 0, 0),
            cursor_color=(0, 0, 1),
            repeat_keys_initial_ms=400,
            repeat_keys_interval_ms=35,
            password=False,
            max_string_length=-1
            ):

        self.loc, self.size = loc, size

        self.antialias = antialias
        self.text_color = text_color
        self.font_size = font_size
        self.password = password
        self.input_string = initial_string

        self.rect = pygame.Rect(*loc, *size)
        self.bg_color = bg_color
        self.border_color, self.thickness = border_color, border_thickness

        if not os.path.isfile(font_family):
            font_family = pygame.font.match_font(font_family)

        self.font_object = pygame.font.Font(font_family, font_size)

        self.surface = pygame.Surface((1, 1))
        self.surface.set_alpha(0)

        self.keyrepeat_counters = {}
        self.keyrepeat_intial_interval_ms = repeat_keys_initial_ms
        self.keyrepeat_interval_ms = repeat_keys_interval_ms

        self.cursor_surface = pygame.Surface((int(self.font_size / 20 + 1), self.font_size))
        self.cursor_surface.fill(cursor_color)
        self.cursor_position = len(initial_string)
        self.cursor_visible = True
        self.cursor_switch_ms = 500
        self.cursor_ms_counter = 0

        self.clock = pygame.time.Clock()

        #i = 1
        #surf = self.font_object.render("W"*i, 1, (0, 0, 0))
        #while surf.get_width() < size[0]:
        #    i += 1
        #    surf = self.font_object.render("W"*i, 1, (0, 0, 0))

        #self.max_string_length = i
        self.max_string_length = max_string_length

    def update(self, events, typing):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.cursor_visible = True

                if event.key not in self.keyrepeat_counters:
                    if not event.key == pygame.K_RETURN:
                        self.keyrepeat_counters[event.key] = [0, event.unicode]

                if typing:
                    if event.key == pygame.K_BACKSPACE:
                        self.input_string = (
                            self.input_string[:max(self.cursor_position - 1, 0)]
                            + self.input_string[self.cursor_position:]
                        )

                        self.cursor_position = max(self.cursor_position - 1, 0)
                    elif event.key == pygame.K_DELETE:
                        self.input_string = (
                            self.input_string[:self.cursor_position]
                            + self.input_string[self.cursor_position + 1:]
                        )

                    elif event.key == pygame.K_RETURN:
                        return True

                    elif event.key == pygame.K_RIGHT:
                        self.cursor_position = min(self.cursor_position + 1, len(self.input_string))

                    elif event.key == pygame.K_LEFT:
                        self.cursor_position = max(self.cursor_position - 1, 0)

                    elif event.key == pygame.K_END:
                        self.cursor_position = len(self.input_string)

                    elif event.key == pygame.K_HOME:
                        self.cursor_position = 0

                    elif len(self.input_string) < self.max_string_length or self.max_string_length == -1:
                        self.input_string = (
                            self.input_string[:self.cursor_position]
                            + event.unicode
                            + self.input_string[self.cursor_position:]
                        )
                        self.cursor_position += len(event.unicode)

            elif event.type == pygame.KEYUP:
                if event.key in self.keyrepeat_counters:
                    del self.keyrepeat_counters[event.key]

        for key in self.keyrepeat_counters:
            self.keyrepeat_counters[key][0] += self.clock.get_time()

            if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
                self.keyrepeat_counters[key][0] = (
                    self.keyrepeat_intial_interval_ms
                    - self.keyrepeat_interval_ms
                )

                event_key, event_unicode = key, self.keyrepeat_counters[key][1]
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=event_key, unicode=event_unicode))

        string = self.input_string
        if self.password:
            string = "*" * len(self.input_string)
        self.surface = self.font_object.render(string, self.antialias, self.text_color)

        self.cursor_ms_counter += self.clock.get_time()
        if self.cursor_ms_counter >= self.cursor_switch_ms:
            self.cursor_ms_counter %= self.cursor_switch_ms
            self.cursor_visible = not self.cursor_visible

        if self.cursor_visible:
            cursor_y_pos = self.font_object.size(self.input_string[:self.cursor_position])[0]
            if self.cursor_position > 0:
                cursor_y_pos -= self.cursor_surface.get_width()
            if typing:
                self.surface.blit(self.cursor_surface, (cursor_y_pos, 0))

        self.clock.tick()
        return False

    def draw(self, window):
        pygame.draw.rect(window, self.bg_color, self.rect)
        pygame.draw.rect(window, self.border_color, self.rect, self.thickness)
        window.blit(self.surface, (int(self.loc[0] + self.size[0] / 2 - self.surface.get_width()/2), int(self.loc[1] + self.size[1] / 2 - self.surface.get_height()/2)))

    def get_surface(self):
        return self.surface

    def get_text(self):
        return self.input_string

    def get_cursor_position(self):
        return self.cursor_position

    def set_text_color(self, color):
        self.text_color = color

    def set_cursor_color(self, color):
        self.cursor_surface.fill(color)

    def clear_text(self):
        self.input_string = ""
        self.cursor_position = 0

    def __repr__(self):
        return self.input_string

class Button:
    def __init__(self, loc, size, font, text, bgCol, textCol, borderThickness, borderColor):
        """
        Creates a button which you can draw on the screen and check for clicks.

        :param loc: the x, y position of the button on the screen
        :param size: the width and height of the button
        :param font: a pygame.font.SysFont() instance
        :param text: the text that you want the button to display
        :param bgCol: the color of the button
        :param textCol: the color of the text you want to display
        :param borderThickness: the thickness of the border surrounding the button
        :param borderColor: the color of the border surrounding the button
        """
        self.loc, self.size = loc, size
        self.font = font
        self.text = text
        self.bgCol, self.textCol = bgCol, textCol
        self.thickness, self.borderColor = borderThickness, borderColor
        self.surf = font.render(text, 1, textCol)
        self.rect = pygame.Rect(*loc, *size)

    def ChangeText(self, newText):
        """
        Changes the text that will be displayed on top of the button
        :param newText: the new text that you want to change the current text to.
        :return: None
        """
        self.text = newText
        self.surf = self.font.render(self.text, 1, self.textCol)

    def ChangeTextColor(self, newTextColor):
        """
        Changes the color of the text
        :param newTextColor: the new color of the text.
        :return: None
        """
        self.textCol = newTextColor
        self.surf = self.font.render(self.text, 1, self.textCol)

    def ChangeLoc(self, loc):
        self.loc = loc
        self.rect = pygame.Rect(*loc, *self.size)

    def ChangeBgColor(self, newBgColor):
        """
        Changes the background color of the button
        :param newBgColor: the new background color of the button.
        :return: None
        """
        self.bgCol = newBgColor

    def ChangeBorderColor(self, newBorderColor):
        """
        Changes the border color of the button
        :param newBorderColor: the new border color of the button.
        :return: None
        """
        self.borderColor = newBorderColor

    def ChangeBorderThickness(self, newBorderThickness):
        """
        Changes the thickness of the border
        :param newBorderThickenss: the new thickness of the border of the button.
        :return: None
        """
        self.thickness = newBorderThickness

    def Draw(self, window):
        """
        Draws the button onto the give surface
        :param window: the surface you want to draw the button to.
        :return: None
        """
        pygame.draw.rect(window, self.bgCol, self.rect)
        pygame.draw.rect(window, self.borderColor, self.rect, self.thickness)
        window.blit(self.surf, (int(self.loc[0] + self.size[0]/2 - self.surf.get_width()/2), int(self.loc[1] + self.size[1]/2 - self.surf.get_height()/2)))

    def Clicked(self, events):
        """
        Checks if the button is clicked
        :return: bool value indicating whether or not the button is clicked
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return self.rect.collidepoint(pygame.mouse.get_pos())

class Canvas:
    def __init__(self):
        self.images = []
        self.prevMouseX, self.prevMouseY, self.movingImage = None, None, None

    def Draw(self):
        for image in self.images:
            image.Update(DISPLAY)

    def AddImage(self, image):
        self.images.append(Image([WIDTH / 2 - image.get_width() / 2, HEIGHT / 2 - image.get_height() / 2], [image.get_width(), image.get_height()], image))

    def Update(self, events, direction):
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                image = self.GetImage(event.pos)
                if image is not None:
                    if keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]:
                        if event.button == 4:
                            image.ScaleUp()
                        if event.button == 5:
                            image.ScaleDown()

                    else:
                        if event.button == 4:
                            image.RotateCW()
                        if event.button == 5:
                            image.RotateCCW()

                    if event.button == 1:
                        self.prevMouseX, self.prevMouseY, self.movingImage = *pygame.mouse.get_pos(), image
                

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.prevMouseX is not None and self.prevMouseY is not None and self.movingImage is not None:
                        try:
                            self.movingImage.Move(event.pos[0] - self.prevMouseX, event.pos[1] - self.prevMouseY)
                            self.prevMouseX, self.prevMouseY, self.movingImage = None, None, None
                        except UnboundLocalError:
                            pass

    def GetImage(self, mousePos):
        for image in self.images:
            x, y = image.loc
            width, height = image.size
            mx, my = mousePos
            if x <= mx <= x + width and y <= my <= y + height:
                return image
        return None

class Image:
    def __init__(self, loc, size, image):
        self.loc, self.size = loc, size
        self.center = [self.loc[0] + self.size[0] / 2, self.loc[1] + self.size[1] / 2]
        self.image = image
        self.rot = 0
        self.velocity = 1.05

    def Update(self, window):
        self.loc[0], self.loc[1] = self.center[0] - self.size[0] / 2, self.center[1] - self.size[1] / 2
        self.Draw(window)

    def Draw(self, window):
        window.blit(self.RotCenter(), (round(self.center[0] - self.size[0] / 2), round(self.center[1] - self.size[1] / 2)))

    def RotateCW(self):
        self.rot += 5

    def RotateCCW(self):
        self.rot -= 5

    def ScaleUp(self):
        self.size[0], self.size[1] = self.size[0] * self.velocity, self.size[1] * self.velocity

    def ScaleDown(self):
        self.size[0], self.size[1] = self.size[0] / self.velocity, self.size[1] / self.velocity

    def RotCenter(self):
        loc = self.image.get_rect().center
        rotImg = pygame.transform.rotate(self.image, self.rot)
        rotImg.get_rect().center = loc
        return rotImg

    def Move(self, deltaX, deltaY):
        self.center[0] += deltaX
        self.center[1] += deltaY