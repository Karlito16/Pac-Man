#!/usr/bin/python3
# -*- coding: utf-8 -*-

# package name: end_frame


import time
import tkinter
from packages.gui.radio_box import RadioBox, RadioButton


class EndFrame(tkinter.Frame):

    def __init__(self, master, fg, bg, status=False):     # status = self.win
        self.master = master
        self.status = status
        self.fg, self.fg2, self.bg = fg, {True: 'green', False: 'red'}[self.status], bg
        super(EndFrame, self).__init__(master=self.master, bg=self.bg)
        self.font1 = ('verdana', 24, 'bold', 'italic')
        self.font2 = ('verdana', 18)
        self.font3 = ('verdana', 22, 'italic')
        self.shown = False
        self.message_frame = tkinter.Frame(master=self, bg=self.bg)
        self.options_frame = tkinter.Frame(master=self, bg=self.bg)
        self.create_labels()
        self.create_buttons()
        self.message_frame.grid(row=0, column=0)
        self.options_frame.grid(row=1, column=0)
        return

    @property
    def is_shown(self):
        return self.shown

    @is_shown.setter
    def is_shown(self, boolean):
        self.shown = boolean
        return

    def set_commands(self, command1, command2):
        self.button1.set_command(command=command1)
        self.button2.set_command(command=command2)
        return

    def create_labels(self):
        self.label1 = tkinter.Label(master=self.message_frame, font=self.font1, fg=self.fg2,
                                    bg=self.bg)
        self.label2 = tkinter.Label(master=self.message_frame, font=self.font2, fg=self.fg,
                                    bg=self.bg)
        self.label1.grid(row=0, column=0)
        self.label2.grid(row=1, column=0, pady=30)
        return

    def create_buttons(self):
        self.button1 = RadioButton(master=self.options_frame, text='Main Menu', font=self.font3, width=20, bg1=self.bg,
                                   bg2='gray', bg3='white')
        self.button2 = RadioButton(master=self.options_frame, text='Play Again', font=self.font3, width=20, bg1=self.bg,
                                   bg2='gray', bg3='white')
        self.radio_box = RadioBox(btn1=self.button1, btn2=self.button2)
        self.button1.grid(row=0, column=0, padx=50, pady=10)
        # self.button2.grid(row=1, column=0, padx=50, pady=10)
        return

    def update_label_text(self, text1, text2):
        self.label1.config(text=text1)
        self.label2.config(text=text2)
        return

    def on_option_click(self, button):
        # self.radio_box.change(active=button)
        self.button1.set_passive()
        self.button2.set_passive()
        # time.sleep(2.5)     # see this solution! - visual effect only!
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
