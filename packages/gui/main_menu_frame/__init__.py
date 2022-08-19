#!/usr/bin/python3
# -*- coding: utf-8 -*-

# package name: main_menu_frame


import threading
import time
import tkinter
from packages.gui.hscrollbar import HorizontalScrollbar


FG = 'white'


class MainMenuFrame(tkinter.Frame):

    def __init__(self, master, img_dir, items_hscrollbar_dir, img_names, cd_frame, bg):  # command = countdown_thread
        self.master = master
        self.img_dir = img_dir
        self.items_hscrollbar_dir = items_hscrollbar_dir
        self.img_names = img_names
        self.cd_frame = cd_frame
        self.bg = bg
        super().__init__(master=self.master, bg=self.bg)
        self.shown = False
        self.start_countdown = False
        self.running = True
        # self.gui_init_game = False
        self.img_paths = self.get_img_paths()
        self.buttons = list()
        self.max_index = len(self.img_paths) - 1
        self.min_index = 1
        self.selected_index = 0
        self.set_bindings()
        self.create_buttons()
        self.update_buttons()       # 0.00018
        self.buttons[0].set_selected()
        self.show_text()
        self.create_map_names()
        self.update_map_names()
        self.create_selected_map_text()
        self.update_selected_map_text()
        self.show_hscrollbar()
        return

    @property
    def is_shown(self):
        return self.shown

    @is_shown.setter
    def is_shown(self, boolean):
        self.shown = boolean
        return

    def get_img_paths(self):
        img_paths = list()
        for name in self.img_names:
            img_paths.append(f'{self.img_dir}\\{name}')
        return img_paths

    def set_bindings(self):
        self.master.bind('<Right>', lambda event: self.on_side(event=event, side='Right'))
        self.master.bind('<Left>', lambda event: self.on_side(event=event, side='Left'))
        self.master.bind('<Return>', lambda event: self.on_return(event=event))
        # self.master.bind('<Escape>', lambda event: self.on_escape(event=event))
        return

    def on_side(self, event, side):
        if side == 'Right':
            self.new_index = self.selected_index + 1
            if self.new_index <= self.max_index:
                self.screen_update(side='Right')
        else:
            self.new_index = self.selected_index - 1
            if self.new_index >= 0:
                self.screen_update(side='Left')
        return

    def on_return(self, event):
        self.buttons[self.selected_index].set_confirmed()
        self.hscrollbar.set_confirmed(index_=self.selected_index)
        for event in ['<Right>', '<Left>', '<Return>']:
            self.master.unbind(event)
        self.start_countdown = True
        return

    def on_escape(self, event):
        self.running = False
        return

    # def do_countdown(self):
    #     self.cd_frame.countdown()  # countdown
    #     time.sleep(0.1)     # temp!
    #     self.cd_frame.hide()
    #     self.gui_init_game = True
    #     return

    def screen_update(self, side):   # + for right; - for left
        self.buttons[self.selected_index].set_deselected()
        self.hscrollbar.hide_body(index_=self.selected_index)
        if side == 'Right':
            self.update_buttons()
            self.update_map_names()
            self.selected_index = self.new_index
        else:
            self.selected_index = self.new_index
            self.update_buttons()
            self.update_map_names()
        self.buttons[self.selected_index].set_selected()
        self.update_selected_map_text()
        self.hscrollbar.show_body(index_=self.selected_index)
        return

    def create_buttons(self):
        for img_path in self.img_paths:
            button = MapButton(master=self, image=tkinter.PhotoImage(file=img_path), bg=self.bg)
            self.buttons.append(button)
        return

    def create_map_names(self):
        font = ('verdana', 16)
        self.map_names = list()
        for n in range(1, self.max_index + 2):
            self.map_names.append(tkinter.Label(master=self, text=f'Map {n}', font=font, fg=FG, bg=self.bg))
        return

    def create_selected_map_text(self):
        font = ('verdana', 18)
        self.selected_map_text = tkinter.Label(master=self, font=font, fg=FG, bg=self.bg)
        self.selected_map_text.grid(row=4, column=0, columnspan=self.max_index + 1)
        return

    def update_buttons(self):
        for t in enumerate(self.buttons):
            button_index = t[0]
            if button_index in (self.selected_index, self.selected_index + 1):
                t[1].grid(row=1, column=button_index, padx=10, pady=20, sticky='nsew')
            else:
                t[1].grid_forget()
        return

    def update_map_names(self):
        for t in enumerate(self.map_names):
            map_index = t[0]
            if map_index in (self.selected_index, self.selected_index + 1):
                t[1].grid(row=2, column=map_index)
            else:
                t[1].grid_forget()
        return

    def update_selected_map_text(self):
        self.selected_map_text.config(text=f'Map {self.selected_index + 1}')
        return

    def show_text(self):
        font = ('verdana', 20)
        font_small = ('verdana', 10, 'italic')
        tkinter.Label(master=self, text='Select the map:', font=font, fg=FG, bg=self.bg).grid(row=0, column=0,
                                                                                              columnspan=self.max_index + 1,
                                                                                              padx=10, pady=10,
                                                                                              sticky='w')
        tkinter.Label(master=self, text='v1.1', font=font_small, fg=FG, bg=self.bg).grid(row=6, column=0,
                                                                                         columnspan=self.max_index + 1,
                                                                                         padx=10, pady=5,
                                                                                         sticky=None)
        # self.bottom_text = tkinter.Label(master=self, text='Press ENTER to play!\nPress ESC to exit!', font=font, fg=FG, bg=self.bg)
        self.bottom_text = tkinter.Label(master=self, text='Press ENTER to play!\n', font=font, fg=FG, bg=self.bg)
        self.bottom_text.grid(row=5, column=0, columnspan=self.max_index + 1, pady=20)
        return

    def show_hscrollbar(self):
        self.hscrollbar = HorizontalScrollbar(master=self, width=self.winfo_screenmmwidth(), range_=self.max_index,
                                              items_path=self.items_hscrollbar_dir, bg=self.bg)
        self.hscrollbar.grid(row=3, column=0, pady=20, columnspan=self.max_index + 1)
        self.hscrollbar.show_body(index_=0)
        return

    def grid_buttons(self):  # not used!
        self.buttons[self.selected_index].grid(row=1, column=self.selected_index, padx=10, pady=20, sticky='nsew')
        self.buttons[self.selected_index + 1].grid(row=1, column=self.selected_index + 1, padx=10, pady=20, sticky='nsew')
        return

    def clear_buttons(self):  # not used!
        self.buttons[self.selected_index - 2].grid_forget()
        self.buttons[self.selected_index - 1].grid_forget()
        return

    def clear_all_buttons(self):  # not used!
        for button in self.buttons:
            button.grid_forget()
        return

    def restart1(self):
        self.start_countdown = False
        # self.gui_init_game = False
        self.selected_index = 0
        self.set_bindings()
        self.update_buttons()
        self.buttons[0].set_selected()
        self.update_map_names()
        self.update_selected_map_text()
        self.hscrollbar.show_body(index_=self.selected_index)
        return

    def show(self, row=0, column=0, rowspan=1, columnspan=1, sticky=None):
        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky)
        self.is_shown = True
        return

    def recover(self):
        self.grid()
        self.is_shown = True
        return

    def hide(self):
        self.grid_remove()
        self.is_shown = False
        return


class MapButton(tkinter.Frame):

    def __init__(self, master, image, bg):
        self.master = master
        self.image = image
        super().__init__(master=self.master, bg=bg)
        self.selected = False
        self.deselected_bg = bg
        self.selected_bg = 'gray'
        self.confirmed_bg = 'dark blue'
        self.img_holder = tkinter.Frame(master=self, bg=bg)
        tkinter.Label(master=self.img_holder, image=self.image, bg=bg).grid()
        self.img_holder.grid(padx=10, pady=10, sticky='nsew')
        return

    def set_selected(self):
        self.selected = True
        self.config(bg=self.selected_bg)
        return

    def set_deselected(self):
        self.selected = False
        self.config(bg=self.deselected_bg)
        return

    def set_confirmed(self):
        self.config(bg=self.confirmed_bg)
        return
