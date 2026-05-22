# -*- coding: ISO-8859-1 -*-
"""
====================================================================
  TOUR DEFENSE 2026 - CONTROLEUR
====================================================================
  Fait le lien entre le Modele (logique du jeu) et la Vue (interface).
  Gere le cycle de vie de la partie : demarrage, boucle de jeu, pause,
  vagues automatiques et placement des tours.
====================================================================
"""

import Tour_2026_modele as mod
import Tour_2026_vue as vue


class Controleur():

    # ================================================================
    # INITIALISATION
    # ================================================================

    def __init__(self):
        # Instanciation du modele et de la vue
        self.modele = mod.Modele(self)
        self.vue = vue.Vue(self)

        # Etats du jeu
        self.paused = True
        self.actif = 0
        self.delai = 50              # Vitesse du jeu (ms entre chaque tick)
        self.vague_automatique = False

    # ================================================================
    # CYCLE DE VIE DE LA PARTIE
    # ================================================================

    # Demarre une nouvelle partie : prepare la vue principale et lance la boucle
    def demarrePartie(self):
        self.vue.changerFrame("principal")
        self.vue.mettre_a_jour_informations()

        if self.actif == 0:
            self.actif = 1
            self.modele.demarrePartie()
            self.vue.creer_carte()
            self.vue.creer_boite_menu()
            self.vue.afficheModele()
            self.vue.afficherCasesVides()
            self.continuePartie()
        else:
            self.actif = 0

    # Boucle principale du jeu : deplace les creeps, fait tirer les tours,
    # met a jour les projectiles et rafraichit l'affichage
    def continuePartie(self):
        if not self.actif:
            return
        partie = self.modele.partie
        if partie and partie.nivoActif:
            self.modele.partie.nivoActif.bougeCreep()
            # Lancement automatique de la prochaine vague si activee
            if self.vague_automatique:
                if partie.vagueTerminee():
                    self.nouvelleVague()

        # Les tours tirent et les projectiles avancent
        for tour in partie.tours:
            tour.tirer()
        partie.ajour_projectiles()
        # Fin de partie si la vie tombe a 0
        if partie.vie <= 0:
            self.actif = 0
            print("Partie Terminee")
            return

        # Rafraichissement graphique
        self.vue.afficheCreepTourBombe()
        if self.actif:
            self.vue.root.after(self.delai, self.continuePartie)

        # # Fin de partie si la vie tombe a 0
        # if self.modele.partie.vie <= 0:
        #     self.actif = 0
        #     print("Partie Terminee")

    # Met le jeu en pause ou le reprend
    def pause(self):
        if self.actif == 0:
            self.actif = 1
            self.continuePartie()    # CRITIQUE : relance la boucle after
            print("Jeu repris")
        else:
            self.actif = 0
            print("Jeu en pause")

    # ================================================================
    # GESTION DES VAGUES
    # ================================================================

    # Lance une nouvelle vague de creeps si la precedente est terminee
    def nouvelleVague(self):
        if self.modele.partie.vagueTerminee():
            self.modele.partie.initPartie()
            self.vue.mettre_a_jour_informations()
        else:
            print("partie en cours, impossible de lancer une nouvelle vague")

    # Active / desactive le lancement automatique des vagues
    def vagueAutomatique(self):
        if not self.vague_automatique:
            self.vague_automatique = True
            self.vue.btn_vague_automatique.config(bg="green", text="Auto: ON")
        else:
            self.vague_automatique = False
            self.vue.btn_vague_automatique.config(bg="red", text="Auto: OFF")

    # ================================================================
    # GESTION DES TOURS
    # ================================================================

    # Demande au modele de creer une tour a la position cliquee
    def setTour(self, pos_x, pos_y, selectionne):
        return self.modele.partie.creerTour(pos_x, pos_y, selectionne)
    
    # Demande au modèle de trouver la tour cliquée à ces coordonnées
    def clic_tour_existante(self, pos_x, pos_y):
        tour_cliquee = self.modele.partie.trouver_tour(pos_x, pos_y)
        
        if tour_cliquee:
            # L'objet retourné est la véritable instance de Tour (ou TourLaser, etc.)
            
            print(f"Succès : Vous avez cliqué sur une tour de type {tour_cliquee.type} !")
            print(f"Force : {tour_cliquee.force} | Rayon : {tour_cliquee.rayon}")

            return tour_cliquee

   
    def powerUpRayon(self):
        self.modele.partie.changerRayonTour()
        self.vue.rafraichir_notification_tour()

    def getTagTour(self):
        return self.modele.partie.tourActuelle.type

    def powerUpForce(self):
        self.modele.partie.changerForceTour()
        self.vue.rafraichir_notification_tour()

# ====================================================================
# POINT D'ENTREE
# ====================================================================

if __name__ == '__main__':
    c = Controleur()
    c.vue.root.mainloop()
