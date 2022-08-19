#!/usr/bin/python3
# -*- coding: utf-8 -*-

# package name: active_frame


import tkinter


class ActiveFrame(tkinter.Frame):

    def __init__(self, master):
        self.master = master
        super().__init__(master=self.master)
        self.frames = []
        self.shown = False
        return

    @property
    def is_shown(self):
        return self.shown

    @is_shown.setter
    def is_shown(self, boolean):
        self.shown = boolean
        return

    def create(self, frames=None):
        if frames is not None:
            self.frames = frames
        row = 0
        for frame in self.frames:
            frame.grid(row=row, column=0)
            row += 1
        return

    def clear(self):
        for frame in self.frames:
            frame.grid_forget()
        self.frames = []
        return

    def update_(self, frames):
        self.clear()
        self.frames = frames
        self.create()
        return

    def show(self, row=0, column=0, rowspan=1, columnspan=1, sticky=None):
        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky)
        self.is_shown = True
        return

    def hide(self):
        self.grid_forget()
        self.is_shown = False
        return
