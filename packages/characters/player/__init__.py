#!/usr/bin/python3
# -*- coding: utf-8 -*-

# package name: player


import threading
import time
from packages.characters.character import Character
from packages.events import collect_coin


class Player(Character):

    def __init__(self, images_paths, grid, map_, position, track_bg, score_frame, char_bg):
        self.score_frame = score_frame      # temp solution?
        super().__init__(images_paths=images_paths, grid=grid, map_=map_, position=position, track_bg=track_bg, char_bg=char_bg)
        # self.get_image()
        self.lives = 3
        self.points = 0
        self.win = False
        self.time = 0
        return

    def activate(self):
        self.running = True
        threading.Thread(target=self.moving).start()
        return

    def change_direction(self, direction):
        pos_x, pos_y = self.next_possible_move(direction=direction)
        if pos_x in range(0, self.grid.x) and pos_y in range(0, self.grid.y):   # sudden direction change during the side changing (1) - IndexError
            if self.map.map_boolean[pos_x][pos_y]:
                self.direction = direction
        else:
            self.direction = {'e': 'w', 'w': 'e', 'n': 's', 's': 'n'}[self.direction]   # (1)
        return

    def collect_coin(self):  # not used
        x, y = self.last_position
        if self.map.map_food[x][y]:
            self.points += 1
            self.map.map_food[x][y] = False
            self.grid.cell_objects[x][y].coin.grid_forget()
        return

    def moving(self):   # thread
        while self.running:
            try:
                pos_x, pos_y = self.next_possible_move()
                if pos_x in range(0, self.grid.x) and pos_y in range(0, self.grid.y):
                    if self.map.map_boolean[pos_x][pos_y]:
                        self.position_update(x=pos_x, y=pos_y)
                        collect_coin(player=self)
                else:
                    self.change_side(x=pos_x, y=pos_y)
                    collect_coin(player=self)
                time.sleep(self.speed)
                # time.sleep(0.08)
            except RuntimeError:
                raise SystemExit
