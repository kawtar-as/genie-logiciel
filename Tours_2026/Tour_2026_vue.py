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
        self.creer_fenetre_principale()
        self.creer_carte()
        ##self.canevas = tk.Canvas(self.root, width=500, height=500)
        ##self.canevas.bind("<Button-1>", self.getPosTour)
        ##self.canevas.pack()

    def creer_fenetre_principale(self):
        self.frame_principale = tk.Frame(self.root)
        self.frame_principale.pack()


    def creer_carte(self):
        self.canevas = tk.Canvas(self.frame_principale, width=500, height=500, bg="yellow")
        self.canevas.grid(row=0, column=0)
        
        self.canevas.bind("<Button-1>", self.getPosTour)
        ##self.canevas.pack()



    def creer_boite_menu(self):
        self.frame_tours = tk.Frame(self.frame_principale,width=400, height=500, bg="#444")
        self.frame_tours.grid_propagate(False)
        self.frame_tours.grid(row=0, column=1, sticky="nsew")

        self.label_tour = tk.Label(self.frame_tours, text="tour1", fg="black", bg="#999", font=("Arial", 12))
        self.label_tour.pack(pady=10)

    def getPosTour(self, evt):
        x = evt.x / 5
        y = evt.y / 5
        # print ("POS",x,y)
        self.parent.setTour([x, y])

    def afficheModele(self):


        pos = []
        # On assume que nivoActif est initialis� au moment de l'affichage
        for i in self.parent.modele.nivoActif.parcours.noeuds:
            pos.append(i[0] * 5)
            pos.append(i[1] * 5)
        self.canevas.delete("all")
        self.canevas.create_line(pos, width=2, fill="black", tags=("chemin",))

    def afficheCreepTourBombe(self):
        self.canevas.delete("creep")
        self.canevas.delete("tour")
        self.canevas.delete("bombe")

        # Logique originale pr�serv�e (via nivoActif)
        for i in self.parent.modele.nivoActif.creepsEnCours:
            x1 = i.pos[0] * 5 - 3
            y1 = i.pos[1] * 5 - 3
            x2 = i.pos[0] * 5 + 3
            y2 = i.pos[1] * 5 + 3
            self.canevas.create_oval(x1, y1, x2, y2, width=2, fill="red", tags=("creep",))

        # Logique originale pr�serv�e (via nivoActif)
        for i in self.parent.modele.nivoActif.tours:
            x1 = i.pos[0] * 5 - 3
            y1 = i.pos[1] * 5 - 5
            x2 = i.pos[0] * 5 + 3
            y2 = i.pos[1] * 5 + 5
            # print("LOCtour",i.pos,x1,y1,x2,y2)
            self.canevas.create_rectangle(x1, y1, x2, y2, width=1, fill="green", tags=("tour",))