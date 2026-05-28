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

# ====================================================================
# PALETTE DE COULEURS CENTRALISEE
# ====================================================================
C = {
    "bg_dark":    "#1a1c1e",   # Fond principal tres sombre
    "bg_panel":   "#23262b",   # Panneaux lateraux
    "bg_card":    "#2c2f36",   # Cartes / elements
    "accent":     "#5865F2",   # Bleu Discord (accent principal)
    "accent2":    "#57F287",   # Vert succes
    "accent3":    "#FEE75C",   # Jaune or
    "danger":     "#ED4245",   # Rouge danger
    "orange":     "#E67E22",   # Orange vague
    "text_light": "#DCDDDE",   # Texte principal clair
    "text_dim":   "#72767D",   # Texte secondaire grise
    "border":     "#3a3d44",   # Bordure subtile
    "hp_high":    "#2ecc71",   # Barre de vie haute
    "hp_mid":     "#f39c12",   # Barre de vie moyenne
    "hp_low":     "#e74c3c",   # Barre de vie basse
}

# ====================================================================
# HELPERS VISUELS
# ====================================================================

def styled_button(parent, text, command=None, color=None, font_size=10):
    """Cree un bouton avec le style du jeu."""
    bg = color or C["accent"]
    btn = tk.Button(
        parent, text=text, command=command,
        bg=bg, fg=C["text_light"],
        font=("Consolas", font_size, "bold"),
        relief="flat", bd=0,
        activebackground=C["bg_card"],
        activeforeground=C["text_light"],
        cursor="hand2", padx=8, pady=4
    )
    return btn

def styled_label(parent, text, font_size=11, bold=False, color=None):
    """Cree un label avec le style du jeu."""
    weight = "bold" if bold else "normal"
    lbl = tk.Label(
        parent, text=text,
        bg=C["bg_panel"], fg=color or C["text_light"],
        font=("Consolas", font_size, weight)
    )
    return lbl

def separateur(parent):
    """Cree une ligne de separation horizontale."""
    return tk.Frame(parent, bg=C["border"], height=1)


class Vue():

    # ================================================================
    # INITIALISATION
    # ================================================================

    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Tk()
        self.root.title("Tour Defense 2026")
        self.root.configure(bg=C["bg_dark"])
        self.root.resizable(False, False)

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

    def creerFrames(self):
        self.frames["principal"] = self.creer_fenetre_principale()
        self.frames["splash"] = self.creer_splash()

    def changerFrame(self, nouveauFrame):
        if self.frameActif:
            self.frameActif.pack_forget()
        self.frameActif = self.frames[nouveauFrame]
        self.frameActif.pack()

    # ----------------------------------------------------------------
    # FRAME : SPLASH (ECRAN D'ACCUEIL)
    # ----------------------------------------------------------------

    def creer_splash(self):
        frame_splash = tk.Frame(self.root, bg=C["bg_dark"])
        frame_splash.grid(row=0, column=0, sticky="nsew")

        # Zone centrale
        centre = tk.Frame(frame_splash, bg=C["bg_dark"])
        centre.pack(expand=True, padx=200, pady=120)

        # Titre principal
        tk.Label(
            centre, text="TOWER", fg=C["accent3"],
            bg=C["bg_dark"], font=("Consolas", 52, "bold")
        ).pack()
        tk.Label(
            centre, text="DEFENSE 2026", fg=C["text_light"],
            bg=C["bg_dark"], font=("Consolas", 28, "bold")
        ).pack()

        # Sous-titre
        tk.Label(
            centre, text="Protege ta base. Elimine les vagues.",
            fg=C["text_dim"], bg=C["bg_dark"], font=("Consolas", 11)
        ).pack(pady=(8, 30))

        # Separateur decoratif
        tk.Frame(centre, bg=C["accent"], height=2, width=300).pack(pady=5)

        # 1. Utiliser styled_button et .pack() dans 'centre' pour éviter le conflit avec grid
        self.carte_options = styled_button(
            centre, text="Options de la carte",
            command=self.afficher_options_carte,
            color=C["bg_card"]
        )
        self.carte_options.pack(pady=10)

        # 2. Styliser le menu déroulant pour coller au thème sombre
        self.frame_cartes = tk.Menu(
            self.root, tearoff=0,
            bg=C["bg_card"], fg=C["text_light"],
            activebackground=C["accent"], activeforeground=C["text_light"],
            font=("Consolas", 10)
        )
        self.frame_cartes.add_command(label="Carte 1", command=lambda: self.parent.carte_choissie(1))
        self.frame_cartes.add_command(label="Carte 2", command=lambda: self.parent.carte_choissie(2))
        self.frame_cartes.add_command(label="Carte 3", command=lambda: self.parent.carte_choissie(3))

        # Bouton START
        self.boutton_play = styled_button(
            centre, text="  START GAME  ",
            command=self.parent.demarrePartie,
            font_size=14
        )
        self.boutton_play.pack(pady=20, ipadx=10, ipady=6)

        return frame_splash
    
    def afficher_options_carte(self):
            x = self.carte_options.winfo_rootx()
            y = self.carte_options.winfo_rooty()
            self.frame_cartes.post(x, y)
    
    def carte_choissie(self, nbCarte):
        return nbCarte

    # ----------------------------------------------------------------
    # FRAME : FENETRE PRINCIPALE
    # ----------------------------------------------------------------

    def creer_fenetre_principale(self):
        self.frame_principale = tk.Frame(self.root, bg=C["bg_dark"])
        self._creer_barre_informations()
        self._creer_canevas_jeu()
        self._creer_menu_tours()
        return self.frame_principale

    # Barre d'informations en haut
    def _creer_barre_informations(self):
        self.frame_infomations = tk.Frame(
            self.frame_principale, width=800, height=52,
            bg=C["bg_panel"]
        )
        self.frame_infomations.grid_propagate(False)
        self.frame_infomations.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Separateur bas de barre
        tk.Frame(self.frame_infomations, bg=C["accent"], height=2).grid(
            row=1, column=0, columnspan=10, sticky="ew"
        )

        # Labels d'info avec icones
        self.label_vie = tk.Label(
            self.frame_infomations, text="--",
            fg=C["danger"], bg=C["bg_panel"], font=("Consolas", 12, "bold")
        )
        self.label_vie.grid(row=0, column=0, pady=12, padx=16)

        self.label_argent = tk.Label(
            self.frame_infomations, text="--",
            fg=C["accent3"], bg=C["bg_panel"], font=("Consolas", 12, "bold")
        )
        self.label_argent.grid(row=0, column=1, pady=12, padx=16)

        self.label_score = tk.Label(
            self.frame_infomations, text="  0",
            fg=C["accent2"], bg=C["bg_panel"], font=("Consolas", 12, "bold")
        )
        self.label_score.grid(row=0, column=2, pady=12, padx=16)

        self.label_niveau = tk.Label(
            self.frame_infomations, text="--",
            fg=C["accent"], bg=C["bg_panel"], font=("Consolas", 12, "bold")
        )
        self.label_niveau.grid(row=0, column=3, pady=12, padx=16)

        # Espace poussoir pour aligner les boutons a droite
        tk.Frame(self.frame_infomations, bg=C["bg_panel"]).grid(
            row=0, column=4, sticky="ew", padx=20
        )
        self.frame_infomations.columnconfigure(4, weight=1)

        # Menu cache d'options
        self.frame_allbtns = tk.Menu(self.frame_infomations, tearoff=0,
                                     bg=C["bg_card"], fg=C["text_light"])
        self.frame_allbtns.add_command(label="Pause", command=self.parent.pause)

        # Boutons d'action
        self.frame_options = styled_button(
            self.frame_infomations, text="Options",
            command=self.afficher_options, color=C["bg_card"]
        )
        self.frame_options.grid(row=0, column=5, pady=10, padx=5)

        self.btn_vague_automatique = styled_button(
            self.frame_infomations, text="Auto: OFF",
            color=C["danger"]
        )
        self.btn_vague_automatique.grid(row=0, column=6, pady=10, padx=5)

    # Canevas de jeu central
    def _creer_canevas_jeu(self):
        self.canevas = tk.Canvas(
            self.frame_principale,
            width=500, height=500,
            bg=C["bg_dark"], highlightthickness=0
        )
        self.canevas.grid(row=1, column=0)

        try:
            self.chemin1 = Image.open("Tours_2026/chemin1.png")
            self.resize = self.chemin1.resize((500, 500), Image.Resampling.LANCZOS)
            self.chmin_img = ImageTk.PhotoImage(self.resize)
            self.canevas.create_image(0, 0, image=self.chmin_img, anchor=tk.NW)
        except Exception as e:
            print(f"Erreur fond de carte: {e}")

    # Menu lateral droit
    def _creer_menu_tours(self):
        self.frame_tours = tk.Frame(
            self.frame_principale,
            width=210, height=500, bg=C["bg_panel"]
        )
        self.frame_tours.grid_propagate(False)
        self.frame_tours.grid(row=1, column=1, sticky="nsew")

        # Titre de section
        styled_label(
            self.frame_tours, text="  TOURS  ",
            font_size=10, bold=True, color=C["text_dim"]
        ).grid(row=0, column=0, columnspan=2, sticky="ew", pady=(12, 4), padx=10)

        separateur(self.frame_tours).grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=10
        )

        # Prix correspondant a chaque tour
        prix_tours = ["0$", "20$", "40$", "80$", "100$", "175$"]

        chemin_routes = [
            "images/tour1.png", "images/tour2.png", "images/tour3.png",
            "images/tour4.png", "images/tour5.png", "images/tour6.png"
        ]

        self.photo_tours = []
        self.btns_tours = []

        for i in range(len(chemin_routes)):
            photo = self.resizeImages(chemin_routes[i], 52, 52)

            # Cellule (frame) pour chaque tour : image + prix
            cell = tk.Frame(self.frame_tours, bg=C["bg_card"],
                            width=85, height=80)
            cell.grid_propagate(False)
            lin = i // 2
            col = i % 2
            cell.grid(row=lin + 2, column=col, padx=8, pady=6)

            if photo:
                self.photo_tours.append(photo)
                btn = tk.Button(
                    cell, image=photo,
                    command=lambda idx=i: self.image_selectionne(idx),
                    borderwidth=0,
                    bg=C["bg_card"],
                    activebackground=C["accent"],
                    cursor="hand2"
                )
                btn.pack(pady=(4, 0))
                self.btns_tours.append(btn)
                setattr(self, f"tour{i}", btn)
            else:
                # Bouton textuel de secours si l'image manque
                btn = tk.Button(
                    cell, text=f"T{i}",
                    command=lambda idx=i: self.image_selectionne(idx),
                    bg=C["bg_card"], fg=C["text_light"],
                    font=("Consolas", 10), relief="flat", cursor="hand2"
                )
                btn.pack(fill="both", expand=True, pady=(4, 0))
                self.btns_tours.append(btn)
                self.photo_tours.append(None)

            # Label prix sous le bouton
            tk.Label(
                cell, text=prix_tours[i],
                bg=C["bg_card"], fg=C["accent3"],
                font=("Consolas", 8, "bold")
            ).pack()

    # ================================================================
    # MISE A JOUR DE L'AFFICHAGE
    # ================================================================

    def mettre_a_jour_informations(self):
        if self.parent.modele.partie:
            p = self.parent.modele.partie
            self.label_vie.config(text=f"{p.vie}")
            self.label_argent.config(text=f"{p.cash}")
            self.label_niveau.config(text=f"{p.nivo}")
            score = p.nivo * 100 + p.cash
            self.label_score.config(text=f"{score}")

    def creer_carte(self, choix_carte):
        self.canevas = tk.Canvas(
            self.frame_principale,
            width=500, height=500,
            bg=C["bg_dark"], highlightthickness=0
        )
        self.canevas.grid(row=1, column=0)
        nom_image = f"Tours_2026/chemin{choix_carte}.png"
        self.chemin1 = Image.open("Tours_2026/chemin1.png")
        self.resize = self.chemin1.resize((500, 500), Image.Resampling.LANCZOS)
        self.chmin_img = ImageTk.PhotoImage(self.resize)

    def afficheModele(self):
        self.canevas.delete("all")
        self.canevas.create_image(0, 0, image=self.chmin_img, anchor=tk.NW)

    def afficherCasesVides(self):
        for i in self.parent.modele.partie.nivoActif.emplacement.cases:
            id = self.parent.modele.partie.creerId()
            # Case avec style plus visible
            self.canevas.create_rectangle(
                (i[0] - 10) * 2, (i[1] - 10) * 2,
                (i[0] + 10) * 2, (i[1] + 10) * 2,
                fill=C["bg_card"], outline=C["accent"],
                width=2, dash=(4, 2), tags=("cases", id)
            )
            self.canevas.tag_bind(
                id, "<Button-1>",
                lambda event, x=i[0]*2, y=i[1]*2: self.creerTour(event, x, y)
            )

    def afficheCreepTourBombe(self):
        self.canevas.delete("creep")
        self.canevas.delete("missile")

        # --- Creeps avec barre de vie ---
        for creep in self.parent.modele.partie.nivoActif.creepsEnCours:
            cx = creep.pos[0] * 5
            cy = creep.pos[1] * 5
            r = 5  # rayon du creep

            # Corps du creep
            self.canevas.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                fill=C["danger"], outline="#ff6666", width=1,
                tags=("creep",)
            )

            # Barre de vie (fond gris + couleur selon hp)
            vie_max = creep.creep_vie  # approximation : on utilise la valeur courante comme reference
            # Calcul de la largeur de barre (fixe sur 14px)
            barre_w = 14
            barre_h = 2
            bx = cx - barre_w // 2
            by = cy - r - 4

            # Fond de barre (gris)
            self.canevas.create_rectangle(
                bx, by, bx + barre_w, by + barre_h,
                fill="#444", outline="", tags=("creep",)
            )

        # --- Missiles colores selon le type ---
        COULEUR_MISSILE = {
            "MissileNormal": C["accent3"],
            "MissileRapide": C["accent2"],
            "MissileFort":   C["danger"],
        }
        for t in self.parent.modele.partie.tours:
            for m in t.projectile:
                mx1 = m.x * 5 - m.taille
                my1 = m.y * 5 - m.taille
                mx2 = m.x * 5 + m.taille
                my2 = m.y * 5 + m.taille
                couleur = COULEUR_MISSILE.get(type(m).__name__, C["accent3"])
                self.canevas.create_oval(
                    mx1, my1, mx2, my2,
                    fill=couleur, outline="", tags=("missile",)
                )

    # ================================================================
    # MENUS & INTERACTIONS
    # ================================================================

    def creer_boite_menu(self):
        self.frame_allbtns = tk.Menu(
            self.frame_infomations, tearoff=0,
            bg=C["bg_card"], fg=C["text_light"]
        )
        self.frame_allbtns.add_command(label="Pause/Unpause", command=self.parent.pause)
        self.frame_allbtns.add_command(label="Reset game",
                                       command=self.parent.modele.demarrePartie)

        self.frame_options = styled_button(
            self.frame_infomations, text="Options",
            command=self.afficher_options, color=C["bg_card"]
        )
        self.frame_options.grid(row=0, column=5, pady=10, padx=5)

        self.btn_vague_automatique = styled_button(
            self.frame_infomations, text="Auto: OFF",
            color=C["danger"]
        )
        self.btn_vague_automatique.grid(row=0, column=6, pady=10, padx=5)
        self.btn_vague_automatique.config(command=self.parent.vagueAutomatique)

        self.btn_next_vague = styled_button(
            self.frame_infomations, text="Vague suivante",
            color=C["orange"]
        )
        self.btn_next_vague.grid(row=0, column=7, pady=10, padx=5)
        self.btn_next_vague.config(command=self.parent.nouvelleVague)

    def afficher_options(self):
        x = self.frame_options.winfo_rootx()
        y = self.frame_options.winfo_rooty()
        self.frame_allbtns.post(x, y)

    def image_selectionne(self, i):
        # Reinitialiser le style de tous les boutons
        for btn in self.btns_tours:
            btn.config(bg=C["bg_card"])

        # Mettre en valeur le bouton selectionne
        if i < len(self.btns_tours):
            self.btns_tours[i].config(bg=C["accent"])

        self.tour_active = self.photo_tours[i]
        self.type_en_cours = f"tour_{i}"
        self.creer_powerUp()
        message_notif = f"Tour selectionnee : tour_{i}"
        self.creer_notification(message=message_notif)

    def creer_powerUp(self):
        if hasattr(self, 'frame_powers') and self.frame_powers:
            self.frame_powers.destroy()

        self.frame_powers = tk.Frame(
            self.frame_tours, bg=C["bg_panel"], width=190
        )
        self.frame_powers.grid(row=5, column=0, columnspan=2,
                                sticky="ew", pady=4, padx=8)

        separateur(self.frame_powers).pack(fill="x", pady=(0, 6))

        tk.Label(
            self.frame_powers, text="AMELIORATIONS",
            fg=C["text_dim"], bg=C["bg_panel"],
            font=("Consolas", 9, "bold")
        ).pack(anchor="w", padx=4)

        styled_button(
            self.frame_powers, text="+FORCE  (20$)",
            command=self.parent.powerUpForce,
            color=C["accent"], font_size=9
        ).pack(fill="x", padx=4, pady=3)

        styled_button(
            self.frame_powers, text="+RAYON  (20$)",
            command=self.parent.powerUpRayon,
            color=C["accent"], font_size=9
        ).pack(fill="x", padx=4, pady=3)

    def creer_notification(self, message):
        if hasattr(self, 'frame_notification') and self.frame_notification:
            self.frame_notification.destroy()

        self.frame_notification = tk.Frame(
            self.frame_tours, bg=C["bg_card"], width=190
        )
        self.frame_notification.grid(
            row=6, column=0, columnspan=2,
            sticky="ew", pady=4, padx=8
        )

        # Bande coloree a gauche
        tk.Frame(self.frame_notification, bg=C["accent"], width=3).pack(
            side="left", fill="y"
        )

        tk.Label(
            self.frame_notification, text=message,
            fg=C["text_light"], bg=C["bg_card"],
            font=("Consolas", 9), justify="left", anchor="w",
            wraplength=160
        ).pack(side="left", padx=6, pady=6)

    def creerTour(self, evt, x, y):
        if self.tour_active:
            if self.parent.setTour(x / 5, y / 5, self.type_en_cours):
                self.canevas.create_image(
                    x, y, image=self.tour_active, tags=("tour_img",)
                )
                self.canevas.tag_bind(
                    "tour_img", "<Button-1>", self.cliquer_tour
                )

    def rafraichir_notification_tour(self):
        tour = self.parent.modele.partie.tourActuelle
        if tour:
            noti = f"Type: {tour.type}\nForce: {tour.force} | Rayon: {tour.rayon}"
            self.creer_notification(message=noti)

    def cliquer_tour(self, evt):
        item_cible = self.canevas.find_withtag("current")[0]
        coords = self.canevas.coords(item_cible)
        self.tour_touve = self.parent.clic_tour_existante(
            coords[0] / 5, coords[1] / 5
        )
        self.rafraichir_notification_tour()

    def game_over(self):
        if hasattr(self, 'frame_game_over') and self.frame_game_over:
            self.frame_game_over.destroy()

        self.frame_game_over = tk.Frame(
            self.frame_principale, bg=C["bg_dark"]
        )
        self.frame_game_over.grid(
            row=0, column=0, rowspan=2, columnspan=2, sticky="nsew"
        )

        centre = tk.Frame(self.frame_game_over, bg=C["bg_dark"])
        centre.pack(expand=True)

        tk.Label(
            centre, text="GAME OVER",
            font=("Consolas", 48, "bold"),
            fg=C["danger"], bg=C["bg_dark"]
        ).pack(pady=(80, 10))

        # Score final
        if self.parent.modele.partie:
            p = self.parent.modele.partie
            score = p.nivo * 100 + p.cash
            tk.Label(
                centre, text=f"Score final : {score}",
                font=("Consolas", 16),
                fg=C["accent3"], bg=C["bg_dark"]
            ).pack(pady=8)
            tk.Label(
                centre, text=f"Vague atteinte : {p.nivo}",
                font=("Consolas", 12),
                fg=C["text_dim"], bg=C["bg_dark"]
            ).pack(pady=4)

        tk.Frame(centre, bg=C["danger"], height=2, width=300).pack(pady=20)

        styled_button(
            centre, text="  Quitter  ",
            command=self.root.quit,
            color=C["danger"], font_size=13
        ).pack(ipadx=10, ipady=6)

    # ================================================================
    # OUTILS
    # ================================================================

    def resizeImages(self, chemin, largeur, hauteur):
        try:
            raw_img = Image.open(chemin)
            resized_img = raw_img.resize((largeur, hauteur), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(resized_img)
        except Exception as e:
            print(f"Error image {chemin}: {e}")
            return None
	#VUE
