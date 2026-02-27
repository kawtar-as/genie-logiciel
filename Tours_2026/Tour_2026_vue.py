# -*- coding: ISO-8859-1 -*-
from tkinter import *
import tkinter as tk


class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Tk()
        # On garde votre logique de bouton
        b = tk.Button(self.root, text="Demarrer", command=self.parent.demarrePartie)
        b.pack()
        self.canevas = tk.Canvas(self.root, width=500, height=500)
        self.canevas.bind("<Button-1>", self.getPosTour)
        self.canevas.pack()

    def getPosTour(self, evt):
        x = evt.x / 5
        y = evt.y / 5
        # print ("POS",x,y)
        self.parent.setTour([x, y])

    def afficheModele(self):
        pos = []
        # On assume que nivoActif est initialisé au moment de l'affichage
        for i in self.parent.modele.nivoActif.parcours.noeuds:
            pos.append(i[0] * 5)
            pos.append(i[1] * 5)
        self.canevas.create_line(pos, width=2, fill="black", tags=("chemin",))

    def afficheCreepTourBombe(self):
        self.canevas.delete("creep")
        self.canevas.delete("tour")
        self.canevas.delete("bombe")

        # Logique originale préservée (via nivoActif)
        for i in self.parent.modele.nivoActif.creepsEnCours:
            x1 = i.pos[0] * 5 - 3
            y1 = i.pos[1] * 5 - 3
            x2 = i.pos[0] * 5 + 3
            y2 = i.pos[1] * 5 + 3
            self.canevas.create_oval(x1, y1, x2, y2, width=2, fill="red", tags=("creep",))

        # Logique originale préservée (via nivoActif)
        for i in self.parent.modele.nivoActif.tours:
            x1 = i.pos[0] * 5 - 3
            y1 = i.pos[1] * 5 - 5
            x2 = i.pos[0] * 5 + 3
            y2 = i.pos[1] * 5 + 5
            # print("LOCtour",i.pos,x1,y1,x2,y2)
            self.canevas.create_rectangle(x1, y1, x2, y2, width=1, fill="green", tags=("tour",))