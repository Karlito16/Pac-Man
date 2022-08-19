#!/usr/bin/python3
# -*- coding: utf-8 -*-

# package name: character


import os
import random
from PIL import Image, ImageTk


class Character:

    ACTIVE_POSITIONS = {}

    def __init__(self, images_paths, grid, map_, position, track_bg, char_bg=None):
        if images_paths is None:
            self.bg = char_bg
        else:
            self.images_paths = images_paths
            self.images_dict = load_images(img_paths=self.images_paths, _resize=(30, 30))
        self.grid = grid
        self.map = map_
        self.x, self.y = position
        self.track_bg = track_bg
        self.transparent_img = load_images  # (img_paths=[f'{os.getcwd()}\\packages\\characters\\character\\transparent.png'], _resize=(30, 30))
        self.direction = 'w'  # s e w
        # self.get_image()
        self.speed = 0.3
        self.running = False
        self.last_position = None
        Character.ACTIVE_POSITIONS[self] = position
        return

    def show(self):
        self.grid.cell_objects[self.x][self.y].config(bg=self.bg)
        return

    def hide(self):
        x, y = self.last_position
        self.grid.cell_objects[self.x][self.y].config(bg=self.track_bg)
        self.grid.cell_objects[x][y].config(bg=self.track_bg)       # maybe fixes issue when player's character stays shown despite being eaten
        return

    def deactivate(self):
        self.running = False
        return

    def position_update(self, x=None, y=None, pos=None):
        if pos is not None:
            x, y = pos
        if self.map.map_food[self.x][self.y]:
            self.grid.cell_objects[self.x][self.y].show_coin()
        self.grid.cell_objects[self.x][self.y].config(bg=self.track_bg)
        self.last_position = (self.x, self.y)
        self.x = x
        self.y = y
        Character.ACTIVE_POSITIONS[self] = (self.x, self.y)

        for character in Character.ACTIVE_POSITIONS:    # here we check if anyone was placed at the same position as the last position of the self object; useful for enemies during "sleep mode"
            pos = Character.ACTIVE_POSITIONS[character]
            if pos == self.last_position:
                character.show()

        if self.map.map_food[self.x][self.y]:
            self.grid.cell_objects[self.x][self.y].hide_coin()
        self.grid.cell_objects[self.x][self.y].config(bg=self.bg)

##        for character in Character.ACTIVE_POSITIONS:
##            if character == self or Character.ACTIVE_POSITIONS[character] == (self.x, self.y):
##                character.show()
##            # x, y = Character.ACTIVE_POSITIONS[character]
##            # self.grid.cell_objects[x][y].config(bg=character.bg)
        
        return

    def next_possible_move(self, direction=None):
        directions = {
            'n':
                (self.x - 1, self.y),
            'e':
                (self.x, self.y + 1),
            's':
                (self.x + 1, self.y),
            'w':
                (self.x, self.y - 1)
        }
        if direction is None:
            pos_x, pos_y = directions[self.direction]
        else:
            pos_x, pos_y = directions[direction]
        return pos_x, pos_y

    def get_new_direction(self):
        possible_direction = 'nsew' + 5 * self.direction  # more chances to continue with the latest direction
        while True:
            self.direction = random.choice(possible_direction)
            pos_x, pos_y = self.next_possible_move()
            if pos_x in range(0, self.grid.x) and pos_y in range(0, self.grid.y):
                if self.map.map_boolean[pos_x][pos_y]:
                    break
                else:
                    pass  # something to do with new direction probability etc.
            else:
                self.change_side(x=pos_x, y=pos_y)
        return pos_x, pos_y

    def change_side(self, x, y):
        self.grid.cell_objects[self.x][self.y].config(bg=self.track_bg)
        if x < 0:
            x = self.grid.x - 1
        elif x == self.grid.x:
            x = 0
        elif y < 0:
            y = self.grid.y - 1
        else:
            y = 0
        self.position_update(x=x, y=y)
        return

    def get_image(self):
        for image_name in self.images_dict:
            if image_name.split('_')[1] == self.direction:
                self.image = self.images_dict[image_name]
                return
        return


def load_images(img_paths, _resize=()):
    _dict = dict()
    for path in img_paths:
        load = Image.open(fp=path)
        if _resize:
            load = load.resize((_resize[0], _resize[1]))
        render = ImageTk.PhotoImage(image=load)
        _dict[path.split('\\')[-1].strip('.png')] = render
    # print(_dict)
    # self.config(image=render)
    # self.image = render
    return _dict
