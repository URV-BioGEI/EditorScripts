#!/usr/bin/env python
# -*- coding: utf-8 -*-

class MyDialog:
    top = None

    def __init__(self, parent, stdout_txt):
        top = self.top = Toplevel(parent)
        stout = tkst.ScrolledText(
            master=top,  # incloem a la finestra fout aquest objecte
            wrap='word',  # Fem que el text sigui de paraules (?)
            width=60,  # carácters per fila
            height=12,  # linies de text
            bg='beige'  # color de fons
        )
        stout.pack(expand=TRUE, fill=BOTH, side=TOP, padx=8, pady=8)
        stout.delete(1.0, END)  # Fem un clean del text
        stout.insert(END, stdout_txt)  # Insertem el contingut del stdout

        b = Button(top, text="Close", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        self.top.destroy()