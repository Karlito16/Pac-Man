#!/usr/bin/python3
# -*- coding: utf-8 -*-

# main program


import threading
import time
import os
import random
from packages.characters.enemy import Enemy
from packages.characters.player import Player
from packages.events import collision, ActiveEnemies
from packages.gui.bottom_frame import BottomFrame
from packages.gui.countdown_frame import CountdownFrame
from packages.gui.end_frame import EndFrame
from packages.gui.items import load_item
from packages.gui.grid_frame import GridFrame
from packages.gui.main_menu_frame import MainMenuFrame
from packages.gui.top_frame import TopFrame
from packages.gui.window import Window
from packages.map.interpreter import MapBin, Map


class Frames:

    def __init__(self, master=None):
        self.countdown_frame = CountdownFrame(master=master, fg1=FG, fg2=FG2, bg=BG)
        self.top_frame = TopFrame(master=master, fg=FG, bg=BG)
        self.main_menu_frame = MainMenuFrame(master=master, img_dir=IMG_DIR, items_hscrollbar_dir=ITEMS_HSCROLLBAR_DIR,
                                             img_names=os.listdir(IMG_DIR), cd_frame=self.countdown_frame,
                                             bg=BG)  # master = window because of the bindings! (temp solution??)
        self.grid_frame = GridFrame(master=master, fg=FG, bg=BG)
        self.bottom_frame = BottomFrame(master=master, fg=FG, bg=BG)
        self.end_frame = EndFrame(master=master, fg=FG2, bg=BG)

        self.mmf_s = False
        self.cdf_s = False
        self.gf_s = False
        self.bf_s = False
        self.ef_s = False
        return

    def set_top_frame(self):
        self.top_frame.show(row=0, column=0)    # 10072599999999993
        time.sleep(0.12)
        return

    def set_main_menu_frame(self):
        if self.mmf_s:
            self.main_menu_frame.recover()
        else:
            self.main_menu_frame.show(row=1, column=0)  # 0.00008409999999992035
            self.mmf_s = True
        time.sleep(0.00010)
        return

    def set_countdown_frame(self, message):
        self.countdown_frame.set_message(message=message)
        if self.cdf_s:
            self.countdown_frame.recover()
        else:
            self.countdown_frame.show(row=1, column=0)
            self.cdf_s = True
        time.sleep(0.2)
        threading.Thread(target=self.countdown_frame.countdown).start()
        return

    def set_grid_frame(self):
        if self.gf_s:
            self.grid_frame.recover()
        else:
            self.grid_frame.show(row=1, column=0)   # 0.00004559999999997899
            self.gf_s = True
        time.sleep(0.001)
        return

    def set_bottom_frame(self):
        if self.bf_s:
            self.bottom_frame.recover()
        else:
            self.bottom_frame.show(row=2, column=0)
            self.bf_s = True
        time.sleep(0.0010)
        return

    def set_end_frame(self, player):
        result = int(round(player.points - 1 + (player.time // 2) * (-5) + pow(7, player.lives) + {True: 200, False: 50}[player.win], 0))
        self.end_frame.update_label_text(text1={True: 'You won!', False: 'Game Over!'}[player.win],
                                         text2=f'Result: {result}\nTime: {player.time} seconds')
        if self.ef_s:
            self.end_frame.recover()
        else:
            self.end_frame.show(row=1, column=0)
            self.ef_s = True
        time.sleep(0.0010)
        return


def check_game_loop_thread():
    global game_loop_start_thread
    print(game_loop_start_thread.is_alive())
    return


class GameLoop:

    def __init__(self, reset=False):
        self.program_running = True
        self.respawning = False
        self.init_gui = True
        self.init_characters = True
        self.frames = Frames(master=window)
        self.timing = False

        self.frames.set_top_frame()
        self.frames.set_main_menu_frame()
        self.frames.end_frame.set_commands(command1=self.on_main_menu, command2=self.on_play_again)
        # if not reset:
        #     self.frames = Frames(master=window)
        return

    def start(self):
        # check_game_loop_thread()
        while self.program_running:
            # print('Running Program')
            time.sleep(0.001)        # Prevents the CPU Overheating!

            if not self.frames.main_menu_frame.running:
                self.end()      # program is still running...[RED]
                break

            if self.frames.main_menu_frame.start_countdown:     # Countdown starts here; ENTER has been pressed!
                # print('Countdown started')
                if self.init_gui:
                    self.initialize_gui()

                if self.frames.countdown_frame.start_game:

                    if not self.timing:
                        self.time_started = time.perf_counter()
                        self.timing = True

                    # print('Running Game')
                    time.sleep(0.000001)        # Prevents the CPU Overheating! (2)

                    if self.init_characters:
                        self.show_game_screen()
                        # self.init_characters = False # temp
                        self.initialize_characters()

                    if not self.program_running:
                        self.deactivate_characters()
                        break

                    if self.respawning:
                        self.resume_game()

                    if self.player.points == self.map.total_coins:
                        self.time_finished = time.perf_counter()
                        self.player.time = round(self.time_finished - self.time_started, 2)
                        self.on_win()
                        self.player.points += 1     # hacked! this will stop program from infinitely executing "on_game_over" func

                    if collision(player=self.player, enemies=self.enemies):
                        if self.player.lives == 1:
                            self.time_finished = time.perf_counter()
                            self.player.time = round(self.time_finished - self.time_started, 2)
                            self.on_game_over()
                            # self.player.lives -= 1
                            self.player.x, self.player.y = 0, 0  # hacked! this will stop program from infinitely executing "on_game_over" func
                        else:
                            self.pause_game()

                    if self.active_enemies.new_enemy:
                        self.active_enemies.check(points=self.player.points)
        return

    def initialize_gui(self):
        # print('Init GUI')
        self.frames.main_menu_frame.hide()
        self.load_map(file_path=MAPS_PATH[self.frames.main_menu_frame.selected_index])
        self.frames.grid_frame.set_size(x=int(self.map_bin.x_str), y=int(self.map_bin.y_str))
        # time.sleep(0.5)
        self.frames.grid_frame.create()  # 0.09724500000000003
        time.sleep(0.1)
        self.frames.set_countdown_frame(message=CD_MESSAGE1)
        self.set_map()
        self.init_gui = False
        return

    def initialize_characters(self):
        # print('Init CHARACTERS')
        self.set_enemy()
        self.set_player()
        self.set_keys()
        self.active_enemies = ActiveEnemies(enemies=self.enemies)
        self.init_characters = False
        # self.game_running = True
        return

    def show_game_screen(self):
        # print('Showing game screen')
        self.frames.countdown_frame.hide()
        self.frames.set_grid_frame()
        self.frames.set_bottom_frame()
        # self.frames.grid_frame.recover()
        # self.frames.bottom_frame.recover()
        return

    def show_end_screen(self):
        self.frames.main_menu_frame.start_countdown = False  # new change; error with NoneType (cell_objects)
        self.frames.grid_frame.hide()
        self.frames.bottom_frame.hide()
        self.frames.set_end_frame(player=self.player)
        return

    def end(self):
        self.program_running = False
        time.sleep(0.01)
        try:
            self.deactivate_characters()
        except AttributeError:
            pass
        finally:
            time.sleep(0.1)
            window.destroy()
        return

    def load_map(self, file_path):
        self.map_bin = MapBin(file=open(file=file_path, mode='r', encoding='utf-8'))
        self.bin_values = self.map_bin.get_bin_values()
        self.player_position = self.map_bin.get_player_position()[0]
        self.enemy_positions = self.map_bin.get_enemy_positions()
        self.enemy1_position = self.enemy_positions[0]
        self.inaccessible_area = self.map_bin.get_inaccessible_area()
        return

    def set_map(self):
        self.map = Map(grid=self.frames.grid_frame, bin_values=self.bin_values, inaccessible_area=self.inaccessible_area, en1_pos=self.enemy1_position)
        self.map.create()
        self.map.set_coins()
        return

    def set_enemy(self):
        self.enemies = list()
        colors = ['red', 'pink', 'light blue', 'orange3']
        i = 0
        for position in self.enemy_positions:
            enemy_paths = f'{ITEMS_DIR}\\enemy{position}\\enemy{position}_'.join(['n.png', 's.png', 'e.png', 'w.png'])
            enemy = Enemy(images_paths=None, grid=self.frames.grid_frame, map_=self.map, position=position,
                          track_bg=BG, spawn_position=self.enemy1_position, char_bg=colors[i])
            enemy.show()  # temp hide
            self.enemies.append(enemy)
            i += 1
        return

    def set_player(self):
        paths = f'{PACMAN_IMGS_DIR}\\pacman_'.join(['w.png', 's.png', 'e.png', 'n.png'])
        self.player = Player(images_paths=None,
                             grid=self.frames.grid_frame, map_=self.map, position=self.player_position, track_bg=BG,
                             score_frame=self.frames.bottom_frame.score_frame, char_bg='yellow')
        self.player.activate()
        self.frames.bottom_frame.lives_frame.update_text(self.player.lives)
        # self.player.show()
        return

    def set_keys(self):
        window.bind('<Up>', lambda event: self.player.change_direction(direction='n'))
        window.bind('<Down>', lambda event: self.player.change_direction(direction='s'))
        window.bind('<Left>', lambda event: self.player.change_direction(direction='w'))
        window.bind('<Right>', lambda event: self.player.change_direction(direction='e'))
        return

    def on_win(self):
        # print('win')
        self.deactivate_characters()
        self.player.win = True
        self.show_end_screen()
        # self.game_running = False
        return

    def pause_game(self):
        # print('Game has been paused!')
        self.frames.grid_frame.hide()
        self.frames.bottom_frame.hide()
        self.frames.set_countdown_frame(message=random.choice(RESPAWN_MESSAGES) + f'\n{CD_MESSAGE2}')

        self.deactivate_characters()
        self.player.hide()  # bug! enemy that catches the player in most cases disappears too!
        self.player.x, self.player.y = self.player_position
        self.player.direction = 'w'
        self.player.lives -= 1
        self.frames.bottom_frame.lives_frame.update_text(new_text=self.player.lives)

        self.respawning = True
        return

    def resume_game(self):
        # print('Game has been resumed!')
        self.show_game_screen()
        self.player.show()
        time.sleep(self.player.speed * 1)  # temp!?
        self.activate_characters()
        self.respawning = False
        return

    def on_game_over(self):
        # print('game over')
        self.deactivate_characters()
        self.player.win = False
        self.show_end_screen()
        # self.game_running = False
        return

    def activate_characters(self):
        for enemy in self.active_enemies.active_enemies:
            enemy.activate()
        self.player.activate()
        return

    def deactivate_characters(self):
        for enemy in self.enemies:
            enemy.deactivate()
        self.player.deactivate()
        time.sleep(0.2)
        return

    def on_main_menu(self, button):
        # print('Main Menu')
        # self.frames.end_frame.on_option_click(button=button)
        self.frames.end_frame.hide()
        time.sleep(0.1)
        self.frames.main_menu_frame.restart1()
        self.__init__(reset=True)
        time.sleep(0.2)
        self.frames.set_main_menu_frame()
        time.sleep(0.1)
        return

    def on_play_again(self, button):
        # print('Play Again')
        # self.frames.end_frame.on_option_click(button=button)
        self.frames.end_frame.hide()
        time.sleep(0.1)
        self.__init__(reset=True)
        self.frames.main_menu_frame.start_countdown = True
        return

#
# def check_game_loop_thread():
#     print(game_loop_start_thread.is_alive())
#     return


BG = 'black'
FG = 'gold'
FG2 = 'white'

CWD = os.getcwd()
ITEMS_DIR = f'{CWD}\\items'
PACMAN_IMGS_DIR = f'{ITEMS_DIR}\\pacman'
IMG_DIR = f'{CWD}\\maps\\images\\130x130'
ITEMS_HSCROLLBAR_DIR = f'{CWD}\\packages\\gui\\hscrollbar\\items'
MAPS_PATH = [f'{CWD}\\maps\\{file_name}' for file_name in os.listdir(f'{CWD}\\maps')][2:]
ICON_PATH = f'{ITEMS_DIR}\\icon\\icon.ico'
# print(MAPS_PATH)

CD_MESSAGE1 = 'Game Starts In...'
CD_MESSAGE2 = 'Game Continues In...'
RESPAWN_MESSAGES = [f'Be Careful!!!', 'Ohhh...', 'What Happened?!', 'Are You Okay?!', 'Their Teeth Are Sharp!!!', 'Watch out!!!']


window = Window(bg=BG)
window.geometry('+500+50')  # temp!
window.iconphoto(False, load_item(ICON_PATH))
window.grid_rowconfigure(0, minsize=50)
window.grid_rowconfigure(1, minsize=528)
window.grid_rowconfigure(2, minsize=60)
window.grid_columnconfigure(0, minsize=528)

# top_frame = TopFrame(master=window, fg=FG, bg=BG)
# top_frame.show(row=0, column=0)

game_loop = GameLoop()
game_loop_start_thread = threading.Thread(target=game_loop.start)
game_loop_start_thread.start()

game_loop_end_thread = threading.Thread(target=game_loop.end)

window.protocol("WM_DELETE_WINDOW", game_loop.end)

window.mainloop()
