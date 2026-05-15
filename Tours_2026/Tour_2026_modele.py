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

# Dans ton modèle ou un fichier de constantes
CONFIG_TOURS = {
    "tour_0": {"prix": 0, "force": 5, "rayon": 150, "vitesse": 5},
    "tour_1": {"prix": 20, "force": 5, "rayon": 20, "vitesse": 6},
    "tour_2": {"prix": 40, "force": 5, "rayon": 20, "vitesse": 7},
    "tour_3": {"prix": 80, "force": 5, "rayon": 25, "vitesse": 8},
    "tour_4": {"prix": 100, "force": 5, "rayon": 30, "vitesse": 9},
    "tour_5": {"prix": 175, "force": 7, "rayon": 30, "vitesse": 10},
    
    
    # ... etc
}
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
    def __init__(self, parent, pos_x, pos_y, type):
        self.parent = parent
        self.pos_x = pos_x
        self.pos_y = pos_y
        config = CONFIG_TOURS[type]
        self.type = type
        self.prix = config["prix"]
        self.force = config["force"]
        self.rayon = config["rayon"]           # rayon depuis la config (NE PAS écraser)
        self.vitesse_tir = config["vitesse"]
        self.projectile = []

        # --- Focus / cible ---
        self.focus = None                       # creep actuellement visé (ou None)

        # --- Cadence de tir ---
        self.cooldown = 0                       # ticks restants avant le prochain tir
        self.cooldown_max = 10                  # ex: 20 ticks ≈ 1 seconde si delai=50ms

    def getPosition(self):
        return self.pos_x, self.pos_y

    def creep_a_portee(self, creep):
        """Vrai si le creep est dans le rayon de la tour."""
        dist = Helper.calcDistance(self.pos_x, self.pos_y,
                                   creep.pos[0], creep.pos[1])
        return dist <= self.rayon

    def chercher_cible(self):
        """Cherche le premier creep à portée et le fixe comme focus."""
        for creep in reversed(self.parent.nivoActif.creepsEnCours):
            if creep.creep_vie > 0 and self.creep_a_portee(creep):
                self.focus = creep
                return
        self.focus = None

    def tirer(self):
        # 1) Décrémenter le cooldown
        if self.cooldown > 0:
            self.cooldown -= 1

        # 2) Vérifier que le focus actuel est toujours valable
        focus_valide = (
            self.focus is not None
            and self.focus in self.parent.nivoActif.creepsEnCours
            and self.focus.creep_vie > 0
            and self.creep_a_portee(self.focus)
        )

        # 3) Si plus de focus valable, en chercher un nouveau
        if not focus_valide:
            self.chercher_cible()

        # 4) Tirer si on a une cible ET que le cooldown est fini
        if self.focus is not None and self.cooldown == 0:
            missile = Missile(self.pos_x, self.pos_y,
                              self.vitesse_tir, self.force, 2)
            missile.cible_creep = self.focus    # référence directe au creep
            missile.cible_x = self.focus.pos[0]
            missile.cible_y = self.focus.pos[1]
            self.projectile.append(missile)
            self.cooldown = self.cooldown_max


class Missile():
    def __init__(self, x, y, vitesse, dmg, taille):
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.dmg = dmg
        self.taille = taille
        self.cible_x = 0
        self.cible_y = 0
        self.cible_creep = None                 # référence au creep visé

    def bouger_misile(self):
        """Le missile suit le creep en mouvement. Retourne True s'il touche."""
        # 1) Cible perdue (morte ou sortie du chemin) → le missile s'auto-détruit
        if self.cible_creep is None or self.cible_creep.creep_vie <= 0:
            return True
        
        # 2) On vérifie aussi qu'elle est encore dans la partie
        if self.cible_creep not in self.cible_creep.parent.creepsEnCours:
            return True
        
        # 3) Cible toujours valide : on la suit
        self.cible_x = self.cible_creep.pos[0]
        self.cible_y = self.cible_creep.pos[1]

        dist = Helper.calcDistance(self.x, self.y, self.cible_x, self.cible_y)

        if dist > self.vitesse:
            angle = Helper.calcAngle(self.x, self.y, self.cible_x, self.cible_y)
            self.x, self.y = Helper.getAngledPoint(angle, self.vitesse, self.x, self.y)
            return False
        else:
            # Impact : infliger les dégâts
            self.x, self.y = self.cible_x, self.cible_y
            self.cible_creep.creep_vie -= self.dmg
            return True



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
            #delete creep si pas de vie
            if(i.creep_vie <= 0):
                self.creepsEnCours.remove(i)
            if(i.cible >= len(self.parcours.noeuds)):
                self.creepsEnCours.remove(i)

    def nextVague(self):
        return True
              

class Partie():
    def __init__(self):
        self.vie=200
        self.cash=20
        self.creepparnivo=5
        self.creepforce=5
        self.nivo=0
        self.compteur = 0
        self.tours=[] # Tableau avec les TOURS
        self.prix_tour = [0,30,50,80,100,175]
        self.price = 0
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
    def creerTour(self,pos_x,pos_y,type_selectionne):
       prix = CONFIG_TOURS[type_selectionne]["prix"]
       if self.acheter_tour(prix): 
            # On passe le type à l'objet Tour pour qu'il s'auto-configure
            nouvelle_tour = Tour(self, pos_x, pos_y, type_selectionne)
            self.tours.append(nouvelle_tour)
            return True
       return False

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
                touche = m.bouger_misile() 
                if touche:
                    t.projectile.remove(m)

    def toursTirent(self):
        for tour in self.tours:
            tour.tirer()

    def acheter_tour(self,prix):
            if self.cash >= prix:
                self.cash -= prix
                print( self.cash )
                return True
            else:
                print( self.cash )
                return False
    
    def vagueTerminee(self):
        if len(self.nivoActif.creeps) == 0 and len(self.nivoActif.creepsEnCours) == 0:  
            return True
        else: 
            return False 
                  
    
    

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