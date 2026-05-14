# -*- coding: ISO-8859-1 -*-
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk


class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Tk()
        self.tour_active = None
        self.frames = {}
        self.frameActif = None

        self.creerFrames()
        self.changerFrame("splash")
        

         # On garde votre logique de bouton
        # b = tk.Button(self.root, text="Demarrer", command=self.parent.demarrePartie)
        # b.pack()
        
        ## Splash est l'écran d'acceuil quand on lance le jeu
        
      
        ##self.canevas = tk.Canvas(self.root, width=500, height=500)
        ##self.canevas.bind("<Button-1>", self.getPosTour)
        ##self.canevas.pack()


    def creerFrames(self):
        principal = self.creer_fenetre_principale()
        self.frames["principal"] = principal
        splash = self.creer_splash()
        self.frames["splash"] = splash
    
    def changerFrame(self, nouveauFrame):
        if self.frameActif:
            self.frameActif.pack_forget()
        self.frameActif = self.frames[nouveauFrame]
        self.frameActif.pack()


       
    def creer_fenetre_principale(self):
        self.frame_principale = tk.Frame(self.root)
        
        # ---------------------------------------------------------
        # 1. BARRE D'INFORMATIONS (En haut - Ligne 0)
        # ---------------------------------------------------------
        self.frame_infomations = tk.Frame(self.frame_principale, width=800, height=50, bg="#2e2f31")
        self.frame_infomations.grid_propagate(False)
        # S'étend sur deux colonnes pour couvrir le jeu et le menu des tours
        self.frame_infomations.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Combine grid() arguments into a single line to prevent Tkinter from overwriting them
        self.label_vie = tk.Label(self.frame_infomations, text="Vie: --", fg="black", bg="#7D9EC0", font=("Arial", 12))
        self.label_vie.grid(row=0, column=0, sticky="ew", pady=10, padx=10)

        self.label_argent = tk.Label(self.frame_infomations, text="Argent: --", fg="black", bg="#7D9EC0", font=("Arial", 12))
        self.label_argent.grid(row=0, column=1, sticky="ew", pady=10, padx=10)

        self.label_score = tk.Label(self.frame_infomations, text="Score: 0", fg="black", bg="#7D9EC0", font=("Arial", 12))
        self.label_score.grid(row=0, column=2, sticky="ew", pady=10, padx=10)

        self.label_niveau = tk.Label(self.frame_infomations, text="Niveau: --", fg="black", bg="#7D9EC0", font=("Arial", 12))
        self.label_niveau.grid(row=0, column=3, sticky="ew", pady=10, padx=10)

        # Menu caché d'options
        self.frame_allbtns = tk.Menu(self.frame_infomations, tearoff=0)
        self.frame_allbtns.add_command(label="Start")
        self.frame_allbtns.add_command(label="Pause", command=self.parent.pause)
        
        # Protection au cas où le modèle ne serait pas encore chargé
        if hasattr(self.parent, 'modele'):
            self.frame_allbtns.add_command(label="Start game", command=self.parent.modele.demarrePartie)

        self.frame_options = tk.Button(self.frame_infomations, text="Game options", command=self.afficher_options)
        self.frame_options.grid(row=0, column=4, sticky="ew", pady=10, padx=10)

        self.btn_vague_automatique = tk.Button(self.frame_infomations, text="Vague automatique", bg="green")
        self.btn_vague_automatique.grid(row=0, column=5, sticky="ew", pady=10, padx=10)
        
        # ---------------------------------------------------------
        # 2. CANEVAS DU JEU (En bas à gauche - Ligne 1, Colonne 0)
        # ---------------------------------------------------------
        self.canevas = tk.Canvas(self.frame_principale, width=500, height=500, bg="black")
        self.canevas.grid(row=1, column=0)
        
        # Le Try/Except empêche le jeu de crasher si l'image manque
        try:
            self.chemin1 = Image.open("Tours_2026/chemin1.png")
            self.resize = self.chemin1.resize((500, 500), Image.Resampling.LANCZOS)
            self.chmin_img = ImageTk.PhotoImage(self.resize)
            self.canevas.create_image(0, 0, image=self.chmin_img, anchor=tk.NW)
        except Exception as e:
            print(f"Erreur de fond de carte: {e}")

        # ---------------------------------------------------------
        # 3. MENU DES TOURS (En bas à droite - Ligne 1, Colonne 1)
        # ---------------------------------------------------------
        self.frame_tours = tk.Frame(self.frame_principale, width=200, height=500, bg="#2e2f31")
        self.frame_tours.grid_propagate(False) # Correction : False avec une majuscule
        self.frame_tours.grid(row=1, column=1, sticky="nsew") # Changé à la colonne 1

        chemin_routes = [
            "images/tour1.png", "images/tour2.png", "images/tour3.png",
            "images/tour4.png", "images/tour5.png", "images/tour6.png"
        ]
        
        self.photo_tours = []
        self.btns_tours = []

        for i in range(len(chemin_routes)):
            photo = self.resizeImages(chemin_routes[i], 50, 50)
            
            if photo:
                self.photo_tours.append(photo)
                btn = tk.Button(
                    self.frame_tours, 
                    image=photo, 
                    command=lambda i=i: self.image_selectionne(i),
                    borderwidth=0,
                    bg="#999",
                    activebackground="#777",
                    cursor="hand2"
                )
                
                # Calcule la ligne et la colonne (2 colonnes max)
                lin = i // 2
                col = i % 2
                btn.grid(row=lin, column=col, padx=10, pady=10)
    
                self.btns_tours.append(btn)
                setattr(self, f"tour{i}", btn)

        return self.frame_principale



    def mettre_a_jour_informations(self):
        if self.parent.modele.partie:
            self.label_vie.config(text="vie: " + str(self.parent.modele.partie.vie))
            self.label_argent.config(text="Argent: " + str(self.parent.modele.partie.cash))
            self.label_niveau.config(text="Niveau: " + str(self.parent.modele.partie.nivo))

    def creer_splash(self):
        frame_splash = tk.Frame(self.root,bg ="#2e2f31" )
        frame_splash.grid(row=0, column=0, sticky="nsew")

        label_titre = tk.Label(frame_splash, text="TOUR DEFENSE", fg="#99AAB5", bg="#2e2f31" ,font=("Arial", 40))
        label_titre.grid(padx=200,pady=200)

        self.boutton_play = tk.Button(frame_splash, text="START GAME",bg="#7289DA" , font=("Arial", 10),command=self.parent.demarrePartie)
        self.boutton_play.grid(pady = 10)
        return frame_splash

    def creer_carte(self):
        self.canevas = tk.Canvas(self.frame_principale ,width=500, height=500, bg="black")
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
       
   

    def getPosTour(self, evt, x, y):
        if self.tour_active:
            # On envoie la position ET le type au contrôleur
            canBuy = self.parent.setTour(x / 5, y / 5, self.type_en_cours)
            if canBuy: # si l'argent est suffisnat 
                self.canevas.create_image(x, y, image=self.tour_active, tags=("tour_img",))
                print("tou achetée")
            else:
                print("non")

    def afficheModele(self):
        self.canevas.delete("all")
        self.canevas.delete("all")

        self.canevas.create_image(0, 0, image=self.chmin_img, anchor=tk.NW)
        pos = []
        # On assume que nivoActif est initialis� au moment de l'affichage
        self.canevas.create_image(0, 0, image=self.chmin_img, anchor=tk.NW)

    def afficherCasesVides(self):
        for i in self.parent.modele.partie.nivoActif.emplacement.cases:
            id = self.parent.modele.partie.creerId()
            self.canevas.create_rectangle((i[0] - 10) * 2, (i[1] - 10) * 2 , (i[0] + 10) * 2 , (i[1] + 10) * 2, fill="black", tags=("cases", id))
            self.canevas.tag_bind(id, "<Button-1>", lambda event, x=i[0]*2, y=i[1]*2 : self.getPosTour(event, x, y))

    def afficheCreepTourBombe(self):
        self.canevas.delete("creep")
        self.canevas.delete("tour")
        self.canevas.delete("missile")

   


        # Logique originale pr�serv�e (via nivoActif)
        for i in self.parent.modele.partie.nivoActif.creepsEnCours:
            x1 = i.pos[0] * 5 - 3
            y1 = i.pos[1] * 5 - 3
            x2 = i.pos[0] * 5 + 3
            y2 = i.pos[1] * 5 + 3
            self.canevas.create_oval(x1, y1, x2, y2, width=2, fill="red", tags=("creep",))
        # pour les missiles 
        for t in self.parent.modele.partie.tours: # pour tour in tours
            for m in t.projectile: # misil dans tour
                mx1 = m.x * 5 - m.taille
                my1 = m.y * 5 - m.taille
                mx2 = m.x * 5 + m.taille
                my2 = m.y * 5 + m.taille
                self.canevas.create_rectangle(mx1, my1, mx2, my2, fill="yellow", tags=("missile",))
            
        # Logique originale pr�serv�e (via nivoActif)
        for i in self.parent.modele.partie.tours:
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
        # On mémorise la clé de la tour (ex: "tour0", "tour1"...)
        self.type_en_cours = f"tour_{i}"

    
    # def pause(self,evt):
    #     self.parent.pause(evt)