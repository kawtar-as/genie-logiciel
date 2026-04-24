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

    def demarrePartie(self):
        
        if self.actif == 0:
            self.actif = 1
            self.modele.demarrePartie()
            self.vue.creer_boite_menu()
            self.vue.afficheModele()
            self.vue.afficherCasesVides()
            self.continuePartie()
        else:
           
            self.actif = 0
        

    def continuePartie(self):
        #if self.paused:
            if self.actif:
                self.modele.nivoActif.bougeCreep()
                self.modele.nivoActif.creepDansRayon()
                self.vue.afficheCreepTourBombe()
                # Appel r�cursif via Tkinter
                self.vue.root.after(self.delai, self.continuePartie)
                #SI VIE JOUEUR == 0 alors partie termine
                if self.modele.vie == 0:
                    self.actif = 0
        
            
        
   
    def pause(self, ):
        if self.actif == 0:
            self.actif = 1
            self.continuePartie()  # <--- CRITIQUE : Relance la boucle after
            print("Jeu repris")
        else:
            self.actif = 0
            print("Jeu en pause")

    def setTour(self, pos_x,pos_y):
        self.modele.setTour(pos_x,pos_y)
    

if __name__ == '__main__':
    c = Controleur()
    c.vue.root.mainloop()