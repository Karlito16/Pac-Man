#!/usr/bin/python3
# -*- coding: utf-8 -*-

# package name: layer


import tkinter


class Layer(tkinter.Frame):

    def __init__(self, master):
        self.master = master
        super().__init__(master=self.master)
        return

    def show(self, row=0, column=0, rowspan=1, columnspan=1, padx=None, pady=None, sticky=None):
        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=padx, pady=pady, sticky=sticky)
        return

    def hide(self):
        self.grid_forget()
        return
