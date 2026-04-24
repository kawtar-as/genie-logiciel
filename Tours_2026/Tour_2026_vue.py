# -*- coding: ISO-8859-1 -*-
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk


class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Tk()
        self.tour_active = None
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
        self.canevas = tk.Canvas(self.frame_principale, width=500, height=500)
        self.canevas.grid(row=1, column=0)
        self.chemin1 = Image.open("Tours_2026/chemin1.png")
        self.resize = self.chemin1.resize((500, 500), Image.Resampling.LANCZOS)
        self.chmin_img = ImageTk.PhotoImage(self.resize)

    def resizeImages(self, chemin, largeur, hauteur):
        try:
            raw_img = Image.open(chemin)
            resized_img = raw_img.resize((largeur, hauteur), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(resized_img)
        except Exception as e:
            print(f"Error image {chemin}: {e}")
            return None

    def creer_boite_menu(self):
        self.frame_tours = tk.Frame(self.frame_principale, width=200, height=500, bg="#444")
        self.frame_tours.grid_propagate(FALSE)
        self.frame_tours.grid(row=1, column=2, sticky="nsew")

        chemin_routes = [
            "images/tour1.png",
            "images/tour2.png",
            "images/tour3.png",
            "images/tour4.png",
            "images/tour5.png",
            "images/tour6.png",

        ]
        
        self.photo_tours = []
        self.btns_tours = []

        for i in range(len(chemin_routes)):
            photo = self.resizeImages(chemin_routes[i], 50, 50)
            
            if photo:
                self.photo_tours.append(photo)
                # Creation btn
                btn = tk.Button(
                    self.frame_tours, 
                    image=photo, 
                    command= lambda i=i : self.image_selectionne(i),
                    borderwidth=0,
                    bg="#999",
                    activebackground="#777",
                    cursor="hand2"
                )
                lin = i // 2
                col = i % 2
                
                btn.grid(row=lin, column=col, padx=10, pady=10)
    
                self.btns_tours.append(btn)
                setattr(self, f"btn_tour{i}", btn)

        

        
       
        
        self.frame_infomations = tk.Frame(self.frame_principale,width=300, height=50, bg="#444")
        self.frame_infomations.grid_propagate(False)
        self.frame_infomations.grid(row=0, column=0,columnspan=4 ,sticky="nsew")

        self.label_vie = tk.Label(self.frame_infomations, text="vie:" + str(self.parent.modele.vie), fg="black", bg="#7D9EC0", font=("Arial", 12))
        self.label_vie.grid(row=0,column=0,sticky="ew")
        self.label_vie.grid(pady=10,padx=10)

        self.label_argent = tk.Label(self.frame_infomations, text="Argent:" + str(self.parent.modele.cash), fg="black", bg="#7D9EC0", font=("Arial", 12))
        self.label_argent.grid(row=0,column=1,sticky="ew")
        self.label_argent.grid(pady=10,padx=10)

        self.label_score = tk.Label(self.frame_infomations, text="Score:" + str(0), fg="black", bg="#7D9EC0", font=("Arial", 12))
        self.label_score.grid(row=0,column=2,sticky="ew")
        self.label_score.grid(pady=10,padx=10)

        self.label_niveau = tk.Label(self.frame_infomations, text="Niveau:" + str(self.parent.modele.nivo), fg="black", bg="#7D9EC0", font=("Arial", 12))
        self.label_niveau.grid(row=0,column=3,sticky="ew")
        self.label_niveau.grid(pady=10,padx=10)
        #pour le bouttons
        self.frame_allbtns = tk.Menu(self.frame_infomations,tearoff=0)
        self.frame_allbtns.add_command(label="Start")
        self.frame_allbtns.add_command(label="Pause", command=self.parent.pause)
        self.frame_allbtns.add_command(label="Start game",command = self.parent.modele.demarrePartie)
        #ajouter les commande frame_allbtns
        self.frame_options = tk.Button(self.frame_infomations, text="Game options")
        self.frame_options.grid(row=0,column=4,sticky="ew")
        self.frame_options.grid(pady=10,padx=10)
        # lier le click avec le btnss
        self.frame_options.config(command=self.afficher_options)

        self.btn_vague_automatique = tk.Button(self.frame_infomations, text = "vague automatique", bg="green")
        self.btn_vague_automatique .grid(row=0,column=5,sticky="ew")
        self.btn_vague_automatique .grid(pady=10,padx=10)
       
    def missile(self):
        item = self.parent.modele.missile
        for i in item:
                self.canevas.create_rectangle(
                i.x - i.taille_x,
                i.y - i.taille.y,
                i.x + i.taille.x,
                i.y + i.taille.y,
                fill="yellow"
                )

    def getPosTour(self, evt, x, y):
        if self.tour_active:
            # On place l'image exactement aux coordonnées du centre de la case (x, y)
            self.canevas.create_image(x, y, image=self.tour_active, tags=("tour_img",))
            
            # On informe le contrôleur (on divise par 5 car ton modèle semble scaler par 5)
            self.parent.setTour(x / 5, y / 5)

    def afficheModele(self):
        self.canevas.delete("all")
        self.canevas.delete("all")

        self.canevas.create_image(0, 0, image=self.chmin_img, anchor=tk.NW)
        pos = []
        # On assume que nivoActif est initialis� au moment de l'affichage
        self.canevas.create_image(0, 0, image=self.chmin_img, anchor=tk.NW)

    def afficherCasesVides(self):
        for i in self.parent.modele.nivoActif.emplacement.cases:
            id = self.parent.modele.creerId()
            self.canevas.create_rectangle((i[0] - 10) * 2, (i[1] - 10) * 2 , (i[0] + 10) * 2 , (i[1] + 10) * 2, fill="black", tags=("cases", id))
            self.canevas.tag_bind(id, "<Button-1>", lambda event, x=i[0]*2, y=i[1]*2 : self.getPosTour(event, x, y))

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
            x1 = i.pos_x * 5 - 3
            y1 = i.pos_y * 5 - 5
            x2 = i.pos_x * 5 + 3
            y2 = i.pos_y * 5 + 5
            

    def afficher_options(self):
        x= self.frame_options.winfo_rootx()
        y= self.frame_options.winfo_rooty()
        self.frame_allbtns.post(x,y)
 
    def image_selectionne(self,i):
        self.tour_active = self.photo_tours[i]

    # def pause(self,evt):
    #     self.parent.pause(evt)