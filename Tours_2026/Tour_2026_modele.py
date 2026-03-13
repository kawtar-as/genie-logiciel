# -*- coding: ISO-8859-1 -*-
'''
Jeu de defense de Tours_2026
 deux patrons de parcours
 les niveaux incremente la difficult�
    en augmentant la force des creeps
    en augmentant le nombre de creeps

les Tours_2026 peuvent b�n�ficier d'ameliorations
   en terme de morts occasion�es
   et d'argent disponible
'''

import random
from helper import *
class Parcours():
    def __init__(self):
        self.noeuds1=[[0,10],
                     [50,10],
                     [50,80],
                     [100,80]]
        
        self.noeuds2=[[0,10],
                     [20,10],
                     [20,40],
                     [50,40],
                     [50,20],
                     [80,20],
                     [80,60],
                     [30,60],
                     [30,80],
                     [100,80]]
        self.noeuds = [[0, 0],
                       [22, 35],
                       [53, 35],
                       [53, 23],
                       [75, 23],
                       [75, 55],
                       [33, 55],
                       [33, 77],
                       [100, 77]]
        
        self.emplacements=[[65, 60],
                          [20, 110],
                          [165, 90]]
       
#créer emplacement = new Emplacement(self.parcours.emplacements[0])
class Emplacement():
    def __init__(self, modele, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.id = modele.creerId()
        self.isOccupied = None 
        




class Tour():
    def __init__(self,parent,pos_x, pos_y):
        self.parent = parent
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.cible = [0,0]
        self.vitesse_tir = 5
        self.rayon = 0
        self.projectile = []
        self.prix = 100
        self.force = 1
    def tirer(self, rayon, cible):
        self.rayon = rayon
        self.cible = cible




class Missile():
    def __init__(self, x, y, vitesse, dmg, taille):
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.dmg = dmg
        self.taille = taille


class Creep():
    def __init__(self,parent):
        self.parent=parent
        self.pos=self.parent.parcours.noeuds[0][:]
        self.cible=1 #indice du noeud de parcours a atteindre
        if self.pos[0]!=self.parent.parcours.noeuds[1][0]: # on simplifie le mouvement en verifiant uniquement l'axe de deplacement
            self.axe=0
            if self.pos[0]<self.parent.parcours.noeuds[1][0]:
                self.dir=1
            else:
                self.dir=-1
        else:
            self.axe=1
            if self.pos[1]<self.parent.parcours.noeuds[1][1]:
                self.dir=1
            else:
                self.dir=-1
        self.vitesse=2
        self.force=10
        self.creep_vie = 10

    def bouge(self):
        # 1. V�rifier si on a fini le parcours (S�curit�)
        if self.cible >= len(self.parent.parcours.noeuds):
            self.perdre_vie_joueur()
            return

        # 2. Identifier le point de destination imm�diat
        cible_x, cible_y = self.parent.parcours.noeuds[self.cible]
        curr_x, curr_y = self.pos

        # 3. Calculer la distance restante vers ce point
        # (Utilise votre nouveau Helper ou l'alias)
        dist_restante = Helper.calcDistance(curr_x, curr_y, cible_x, cible_y)

        # 4. Logique de mouvement
        if dist_restante <= self.vitesse:
            # CAS A : On d�passe ou on atteint la cible ce tour-ci
            self.pos = [cible_x, cible_y]  # On se "snap" exactement sur le point
            self.cible += 1  # On passe au prochain noeud

            # Si c'�tait le dernier noeud, on blesse le joueur
            if self.cible >= len(self.parent.parcours.noeuds):
                self.perdre_vie_joueur()
        else:
            # CAS B : On est encore en chemin
            # On calcule l'angle vers la cible
            angle = Helper.calcAngle(curr_x, curr_y, cible_x, cible_y)
            # On avance exactement de "vitesse" dans cette direction
            nouv_x, nouv_y = Helper.getAngledPoint(angle, self.vitesse, curr_x, curr_y)
            self.pos = [nouv_x, nouv_y]

    def perdre_vie_joueur(self, valeur=1):
        self.parent.parent.vie -= valeur
        print(self.parent.parent.vie)

        
class Nivo(): ##Vague
    def __init__(self,parent):
        self.parent=parent
        self.parcours = Parcours()
        self.densiteCreep=3
        self.tours=[]
        self.creeps=[]
        self.creepsEnCours=[]
        self.creeCreep()
        
    
    def ajouteTour(self,pos_x,pos_y):
        self.tours.append(Tour(self,pos_x,pos_y))
        
        
    def creeCreep(self):
        for i in range(self.parent.creepparnivo):
            self.creeps.append(Creep(self))
            
    def bougeCreep(self): ## bouger sur le chemin
        if self.creeps:
            ajoute=0
            c=self.creeps[0]
            if self.creepsEnCours:
                cPrecedent=self.creepsEnCours[0]
                if cPrecedent.cible==1: # onverifie si le dernier creep parti est assez loin seulement s'il est sur le m�me tron�on
                    if cPrecedent.pos[c.axe]>c.pos[c.axe]+c.parent.densiteCreep:
                        ajoute=1
            else:
                ajoute=1
            if ajoute:  ## les faire bouger sur le chemin 
                c=self.creeps.pop(0)
                c.pos=self.parcours.noeuds[0][:] # on positionne le creep sur le prmier noeud
                c.cible=1 #on vise le prochain noeud, le deuxieme
                self.creepsEnCours.insert(0,c)
        n=0
        for i in self.creepsEnCours:
            n=n+1
            i.bouge()
            if(i.cible >= len(self.parcours.noeuds)):
                self.creepsEnCours.remove(i)
            
    def setTour(self,pos_x,pos_y):
        print("NIVO",pos_x,pos_y)
        self.tours.append(Tour(self,pos_x,pos_y))
        
class Modele():
    
    def __init__(self, parent):
        self.parent=parent
        self.vie=20
        self.cash=0
        self.creepparnivo=12
        self.creepforce=5
        self.nivo=0
        self.compteur = 0
        self.parcours = Parcours()# À modifier plus tard
        
        self.emplacements = self.creer_Emplacement()

    def creer_Emplacement(self):
        liste=[]
        for x,y in self.parcours.emplacements:
            emplacement = Emplacement(self,x,y)
            liste.append(emplacement)
        return liste

    def demarrePartie(self):
        self.nivo=self.nivo+1
        self.nivoActif=Nivo(self)

    def setTour(self,pos_x,pos_y):
        print("MODELE",pos_x,pos_y)
        self.nivoActif.setTour(pos_x,pos_y)

    def creerId(self):
        s = "id_" + str(self.compteur)
        self.compteur += 1
        return s

    


if __name__ == '__main__':
    m=Modele(1)
    m.demarrePartie()
    print(m.nivo.creeps)
    print("FIN")