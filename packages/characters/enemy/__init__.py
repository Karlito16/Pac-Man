#!/usr/bin/python3
# -*- coding: utf-8 -*-

# package name: enemy


import threading
import time
from packages.characters.character import Character


class Enemy(Character):

    def __init__(self, images_paths, grid, map_, position, track_bg, spawn_position, char_bg):
        self.spawn_position = spawn_position
        super().__init__(images_paths=images_paths, grid=grid, map_=map_, position=position, track_bg=track_bg, char_bg=char_bg)
        self.direction = 'n'    # easier for them to exit the house
        return

    def activate(self):
        self.running = True
        threading.Thread(target=self.moving).start()
        return

    def show(self):
        self.grid.cell_objects[self.x][self.y].config(bg=self.bg)
        return

    def moving(self):  # thread
        while self.running:
            try:
                pos_x, pos_y = self.get_new_direction()
                self.position_update(pos_x, pos_y)
                time.sleep(self.speed)
            except RuntimeError:
                raise SystemExit
