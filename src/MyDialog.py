#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter.constants import TRUE, END, TOP, BOTH
from tkinter import Button, scrolledtext as tkst, Toplevel


class MyDialog:
    top = None

    def __init__(self, parent, stdout_txt):
        top = self.top = Toplevel(parent)
        stout = tkst.ScrolledText(
            master=top,  # incloem a la finestra top a aquest objecte
            wrap='word',  # Fem que el text sigui de paraules (?)
            width=60,  # caràcters per fila
            height=12,  # línies de text
            bg='beige'  # color de fons
        )
        stout.pack(expand=TRUE, fill=BOTH, side=TOP, padx=8, pady=8)
        stout.delete(1.0, END)  # Fem un clean del text
        stout.insert(END, stdout_txt)  # Inserim el contingut del stdout

        b = Button(top, text="Close", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        self.top.destroy()
