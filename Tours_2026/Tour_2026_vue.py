# -*- coding: ISO-8859-1 -*-
"""
====================================================================
  TOUR DEFENSE 2026 - VUE
====================================================================
  Gere toute l'interface graphique du jeu (Tkinter) :
   - Ecran d'accueil (splash)
   - Fenetre principale (carte + menu des tours + barre d'infos)
   - Affichage des creeps, tours et missiles
   - Gestion des clics et selection des tours
====================================================================
"""

from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk


class Vue():

    # ================================================================
    # INITIALISATION
    # ================================================================

    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Tk()

        # Etat de la selection de tour
        self.tour_active = None
        self.type_en_cours = None

        # Gestion des frames (ecrans)
        self.frames = {}
        self.frameActif = None

        # Construction de l'interface
        self.creerFrames()
        self.changerFrame("splash")

    # ================================================================
    # GESTION DES FRAMES (ECRANS)
    # ================================================================

    # Cree tous les frames de l'application (splash + principal)
    def creerFrames(self):
        self.frames["principal"] = self.creer_fenetre_principale()
        self.frames["splash"] = self.creer_splash()

    # Change le frame affiche a l'ecran
    def changerFrame(self, nouveauFrame):
        if self.frameActif:
            self.frameActif.pack_forget()
        self.frameActif = self.frames[nouveauFrame]
        self.frameActif.pack()

    # ----------------------------------------------------------------
    # FRAME : SPLASH (ECRAN D'ACCUEIL)
    # ----------------------------------------------------------------

    # Cree l'ecran d'accueil avec le titre et le bouton "START GAME"
    def creer_splash(self):
        frame_splash = tk.Frame(self.root, bg="#2e2f31")
        frame_splash.grid(row=0, column=0, sticky="nsew")

        # Titre
        label_titre = tk.Label(frame_splash, text="TOUR DEFENSE",
                               fg="#99AAB5", bg="#2e2f31",
                               font=("Arial", 40))
        label_titre.grid(padx=200, pady=200)

        # Bouton de demarrage
        self.boutton_play = tk.Button(frame_splash, text="START GAME",
                                      bg="#7289DA", font=("Arial", 10),
                                      command=self.parent.demarrePartie)
        self.boutton_play.grid(pady=10)
        return frame_splash

    # ----------------------------------------------------------------
    # FRAME : FENETRE PRINCIPALE
    # ----------------------------------------------------------------

    # Cree la fenetre principale : barre d'infos, canevas du jeu, menu des tours
    def creer_fenetre_principale(self):
        self.frame_principale = tk.Frame(self.root)

        # Construction des trois zones
        self._creer_barre_informations()
        self._creer_canevas_jeu()
        self._creer_menu_tours()

        return self.frame_principale

    # Cree la barre d'informations en haut (vie, argent, score, niveau, boutons)
    def _creer_barre_informations(self):
        self.frame_infomations = tk.Frame(self.frame_principale,
                                          width=800, height=50,
                                          bg="#2e2f31")
        self.frame_infomations.grid_propagate(False)
        self.frame_infomations.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # --- Labels d'information ---
        self.label_vie = tk.Label(self.frame_infomations, text="Vie: --",
                                  fg="black", bg="#7D9EC0", font=("Arial", 12))
        self.label_vie.grid(row=0, column=0, sticky="ew", pady=10, padx=10)

        self.label_argent = tk.Label(self.frame_infomations, text="Argent: --",
                                     fg="black", bg="#7D9EC0", font=("Arial", 12))
        self.label_argent.grid(row=0, column=1, sticky="ew", pady=10, padx=10)

        self.label_score = tk.Label(self.frame_infomations, text="Score: 0",
                                    fg="black", bg="#7D9EC0", font=("Arial", 12))
        self.label_score.grid(row=0, column=2, sticky="ew", pady=10, padx=10)

        self.label_niveau = tk.Label(self.frame_infomations, text="Niveau: --",
                                     fg="black", bg="#7D9EC0", font=("Arial", 12))
        self.label_niveau.grid(row=0, column=3, sticky="ew", pady=10, padx=10)

        # --- Menu cache d'options ---
        self.frame_allbtns = tk.Menu(self.frame_infomations, tearoff=0)
        self.frame_allbtns.add_command(label="Start")
        self.frame_allbtns.add_command(label="Pause", command=self.parent.pause)
        if hasattr(self.parent, 'modele'):
            self.frame_allbtns.add_command(label="Start game",
                                           command=self.parent.modele.demarrePartie)

        # --- Boutons d'options et de vague ---
        self.frame_options = tk.Button(self.frame_infomations,
                                       text="Game options",
                                       command=self.afficher_options)
        self.frame_options.grid(row=0, column=4, sticky="ew", pady=10, padx=10)

        self.btn_vague_automatique = tk.Button(self.frame_infomations,
                                               text="Vague automatique",
                                               bg="green")
        self.btn_vague_automatique.grid(row=0, column=5, sticky="ew", pady=10, padx=10)

    # Cree le canevas central ou le jeu se deroule
    def _creer_canevas_jeu(self):
        self.canevas = tk.Canvas(self.frame_principale,
                                 width=500, height=500, bg="black")
        self.canevas.grid(row=1, column=0)

        # Chargement de l'image de fond (avec protection si elle manque)
        try:
            self.chemin1 = Image.open("Tours_2026/chemin1.png")
            self.resize = self.chemin1.resize((500, 500), Image.Resampling.LANCZOS)
            self.chmin_img = ImageTk.PhotoImage(self.resize)
            self.canevas.create_image(0, 0, image=self.chmin_img, anchor=tk.NW)
        except Exception as e:
            print(f"Erreur de fond de carte: {e}")

    # Cree le menu lateral droit avec les images des tours selectionnables
    def _creer_menu_tours(self):
        self.frame_tours = tk.Frame(self.frame_principale,
                                    width=200, height=500, bg="#2e2f31")
        self.frame_tours.grid_propagate(False)
        self.frame_tours.grid(row=1, column=1, sticky="nsew")

        # Chemins des images de tours
        chemin_routes = [
            "images/tour1.png", "images/tour2.png", "images/tour3.png",
            "images/tour4.png", "images/tour5.png", "images/tour6.png"
        ]

        self.photo_tours = []
        self.btns_tours = []

        # Creation des boutons-images pour chaque tour disponible
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

                # Disposition sur 2 colonnes
                lin = i // 2
                col = i % 2
                btn.grid(row=lin, column=col, padx=10, pady=10)

                self.btns_tours.append(btn)
                setattr(self, f"tour{i}", btn)

    # ================================================================
    # MISE A JOUR DE L'AFFICHAGE
    # ================================================================

    # Met a jour les labels d'informations (vie, argent, niveau)
    def mettre_a_jour_informations(self):
        if self.parent.modele.partie:
            self.label_vie.config(text="vie: " + str(self.parent.modele.partie.vie))
            self.label_argent.config(text="Argent: " + str(self.parent.modele.partie.cash))
            self.label_niveau.config(text="Niveau: " + str(self.parent.modele.partie.nivo))

    # Reinitialise le canevas et redessine le fond
    def creer_carte(self):
        self.canevas = tk.Canvas(self.frame_principale,
                                 width=500, height=500, bg="black")
        self.canevas.grid(row=1, column=0)
        self.chemin1 = Image.open("Tours_2026/chemin1.png")
        self.resize = self.chemin1.resize((500, 500), Image.Resampling.LANCZOS)
        self.chmin_img = ImageTk.PhotoImage(self.resize)

    # Redessine la carte de fond
    def afficheModele(self):
        self.canevas.delete("all")
        self.canevas.create_image(0, 0, image=self.chmin_img, anchor=tk.NW)

    # Affiche les cases vides ou il est possible de poser une tour
    def afficherCasesVides(self):
        for i in self.parent.modele.partie.nivoActif.emplacement.cases:
            id = self.parent.modele.partie.creerId()
            self.canevas.create_rectangle((i[0] - 10) * 2, (i[1] - 10) * 2,
                                          (i[0] + 10) * 2, (i[1] + 10) * 2,
                                          fill="black", tags=("cases", id))
            self.canevas.tag_bind(id, "<Button-1>",
                                  lambda event, x=i[0]*2, y=i[1]*2:
                                  self.creerTour(event, x, y))

    # Redessine tous les elements mobiles : creeps, missiles, tours
    def afficheCreepTourBombe(self):
        # Nettoyage des anciens elements
        self.canevas.delete("creep")
        self.canevas.delete("tour")
        self.canevas.delete("missile")

        # --- Creeps ---
        for i in self.parent.modele.partie.nivoActif.creepsEnCours:
            x1 = i.pos[0] * 5 - 3
            y1 = i.pos[1] * 5 - 3
            x2 = i.pos[0] * 5 + 3
            y2 = i.pos[1] * 5 + 3
            self.canevas.create_oval(x1, y1, x2, y2,
                                     width=2, fill="red", tags=("creep",))

        # --- Missiles ---
        for t in self.parent.modele.partie.tours:
            for m in t.projectile:
                mx1 = m.x * 5 - m.taille
                my1 = m.y * 5 - m.taille
                mx2 = m.x * 5 + m.taille
                my2 = m.y * 5 + m.taille
                self.canevas.create_rectangle(mx1, my1, mx2, my2,
                                              fill="yellow", tags=("missile",))
        
        

    # ================================================================
    # MENUS & INTERACTIONS
    # ================================================================

    # Cree le menu deroulant et les boutons de gestion des vagues
    # (Cette methode est appelee apres le demarrage de la partie pour
    #  brancher les commandes qui dependent du modele/controleur)
    def creer_boite_menu(self):
        # Menu cache d'options
        self.frame_allbtns = tk.Menu(self.frame_infomations, tearoff=0)
        self.frame_allbtns.add_command(label="Start")
        self.frame_allbtns.add_command(label="Pause", command=self.parent.pause)
        self.frame_allbtns.add_command(label="Start game",
                                       command=self.parent.modele.demarrePartie)

        # Bouton "Game options"
        self.frame_options = tk.Button(self.frame_infomations, text="Game options")
        self.frame_options.grid(row=0, column=4, sticky="ew", pady=10, padx=10)
        self.frame_options.config(command=self.afficher_options)

        # Bouton "Vague automatique"
        self.btn_vague_automatique = tk.Button(self.frame_infomations,
                                               text="vague automatique")
        self.btn_vague_automatique.grid(row=0, column=5, sticky="ew", pady=10, padx=10)
        self.btn_vague_automatique.config(command=self.parent.vagueAutomatique)

        # Bouton "Vague suivante"
        self.btn_next_vague = tk.Button(self.frame_infomations,
                                        text="vague suivante", bg="orange")
        self.btn_next_vague.grid(row=0, column=6, sticky="ew", pady=10, padx=10)
        self.btn_next_vague.config(command= self.parent.nouvelleVague)
        
    # Affiche le menu d'options sous le bouton "Game options"
    def afficher_options(self):
        x = self.frame_options.winfo_rootx()
        y = self.frame_options.winfo_rooty()
        self.frame_allbtns.post(x, y)

   
    # Memorise la tour choisie par le joueur dans le menu
    def image_selectionne(self, i):
        self.tour_active = self.photo_tours[i]
        self.type_en_cours = f"tour_{i}"
        self.creer_powerUp()
        message_notif = f"Tour selectionnee : {self.type_en_cours}"
        self.creer_notification(message=message_notif)
        
       

    def creer_powerUp(self):
        if hasattr(self, 'frame_powers') and self.frame_powers:
            self.frame_powers.destroy()

        
        self.frame_powers = tk.Frame(self.frame_tours, width=180, height=150, bg="#2e2f31")
        self.frame_powers.grid_propagate(False)
        self.frame_powers.grid(row=4, column=0, columnspan=2, sticky="ew", pady=10)

        self.lbl_titre = tk.Label(self.frame_powers, text="POWER-UPS", fg="#99AAB5", bg="#2e2f31", font=("Arial", 11, "bold"))
        self.lbl_titre.pack(pady=5,padx=10)
            # on doit ajouter les commandes pour les powerups 
        self.btn_portee = tk.Button(self.frame_powers, text="+ FORCE (20$)", bg="#7289DA", fg="white")
        self.btn_portee.pack(fill="x",padx=10, pady=5)
        self.btn_portee.config(command=self.parent.powerUpForce)

        self.btn_degat = tk.Button(self.frame_powers, text="+ RAYON (20$)", bg="#7289DA", fg="white")
        self.btn_degat.pack(fill="x",padx=10, pady=5)
        self.btn_degat.config(command=self.parent.powerUpRayon)
    
    def creer_notification(self,message):
        if hasattr(self, 'frame_notification') and self.frame_notification:
            self.frame_notification.destroy()
        self.frame_notification = tk.Frame(self.frame_tours,
                                    width=150, height=50, bg="#dd2108")
        self.frame_notification.grid_propagate(False)
        self.frame_notification.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5,padx=10)

        lbl_message = tk.Label(self.frame_notification, text=message,fg = "black", font=("Arial", 11, "bold"))
        lbl_message.pack(expand=True, fill="both")
    # Place une tour sur le canevas en cas de clic sur une case
    def creerTour(self, evt, x, y):
        if self.tour_active:
            # Envoi de la position et du type au controleur
            if self.parent.setTour(x / 5, y / 5, self.type_en_cours):
                self.canevas.create_image(x, y, image=self.tour_active,
                                          tags=("tour_img",))
                
                self.canevas.tag_bind("tour_img", "<Button-1>", self.cliquer_tour)

    def rafraichir_notification_tour(self):
        # On va chercher la tour actuellement sélectionnée dans le modèle
        tour = self.parent.modele.partie.tourActuelle
        if tour:
            # On recrée le message avec les nouvelles statistiques mises à jour
            noti = f"Type: {tour.type}\nForce: {tour.force} | Rayon: {tour.rayon}"
            self.creer_notification(message=noti)

    def cliquer_tour(self, evt):
        # "current" est un tag spécial de Tkinter qui cible l'élément sous la souris
        item_cible = self.canevas.find_withtag("current")[0]
        
        # On récupère les coordonnées [x, y] de cette image sur le canevas
        coords = self.canevas.coords(item_cible)
        x_canevas = coords[0]
        y_canevas = coords[1]
        
        # On reconvertit les coordonnées pour le Modèle (divisé par 5) et on l'envoie au Contrôleur
        self.tour_touve = self.parent.clic_tour_existante(x_canevas / 5, y_canevas / 5)

        self.rafraichir_notification_tour()

    def game_over(self):
        if hasattr(self, 'frame_game_over' )and self.frame_game_over:
            self.frame_game_over.destroy()
        
        self.frame_game_over = tk.Frame(self.frame_principale, bg="#1a1a1a")
        self.frame_game_over.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="nsew")
        
        lbl_title = tk.Label(self.frame_game_over, text="GAME OVER", 
                            font=("Arial", 40, "bold"), fg="red", bg="#1a1a1a")
        lbl_title.pack(pady=50)
        
        # Bouton quitter
        btn_quitter = tk.Button(self.frame_game_over, text="Quitter",
                                command=self.root.quit,
                                font=("Arial", 15), bg="red", fg="white")
        btn_quitter.pack(pady=10)

    

    
       
    # ================================================================
    # OUTILS
    # ================================================================

    # Charge et redimensionne une image, retourne None en cas d'erreur
    def resizeImages(self, chemin, largeur, hauteur):
        try:
            raw_img = Image.open(chemin)
            resized_img = raw_img.resize((largeur, hauteur), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(resized_img)
        except Exception as e:
            print(f"Error image {chemin}: {e}")
            return None
	#VUE