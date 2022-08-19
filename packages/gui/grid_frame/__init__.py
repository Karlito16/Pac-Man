#!/usr/bin/python3
# -*- coding: utf-8 -*-

# package name: grid_frame


import tkinter
from packages.gui.items import ImportItem


class GridFrame(tkinter.Frame):

    def __init__(self, master, fg, bg):
        self.master = master
        self.fg, self.bg = fg, bg
        super().__init__(master=self.master, bg=self.bg)
        self.shown = False
        self.cell_objects = None
        return

    @property
    def is_shown(self):
        return self.shown

    @is_shown.setter
    def is_shown(self, boolean):
        self.shown = boolean
        return

    def set_size(self, x, y):
        import time
        self.x, self.y = x, y
        # t1 = time.perf_counter()
        self.cell_objects = [[object for _ in range(self.y)] for _ in range(self.x)]
        # print(f'Time: {time.perf_counter() - t1}\n{self.cell_objects}')
        return

    def create(self):
        for i in range(self.x * self.y):
            x, y = i // self.y, i % self.y
            cell = Cell(master=self, fg=self.fg, bg=self.bg)
            cell.grid(row=x, column=y, padx=5, pady=5, sticky='nsew')
            self.cell_objects[x][y] = cell
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


class Cell(tkinter.Frame):

    def __init__(self, master, fg, bg):
        self.master = master
        self.fg, self.bg = fg, bg
        super().__init__(master=self.master, width=12, height=12, bg=self.bg)
        self.coin = tkinter.Frame(master=self, width=4, height=4, bg=self.fg)
        self.winfo_reqwidth()
        return

    def show_coin(self):
        self.coin.grid(padx=4, pady=4, sticky='nsew')
        return

    def hide_coin(self):
        self.coin.grid_forget()
        return
