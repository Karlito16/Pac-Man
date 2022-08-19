#!/usr/bin/python3
# -*- coding: utf-8 -*-

# package name: events


import random


def collision(player, enemies):
    positions = list()
    for enemy in enemies:
        positions.append((enemy.x, enemy.y))
        positions.append(enemy.last_position)   # very useful!
    if (player.x, player.y) in positions:
        return True
    return False


def collect_coin(player):
    x, y = player.last_position
    if player.map.map_food[x][y]:
        player.points += 1
        player.map.map_food[x][y] = False
        player.grid.cell_objects[x][y].coin.grid_forget()
        player.score_frame.update_text(new_text=player.points)
        return True
        # print_map_coins(matrix=player.map.map_food)
    return


def print_map_coins(matrix):
    for row in matrix:
        print(row)
    print()
    return


class ActiveEnemies:

    def __init__(self, enemies):
        self.enemies = enemies
        self.enemies_boolean = [False for _ in range(len(self.enemies))]
        self.active_enemies = list()
        self.new_enemy = True
        self.c = 2  # random.choice([2, 5, 7, 11])
        return

    def check(self, points):
        index = points // self.c
        if not self.enemies_boolean[index]:
            self.activate_enemy(index=index)
            self.enemies_boolean[index] = True
        if index == len(self.enemies) - 1:
            self.new_enemy = False
        return

    def activate_enemy(self, index):
        enemy = self.enemies[index]
        # enemy.position_update(pos=enemy.spawn_position)   # this is commented because now they can "easily" exit their "home"
        enemy.activate()
        self.active_enemies.append(enemy)
        return
