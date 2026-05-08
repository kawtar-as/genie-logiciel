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
       

class Emplacement():
    def __init__(self):
        self.isOccupied = None 
        # objet emplacement dans la liste
        a =  {}
        self.cases=[[100, 55],
                        [56, 150],
                        [161, 90]]
        




class Tour():
    def __init__(self,parent,pos_x, pos_y):
        self.parent = parent
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.cible = [0,0]
        self.vitesse_tir = 5
        self.rayon = 15
        self.projectile = []
        self.prix = 100
        self.force = 1
        ##self.focus
        self.focus = self.parent.nivoActif.creepsEnCours[0]

    def getPosition(self):
        return self.pos_x, self.pos_y
    
    def creepInRTour(self, tour):
         self.creepInRTour = []
         xTour, yTour = tour.getPosition() 

         for creep in self.creepsEnCours:
             xCreep, yCreep = creep.getPosition() # PRENDRE LA POSITION DU CREEP X,Y
             deltax = self.diference(xTour, xCreep)
             deltaY = self.diference(yTour, yCreep)
             if (deltax <= tour.rayon and deltaY <= tour.rayon):
                print("creep dans le rayon")
                 ## le tag du creep rajouter au tableau de la tour. 
                tour.CreepsInTour.append(creep)
                return len(self.CreepsInTour) > 0
             

    def diference(self, n1, n2):
        return abs(abs(n1)-abs(n2))
           
   
    def tirer(self):
        # On cherche s'il y a des creeps 
        creeps_a_portee = []
        for creep in self.parent.nivoActif.creepsEnCours:
            dist = Helper.calcDistance(self.pos_x, self.pos_y, creep.pos[0], creep.pos[1])
            if dist <= self.rayon:
                creeps_a_portee.append(creep)

        if creeps_a_portee:
            # On cible le premier creep trouvé
            cible = creeps_a_portee[0]
            # Création du missile
            nouveau_missile = Missile(self.pos_x, self.pos_y, self.vitesse_tir, self.force, 2)
            nouveau_missile.cible_x = cible.pos[0]
            nouveau_missile.cible_y = cible.pos[1]
            self.projectile.append(nouveau_missile)
    
      
    def parcourToursPourTirer(self):
        self.tirer()
                

    

class Missile():
    def __init__(self, x, y, vitesse, dmg, taille):
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.dmg = dmg
        self.taille = taille
        self.cible_x =0
        self.cible_y =0
    def bouger_misile(self, creep) :
        #éplace le missile vers destination
        dist = Helper.calcDistance(self.x, self.y, self.cible_x, self.cible_y)
        if dist > self.vitesse:
            angle = Helper.calcAngle(self.x, self.y, self.cible_x, self.cible_y)
            self.x, self.y = Helper.getAngledPoint(angle, self.vitesse, self.x, self.y)
        else:
            # Le missile a atteint sa cible
            self.x, self.y = self.cible_x, self.cible_y
            return True # Signale qu'il a touché
        return False


class Creep():
    def __init__(self,parent):
        self.parent=parent
        self.pos=self.parent.parcours.noeuds[0][:]
        self.cible=1 #indice du noeud de parcours a atteindre
        self.vitesse=2
        self.force=10
        self.creep_vie = 10
        self.axe = 0

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
        
    ## Les creeps suivent le chemin
    def bouge(self):
        ## si le creep arrive a la fin 
        if self.cible >= len(self.parent.parcours.noeuds):
            self.perdre_vie_joueur()
            return
        cible_x, cible_y = self.parent.parcours.noeuds[self.cible]
        curr_x, curr_y = self.pos
        dist_restante = Helper.calcDistance(curr_x, curr_y, cible_x, cible_y)

  
        if dist_restante <= self.vitesse:
            self.pos = [cible_x, cible_y] 
            self.cible += 1  
            if self.cible >= len(self.parent.parcours.noeuds):
                self.perdre_vie_joueur()
        else:
            angle = Helper.calcAngle(curr_x, curr_y, cible_x, cible_y)
            nouv_x, nouv_y = Helper.getAngledPoint(angle, self.vitesse, curr_x, curr_y)
            self.pos = [nouv_x, nouv_y]


    def perdre_vie_joueur(self, valeur=1):
        self.parent.parent.vie -= valeur
        print(self.parent.parent.vie)

    def getPosition(self):
        return self.pos[0], self.pos[1]

class Nivo(): ##Vague
    def __init__(self,parent):
        self.parent=parent
        self.parcours = Parcours()
        self.emplacement = Emplacement()
        self.densiteCreep=3
        #self.tours=[]
        self.creeps={}
        self.creepsEnCours=[]
        self.compteur = 0
        self.creepPopCount = 0
        self.creeCreep()
        
    
    def creerId(self):
       ## s = "creep_" + str(self.compteur)
        s = f"creep_{self.compteur}"
        self.compteur += 1
        print(s)
        return s

        
    def creeCreep(self):
        for i in range(self.parent.creepparnivo):
            self.creeps[self.creerId()] = Creep(self) 
            ## self.creeps.add( Creep(self))
            
    def bougeCreep(self): ## bouger sur le chemin
        if self.creeps:
            ajoute=0
            c=self.creeps["creep_" + str(self.creepPopCount)]
            if self.creepsEnCours:
                cPrecedent=self.creepsEnCours[0]
                if cPrecedent.cible==1:
                    if cPrecedent.pos[c.axe]>c.pos[c.axe]+c.parent.densiteCreep:
                        ajoute=1
            else:
                ajoute=1
            if ajoute:  
                c=self.creeps.pop("creep_" + str(self.creepPopCount))
                self.creepPopCount += 1
                c.pos=self.parcours.noeuds[0][:] 
                c.cible=1 
                self.creepsEnCours.insert(0,c)
        n=0
        for i in self.creepsEnCours:
            n=n+1
            i.bouge()
            if(i.cible >= len(self.parcours.noeuds)):
                self.creepsEnCours.remove(i)

    def nextVague(self):
        
        return True
              

class Partie():
    def __init__(self):
        self.vie=200
        self.cash=250
        self.creepparnivo=12
        self.creepforce=5
        self.nivo=0
        self.compteur = 0
        self.tours=[] # Tableau avec les TOURS
        # self.paused = False
    
    ## Initiation des attributs (Creation de un Niveau)
    def initPartie(self):
            self.nivo=self.nivo+1 ## Le premier niveau
            self.nivoActif=Nivo(self) ## Creation d'une vague

    ## Attribution de la position de la tour
    def setTour(self,pos_x,pos_y):
        print("MODELE",pos_x,pos_y)
        self.nivoActif.setTour(pos_x,pos_y)

    ## Creation de UNE TOUR et on la rajoute dans le tableau
    ## setTour
    def creerTour(self,pos_x,pos_y):
        self.tours.append(Tour(self,pos_x,pos_y))

    ## ID pour les emplacements des carrées
    def creerId(self):
        s = "id_" + str(self.compteur)
        self.compteur += 1
        print(s)
        return s

    ## ajouter les projetctiles pour chaque tour
    def ajour_projectiles(self):
        for t in self.tours:
            for m in t.projectile[:]: 
                touche = m.bouger_misile(None) 
                if touche:
                    t.projectile.remove(m)

    def toursTirent(self):
        for tour in self.tours:
            tour.tirer()
                  
    
    

class Modele():
    def __init__(self, parent):
        self.parent=parent
        self.partie = None
        ##self.isPaused ## la partie


    def demarrePartie(self):
        self.partie = Partie()
        self.partie.initPartie()
        

    ## PAUSE tout le Jeu, LE JOEUR NE PEUT PAS JOUER
    # def pause(self):
    #     if self.paused == False:
    #         self.paused = True
    #     else:
    #         self.paused = False
    
if __name__ == '__main__':
    m=Modele(1)
    m.demarrePartie()
    ##print(m.nivo.creeps)
    print("FIN")