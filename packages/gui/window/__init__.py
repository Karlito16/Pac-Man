#!/usr/bin/python3
# -*- coding: utf-8 -*-

# package name: window


import tkinter


class Window(tkinter.Tk):

    def __init__(self, bg):
        super().__init__()
        self.title('Pac-Man')
        self.resizable(width=False, height=False)
        self.config(bg=bg)
        # icon
        return
