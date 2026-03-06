# -*- coding: ISO-8859-1 -*-
import Tour_2026_modele as mod
import Tour_2026_vue as vue


class Controleur():
    def __init__(self):
        self.modele = mod.Modele(self)
        self.vue = vue.Vue(self)
        self.actif = 0
        self.delai = 50  # Vitesse du jeu

    def demarrePartie(self):
        if self.actif == 0:
            self.actif = 1
            self.modele.demarrePartie()
            self.vue.creer_boite_menu()
            
            self.vue.afficheModele()
            self.continuePartie()
        else:
            self.actif = 0

    def continuePartie(self):
        if self.actif:
            self.modele.nivoActif.bougeCreep()
            self.vue.afficheCreepTourBombe()
            # Appel r�cursif via Tkinter
            self.vue.root.after(self.delai, self.continuePartie)

    def setTour(self, pos):
        self.modele.setTour(pos)


if __name__ == '__main__':
    c = Controleur()
    c.vue.root.mainloop()