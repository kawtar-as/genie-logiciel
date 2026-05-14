# -*- coding: ISO-8859-1 -*-
import Tour_2026_modele as mod
import Tour_2026_vue as vue


class Controleur():
    def __init__(self):
        self.modele = mod.Modele(self)
        self.vue = vue.Vue(self)
        self.paused = True
        self.actif = 0
        self.delai = 50  # Vitesse du jeu
        self.vague_automatique = False

    def demarrePartie(self):
        self.vue.changerFrame("principal")   
        self.vue.mettre_a_jour_informations() 
        if self.actif == 0:
            self.actif = 1
            self.modele.demarrePartie()
          #  self.vue.frame_lobby.destroy()
            self.vue.creer_carte()
            self.vue.creer_boite_menu()
            self.vue.afficheModele()
            self.vue.afficherCasesVides()
            self.continuePartie()
        else:
         
            self.actif = 0
        

    def continuePartie(self):
            if self.actif:
                self.modele.partie.nivoActif.bougeCreep()
                if self.vague_automatique:
                    if self.modele.partie.vagueTerminee():
                        self.nouvelleVague()

            for tour in self.modele.partie.tours:
                tour.tirer()
            self.modele.partie.ajour_projectiles()
            self.vue.afficheCreepTourBombe()
            self.vue.root.after(self.delai, self.continuePartie)
            if self.modele.partie.vie <= 0: 
                self.actif = 0
                print("Partie Terminée")
 
   
    def pause(self, ):
        if self.actif == 0:
            self.actif = 1 
            self.continuePartie()  # <--- CRITIQUE : Relance la boucle after
            print("Jeu repris")
        else:
            self.actif = 0
            print("Jeu en pause")

    def setTour(self, pos_x,pos_y,selectionne):
        self.modele.partie.creerTour(pos_x,pos_y,selectionne)
    

if __name__ == '__main__':
    c = Controleur()
    c.vue.root.mainloop()