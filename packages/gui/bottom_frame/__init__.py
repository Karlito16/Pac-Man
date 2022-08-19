#!/usr/bin/python3
# -*- coding: utf-8 -*-

# package name: bottom_frame


import tkinter


class BottomFrame(tkinter.Frame):

    def __init__(self, master, fg, bg):
        self.master = master
        self.fg = fg
        self.bg = bg
        super().__init__(master=self.master, bg=self.bg)
        self.shown = False
        self.master.update()
        self.width = int(self.master.winfo_width()) / 2
        self.score_frame = SubFrame(master=self, text='Score: ', width=self.width, fg=self.fg, bg=self.bg)
        self.lives_frame = SubFrame(master=self, text='Lives: ', width=self.width, fg=self.fg, bg=self.bg)
        self.score_frame.grid(row=0, column=0, sticky='w')
        self.lives_frame.grid(row=0, column=1, sticky='w')
        self.grid_columnconfigure(index=0, minsize=self.width)
        self.grid_columnconfigure(index=1, minsize=self.width)
        return

    @property
    def is_shown(self):
        return self.shown

    @is_shown.setter
    def is_shown(self, boolean):
        self.shown = boolean
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


class SubFrame(tkinter.Frame):

    def __init__(self, master, text, width, fg, bg):
        self.master = master
        self.text = text
        self.width = width
        self.fg, self.bg = fg, bg
        self.font = ('verdana', 20, 'bold')
        super().__init__(master=self.master, bg=self.bg)
        self.create_text()
        self.show_text()
        return

    def create_text(self):
        self.label = tkinter.Label(master=self, text=self.text, font=self.font, fg=self.fg, bg=self.bg)
        return

    def show_text(self):
        self.label.grid(padx=20, pady=10)
        return

    def update_text(self, new_text):
        self.label.config(text=f'{self.text}{new_text}')
        return

    def hide_text(self):
        self.label.grid_forget()
        return
