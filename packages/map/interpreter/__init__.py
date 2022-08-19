#!/usr/bin/python3
# -*- coding: utf-8 -*-

# package name: interpreter


import random


class MapBin:

    def __init__(self, file):
        self.file = file
        self.data = self.file.readlines()
        self.x_str, self.y_str = self.get_size()
        return

    def get_size(self):
        return tuple(self.data[0].split('x'))

    def get_bin_values(self):
        return self.data[1:int(self.x_str) + 1]

    def get_player_position(self):
        return convert_to_tuple([self.data[-3].strip()])

    def get_enemy_positions(self):
        return convert_to_tuple(self.data[-2].strip().split(';'))

    def get_inaccessible_area(self):
        return convert_to_tuple(self.data[-1].strip().split(';') + self.data[-2].strip().split(';'))


def convert_to_tuple(data):
    list_ = list()
    for position in data:
        position = position[1:-1].split(',')
        list_.append((int(position[0]), int(position[1])))
    return list_


class Map:

    def __init__(self, grid, bin_values, inaccessible_area, en1_pos):
        self.grid = grid
        self.bin_values = bin_values
        self.inaccessible_area = inaccessible_area
        self.enemy1_position = en1_pos
        self.map_boolean = [[True for _ in range(self.grid.y)] for _ in range(self.grid.x)]
        self.map_food = [[True for _ in range(self.grid.y)] for _ in range(self.grid.x)]
        self.total_coins = 0
        return

    def create(self):
        x, y = 0, 0
        wall_color = random.choice(['turquoise', 'spring green', 'pale violet red', 'tomato', 'HotPink1', 'maroon', 'navy'])
        # print(self.bin_values)
        for line in self.bin_values:
            for value in line.strip():
                if not int(value):
                    self.grid.cell_objects[x][y].config(bg=wall_color)  # wall
                    self.map_boolean[x][y] = False
                    self.map_food[x][y] = False
                else:
                    self.grid.cell_objects[x][y].config(bg='black')  # food
                y += 1
            x += 1
            y = 0
        return

    def set_coins(self):
        x, y = 0, 0
        for row in self.map_food:
            for boolean in row:
                if boolean and not (x, y) in self.inaccessible_area:
                    self.grid.cell_objects[x][y].show_coin()
                    self.total_coins += 1
                elif boolean:
                    self.map_food[x][y] = False
                    # self.map_boolean[x][y] = False
                if boolean and (x, y) == self.enemy1_position and (x, y) not in self.inaccessible_area:       # temp solution!
                    self.map_food[x][y] = True
                    self.grid.cell_objects[x][y].show_coin()
                    self.total_coins += 1
                y += 1
            x += 1
            y = 0
        return
