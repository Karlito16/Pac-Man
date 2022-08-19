#!/usr/bin/python3
# -*- coding: utf-8 -*-

# package name: hscrollbar


import tkinter
from PIL import Image, ImageTk


class HorizontalScrollbar(tkinter.Frame):

    def __init__(self, master, width, range_, items_path, bg):
        self.master = master
        self.width = width
        self.range_ = range_
        self.items_path = items_path
        self.bg = bg
        super().__init__(master=self.master, bg='blue')
        self.track = tkinter.Frame(master=self, bg='blue')
        self.track.grid(padx=30)
        self.bodies = list()
        self.active_bg = 'gray'
        self.confirmed_bg = 'dark blue'
        self.create_arrows()
        self.create_bodies()
        return

    def create_arrows(self):
        for t in [(f'{self.items_path}\\arrow_right.png', 'e'), (f'{self.items_path}\\arrow_left.png', 'w')]:
            load = Image.open(fp=t[0])
            render = ImageTk.PhotoImage(image=load)
            img = tkinter.Label(master=self, image=render, bg='blue')
            # img.bind('<Enter>', lambda event: (self.config(cursor='arrow'), print('a')))
            img.image = render
            img.grid(row=0, column=0, padx=3, sticky=t[1])
        return

    def create_bodies(self):
        body_width = (self.width - 60) / (self.range_ + 1)
        for column in range(self.range_ + 1):
            body = tkinter.Frame(master=self.track, width=body_width / 2, height=20, bg=self.bg)
            body.grid(row=0, column=column, pady=1, sticky='ns')
            self.bodies.append(body)
        return

    def show_body(self, index_):
        self.bodies[index_].config(bg=self.active_bg)
        return

    def hide_body(self, index_):
        self.bodies[index_].config(bg=self.bg)
        return

    def set_confirmed(self, index_):
        self.bodies[index_].config(bg=self.confirmed_bg)
        return
