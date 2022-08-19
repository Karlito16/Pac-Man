#!/usr/bin/python3
# -*- coding: utf-8 -*-

# package name: radio_box


import tkinter


class RadioBox:

    def __init__(self, btn1, btn2, set_active=False):
        self.button1 = btn1
        self.button2 = btn2
        if set_active:
            self.active = self.button1
            self.passive = self.button2
            self.active.set_active()
            self.passive.set_passive()
        return

    def change(self, active):
        self.active = active
        if self.active == self.button1:
            self.passive = self.button2
        else:
            self.passive = self.button1
        self.active.set_active()
        self.passive.set_passive()
        return

    def deactivate_all(self):
        self.button1.set_passive()
        self.button2.set_passive()
        return


class RadioButton(tkinter.Frame):

    def __init__(self, master, text, font, width, bg1, bg2, bg3, command=None):  # bg1 - passive; bg2 - focus; bg3 - active
        self.master = master
        self.text = text
        self.font = font
        self.width = width
        self.bg1 = bg1
        self.bg2 = bg2
        self.bg3 = bg3
        self.command = command
        super().__init__(self.master, bg=self.bg1)
        self.selected = False

        self.create()

        self.bind('<Enter>', self.on_enter)
        self.button.bind('<Button-1>', self.on_click)
        self.bind('<Leave>', self.on_leave)
        return

    def set_command(self, command):
        self.command = command
        return

    def create(self):
        self.button = tkinter.Label(self, text=self.text, font=self.font, width=self.width, bg=self.bg2)
        self.button.grid(padx=2, pady=2, sticky='nsew')
        return

    def on_enter(self, event):
        self.config(bg=self.bg3)
        return

    def on_click(self, event):
        if not self.selected:
            self.set_active()
        self.command(self)
        return

    def on_leave(self, event):
        if not self.selected:
            self.config(bg=self.bg1)
        return

    def set_active(self):
        self.selected = True
        self.config(bg=self.bg3)
        # self.button.config(bg=self.bg3)
        return

    def set_passive(self):
        self.selected = False
        self.config(bg=self.bg1)
        self.button.config(bg=self.bg2)
        return
