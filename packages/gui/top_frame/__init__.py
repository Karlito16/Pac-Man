#!/usr/bin/python3
# -*- coding: utf-8 -*-

# package name: top_frame


import tkinter


class TopFrame(tkinter.Frame):

    def __init__(self, master, fg, bg):
        self.master = master
        self.fg, self.bg = fg, bg
        super().__init__(master=self.master, bg=self.bg)
        self.font = ('Calibri', 50, 'bold', 'italic')
        self.text = 'Pac-Man'
        self.letter_boxes = list()
        self.show_text()
        return

    def show_text(self):
        col = 0
        for letter in self.text:
            letter_box = tkinter.Label(master=self, text=letter, font=self.font, fg=self.fg, bg=self.bg)
            letter_box.grid(row=0, column=col, padx=0, pady=0, sticky='e')
            self.letter_boxes.append(letter_box)
            col += 1
        return

    def show(self, row=0, column=0, rowspan=1, columnspan=1, sticky=None):
        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky)
        return

    def hide(self):
        self.grid_forget()
        return
