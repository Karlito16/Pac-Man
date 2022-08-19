#!/usr/bin/python3
# -*- coding: utf-8 -*-

# # package name: items


import tkinter
from PIL import Image, ImageTk


class ImportItem(tkinter.Label):

    def __init__(self, master, items_dir, item_name, resize=()):
        self.master = master
        self.items_dir = items_dir
        self.item_name = item_name
        self.resize = resize
        super().__init__(master=self.master)
        self.item_path = f'{items_dir}\\{item_name}'
        self.image = load_item(img_path=self.item_path, resize=self.resize)
        return

    # def load_item(self, img_path):
    #     load = Image.open(fp=img_path)
    #     if self.resize:
    #         load = load.resize((self.resize[0], self.resize[1]))
    #     render = ImageTk.PhotoImage(image=load)
    #     self.config(image=render)
    #     self.image = render
    #     return

    def show_item(self, row=0, column=0, rowspan=1, columnspan=1, sticky=None):
        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky)
        return

    def hide_item(self):
        self.grid_forget()
        return


def load_item(img_path, resize=()):
    load = Image.open(fp=img_path)
    if resize:
        load = load.resize((resize[0], resize[1]))
    render = ImageTk.PhotoImage(image=load)
    return render
