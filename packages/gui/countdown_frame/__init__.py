#!/usr/bin/python3
# -*- coding: utf-8 -*-

# package name: countdown_frame


import time
import tkinter


class CountdownFrame(tkinter.Frame):

    def __init__(self, master, fg1, fg2, bg):       # master must be window
        self.fg1, self.fg2, self.bg = fg1, fg2, bg
        super().__init__(master=master, bg=self.bg)
        self.font = ('verdana', 20, 'italic')
        self.message_label = tkinter.Label(master=self, font=self.font, fg=self.fg2, bg=self.bg)
        self.countdown_label = tkinter.Label(master=self, font=self.font, fg='red', bg=self.bg)
        self.create()
        time.sleep(0.1)
        self.shown = False
        self.start_game = False
        return

    @property
    def is_shown(self):
        return self.shown

    @is_shown.setter
    def is_shown(self, boolean):
        self.shown = boolean
        return

    def set_frame_size(self, width, height):
        self.grid_columnconfigure(0, minsize=width)
        self.grid_rowconfigure(0, minsize=height / 2)
        self.grid_rowconfigure(1, minsize=height / 2)
        return

    def create(self):
        self.message_label.grid(row=0, column=0, pady=30)
        self.countdown_label.grid(row=1, column=0, pady=30)
        return

    def set_message(self, message):
        self.message_label.config(text=f'{message}')
        return

    def countdown(self):    # Thread target!
        self.start_game = False
        try:
            n = 3
            while True:
                self.countdown_label.config(text=n)
                time.sleep(1)
                n -= 1
                if n == -1:
                    self.start_game = True
                    return
        except RuntimeError:    # handles the RuntimeError if user closes the window during the countdown process!
            print('here')
            pass

    def show(self, row=0, column=0, rowspan=1, columnspan=1, sticky=None):
        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky)
        self.is_shown = True
        return

    def recover(self):
        self.grid()
        self.is_shown = True
        return

    def hide(self):
        self.grid_forget()
        self.is_shown = False
        time.sleep(0.01)
        return
