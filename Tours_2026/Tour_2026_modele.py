# -*- coding: ISO-8859-1 -*-
"""
====================================================================
  TOUR DEFENSE 2026 - MODELE
====================================================================
  Contient toute la logique du jeu :
   - Deux patrons de parcours
   - Les niveaux augmentent la difficulte
       * en augmentant la force des creeps
       * en augmentant le nombre de creeps
   - Les tours peuvent beneficier d'ameliorations
       * en terme de morts occasionnees
       * et d'argent disponible
====================================================================
"""

import random
from helper import *
import csv
# ====================================================================
# CLASSE PARCOURS
# ====================================================================
# Definit les chemins (suite de noeuds) que les creeps doivent suivre.
class Parcours():

    def __init__(self, choix_carte=1):
        # Premier parcours simple
        self.noeuds1 = [[0, 10],
                        [50, 10],
                        [50, 80],
                        [100, 80]]

        # Deuxieme parcours plus complexe
        self.noeuds2 = [[0, 10],
                        [20, 10],
                        [20, 40],
                        [50, 40],
                        [50, 20],
                        [80, 20],
                        [80, 60],
                        [30, 60],
                        [30, 80],
                        [100, 80]]

        # Parcours actif utilise dans la partie
        self.noeuds3 = [[0, 0],
                       [22, 35],
                       [53, 35],
                       [53, 23],
                       [75, 23],
                       [75, 55],
                       [33, 55],
                       [33, 77],
                       [100, 77]]
        

        if choix_carte == 1:
            self.noeuds = self.noeuds1
        elif choix_carte == 2:
            self.noeuds = self.noeuds2
        else:
            self.noeuds = self.noeuds3


# ====================================================================
# CLASSE EMPLACEMENT
# ====================================================================
# Gere les cases ou il est possible de poser une tour.
class Emplacement():

    def __init__(self):
        self.isOccupied = None
        # Liste des positions disponibles pour placer une tour
        self.cases = [[100, 55],
                      [56, 150],
                      [161, 90]]


# ====================================================================
# CONFIGURATION DES TOURS
# ====================================================================
# Dictionnaire central qui regroupe toutes les caracteristiques de chaque
# type de tour : prix, force d'attaque, rayon d'action, vitesse de tir.
CONFIG_TOURS = {
    "tour_0": {"prix": 0,   "force": 5, "rayon": 150, "vitesse": 5,"type_missile":"missile_normal"},
    "tour_1": {"prix": 20,  "force": 5, "rayon": 20,  "vitesse": 6,"type_missile":"missile_normal"},
    "tour_2": {"prix": 40,  "force": 5, "rayon": 20,  "vitesse": 1,"type_missile":"missile_normal"},
    "tour_3": {"prix": 80,  "force": 5, "rayon": 25,  "vitesse": 8,"type_missile":"missile_rapide"},
    "tour_4": {"prix": 100, "force": 5, "rayon": 30,  "vitesse": 9,"type_missile":"missile_normal"},
    "tour_5": {"prix": 175, "force": 7, "rayon": 30,  "vitesse": 10,"type_missile":"missile_fort"},
} 
# pour les creep
# reward = argent donne au joueur quand ce creep est tue
# taille  = rayon visuel en pixels (utilise par la vue)
CONFIG_CREEPS = {
    "creep_normal": {"vie": 10,  "vitesse": 2,   "force": 10, "reward": 10,  "taille": 5},
    "creep_rapide": {"vie": 6,   "vitesse": 2.5,   "force": 5,  "reward": 15,  "taille": 4},
    "creep_fort":   {"vie": 40,  "vitesse": 1,   "force": 20, "reward": 25,  "taille": 8},
    "creep_boss":   {"vie": 150, "vitesse": 0.8, "force": 50, "reward": 60,  "taille": 12},
}

CONFIG_TIRS= {
    "missile_normal": {"degat": 10,  "vitesse": 3,"rayon":10,"taille": 5},
    "missile_rapide": {"degat": 20,   "vitesse": 4, "rayon":10,"taille": 7},
    "missile_fort"  : {"degat": 70,   "vitesse": 10, "rayon":10,"taille": 15},
}

# ====================================================================
# CLASSE TOUR
# ====================================================================
# Represente une tour de defense posee sur la carte.
# Elle vise et tire sur les creeps a portee.
class Tour():

    # ----------------------------------------------------------------
    # INITIALISATION
    # ----------------------------------------------------------------

    def __init__(self, parent, pos_x, pos_y, type):
        self.parent = parent
        self.pos_x = pos_x
        self.pos_y = pos_y
        config = CONFIG_TOURS[type]
        self.type = type
        self.prix = config["prix"]
        self.force = config["force"]
        self.rayon = config["rayon"]
        self.vitesse_tir = config["vitesse"]
        # Cible actuellement visee
        self.focus = None
        self.projectile = []
        # Cadence de tir (en ticks)
        self.cooldown = 0
        self.cooldown_max =  max(1,11-self.vitesse_tir)        # ex: 20 ticks = 1 seconde si delai=50ms
        #type de projectile que la tur va utiliser 
        self.type_missile = config.get("type_missile","missile_normal")
    

    # ----------------------------------------------------------------
    # ACCESSEURS
    # ----------------------------------------------------------------

    # Retourne la position de la tour
    def getPosition(self):
        return self.pos_x, self.pos_y

    # ----------------------------------------------------------------
    # DETECTION & CIBLAGE
    # ----------------------------------------------------------------

    # Verifie si un creep est a portee de tir
    def creep_a_portee(self, creep):
        dist = Helper.calcDistance(self.pos_x, self.pos_y,
                                   creep.pos[0], creep.pos[1])
        return dist <= self.rayon

    # Cherche le premier creep a portee et le fixe comme focus
    def chercher_cible(self):
        #if not self.parent.nivoActif : 
            #return
        for creep in reversed(self.parent.nivoActif.creepsEnCours):
            if creep.creep_vie > 0 and self.creep_a_portee(creep):
                self.focus = creep
                return
        self.focus = None
    #Vérifie si la cible actuelle est toujours valide, vivante et à portée.
    # def valider_focus(self):
    #     return (self.focus is not None  
    #             and self.focus in self.parent.nivoActif.creepsEnCours
    #             and self.focus.creep_vie > 0 
    #             and self.creep_a_portee(self.focus))
    # ----------------------------------------------------------------
    # TIR
    # ----------------------------------------------------------------

    # Fait tirer la tour si elle a une cible valide et que le cooldown est fini
    def tirer(self):
        # 1) Decrementer le cooldown
        if self.cooldown > 0:
            self.cooldown -= 1

        # 2) Verifier que la cible actuelle est toujours valable
        focus_valide = (
            self.focus is not None
            and self.focus in self.parent.nivoActif.creepsEnCours
            and self.focus.creep_vie > 0
            and self.creep_a_portee(self.focus)
        )

        # 3) Si plus de cible valable, en chercher une nouvelle
        if not focus_valide:
            self.chercher_cible()
        # 2) Verifier que la cible actuelle est toujours valable
        # focus_valide = (
        #     self.focus is not None
        #     and self.focus in self.parent.nivoActif.creepsEnCours
        #     and self.focus.creep_vie > 0
        #     and self.creep_a_portee(self.focus)
        # )

        # 3) Si plus de cible valable, en chercher une nouvelle
        # if not focus_valide:
        #     self.chercher_cible()

        # 4) Tirer si on a une cible ET que le cooldown est fini
        if self.focus is not None and self.cooldown == 0:
            dictionnaire_missiles = {
                "missile_normal" :MissileNormal,
                "missile_rapide" :MissileRapide,
                "missile_fort" :MissileFort,
            }
            Classe_missile = dictionnaire_missiles.get(self.type_missile,MissileNormal)
            missile = Classe_missile(self.pos_x, self.pos_y, self.focus)
            missile.cible_x = self.focus.pos[0]
            missile.cible_y = self.focus.pos[1]
            self.projectile.append(missile)
            self.cooldown = self.cooldown_max


class TourLaser(Tour):
    def __init__(self, parent, pos_x, pos_y, type_tour="tour_1"):
        super().__init__(parent, pos_x, pos_y, type_tour)
    def tirer(self):
        super().tirer()

            
class TourNormale(Tour):
    def __init__(self, parent, pos_x, pos_y, type_tour="tour_0"):
        super().__init__(parent, pos_x, pos_y, type_tour)  
    def tirer(self):
        super().tirer()

class TourCrazy(Tour):
    def __init__(self, parent, pos_x, pos_y, type_tour="tour_2"):
        super().__init__(parent, pos_x, pos_y, type_tour)  
    def tirer(self):
        super().tirer()

class TourRapidos(Tour):
    def __init__(self, parent, pos_x, pos_y, type_tour="tour_3"):
        super().__init__(parent, pos_x, pos_y, type_tour)  

    def tirer(self):
        super().tirer()

class TourForte(Tour):
    def __init__(self, parent, pos_x, pos_y, type_tour="tour_4"):
        super().__init__(parent, pos_x, pos_y, type_tour)  

    def tirer(self):
        super().tirer()

class TourClassique(Tour):
    def __init__(self, parent, pos_x, pos_y, type_tour="tour_5"):
        super().__init__(parent, pos_x, pos_y, type_tour)  

    def tirer(self):
        super().tirer()

# ====================================================================
# CLASSE MISSILE
# ====================================================================
# Projectile tire par une tour qui suit un creep jusqu'a l'impact.

      
class Missile():

    def __init__(self, x, y, taille, type_missile):
        self.x = x
        self.y = y
        config = CONFIG_TIRS.get(type_missile, CONFIG_TIRS["missile_normal"])
        self.vitesse = config["vitesse"]
        self.degat = config["degat"]
        self.rayon = config["rayon"]
        self.taille = taille
        self.cible_x = 0
        self.cible_y = 0
        self.cible_creep = None      

    def bouger_misile(self):
           # 1) Cible perdue (morte) : le missile s'auto-detruit
        if self.cible_creep is None or self.cible_creep.creep_vie <= 0:
            return True

        # 2) Verifier que la cible est toujours dans la partie
        if self.cible_creep not in self.cible_creep.parent.creepsEnCours:
            return True

        # 3) Cible toujours valide : mise a jour de sa position
        self.cible_x = self.cible_creep.pos[0]
        self.cible_y = self.cible_creep.pos[1]

        dist = Helper.calcDistance(self.x, self.y, self.cible_x, self.cible_y)

        # Trajet vers la cible
        if dist > self.vitesse:
            angle = Helper.calcAngle(self.x, self.y, self.cible_x, self.cible_y)
            self.x, self.y = Helper.getAngledPoint(angle, self.vitesse, self.x, self.y)
            return False
        else:
            # Impact : infliger les degats
            self.x, self.y = self.cible_x, self.cible_y
            self.cible_creep.creep_vie -= self.degat
            return True

            

class MissileNormal(Missile):
    def __init__(self, x, y, cible_creep):
        # On passe la clé de configuration correspondante
        super().__init__(x, y, 2, "missile_normal")
        self.cible_creep = cible_creep
        self.cible_x = cible_creep.pos[0]
        self.cible_y = cible_creep.pos[1]
        
class MissileRapide(Missile):
   
    def __init__(self, x, y, cible_creep):
        super().__init__(x, y, 4, "missile_rapide")
        self.cible_creep = cible_creep 
        self.cible_x = cible_creep.pos[0]
        self.cible_y = cible_creep.pos[1]

class MissileFort(Missile):

    def __init__(self, x, y, cible_creep): 
        super().__init__(x, y, 15, "missile_fort")
        self.cible_creep = cible_creep
        self.rayon_explosion = self.rayon
        self.cible_x = cible_creep.pos[0]
        self.cible_y = cible_creep.pos[1]
    
    

# ====================================================================
# CLASSE CREEP
# ====================================================================
# Ennemi qui parcourt le chemin pour atteindre la base du joueur.
class Creep():
    def __init__(self, parent, type_creep="creep_normal"):
        self.parent = parent
        self.pos = self.parent.parcours.noeuds[0][:]
        self.cible = 1               # Indice du prochain noeud a atteindre
        self.axe = 0
        config = CONFIG_CREEPS[type_creep]
        self.type_creep = type_creep            # utilise par la vue pour la couleur
        # Recuperer le multiplicateur de difficulte depuis Partie (grand-parent de Creep)
        diff = getattr(self.parent.parent, "difficulte", 1.0)
        self.vitesse    = config["vitesse"]                     # vitesse fixe (pas scalee)
        self.force      = config["force"]
        self.creep_vie  = int(config["vie"]  * diff)
        self.vie_max    = self.creep_vie                        # reference fixe pour la barre de vie
        self.taille     = config["taille"]                      # rayon visuel
        self.reward     = config["reward"]                      # argent donne au joueur au kill

        # Determination de l'axe et de la direction initiale de deplacement
        if self.pos[0] != self.parent.parcours.noeuds[1][0]:
            self.axe = 0
            if self.pos[0] < self.parent.parcours.noeuds[1][0]:
                self.dir = 1
            else:
                self.dir = -1
        else:
            self.axe = 1
            if self.pos[1] < self.parent.parcours.noeuds[1][1]:
                self.dir = 1
            else:
                self.dir = -1


    # Retourne la position actuelle du creep
    def getPosition(self):
        return self.pos[0], self.pos[1]


    # Deplace le creep le long du chemin vers le prochain noeud
    def bouge(self):
        # Si le creep a atteint la fin du parcours
        if self.cible >= len(self.parent.parcours.noeuds):
            self.perdre_vie_joueur()
            return

        cible_x, cible_y = self.parent.parcours.noeuds[self.cible]
        curr_x, curr_y = self.pos
        dist_restante = Helper.calcDistance(curr_x, curr_y, cible_x, cible_y)

        # On atteint le noeud : passer au suivant
        if dist_restante <= self.vitesse:
            self.pos = [cible_x, cible_y]
            self.cible += 1
            if self.cible >= len(self.parent.parcours.noeuds):
                self.perdre_vie_joueur()
        # Sinon avancer en direction du noeud
        else:
            angle = Helper.calcAngle(curr_x, curr_y, cible_x, cible_y)
            nouv_x, nouv_y = Helper.getAngledPoint(angle, self.vitesse, curr_x, curr_y)
            self.pos = [nouv_x, nouv_y]


    # Le creep atteint la fin : retire de la vie au joueur
    def perdre_vie_joueur(self, valeur=1):
        self.parent.parent.vie -= valeur
        print(self.parent.parent.vie)

class CreepNormal(Creep):
    def __init__(self, parent):
        super().__init__(parent, "creep_normal")


class CreepRapide(Creep):
    def __init__(self, parent):
        super().__init__(parent, "creep_rapide")


class CreepFort(Creep):
    def __init__(self, parent):
        super().__init__(parent, "creep_fort")


class CreepBoss(Creep):
    def __init__(self, parent):
        super().__init__(parent, "creep_boss") # Utilise les stats de base
        

# ====================================================================
# CLASSE NIVO (VAGUE)
# ====================================================================
# Represente une vague de creeps a affronter.
class Nivo():

    # ----------------------------------------------------------------
    # INITIALISATION
    # ----------------------------------------------------------------

    def __init__(self, parent):
        self.parent = parent
        self.parcours = Parcours()
        self.emplacement = Emplacement()
        self.densiteCreep = 3
        self.creeps = {}             # Creeps en attente
        self.creepsEnCours = []      # Creeps actuellement sur le chemin
        self.compteur = 0
        self.creepPopCount = 0
        self.creeCreep()

    # ----------------------------------------------------------------
    # CREATION DES CREEPS
    # ----------------------------------------------------------------

    # Genere un identifiant unique pour chaque creep
    def creerId(self):
        s = f"creep_{self.compteur}"
        self.compteur += 1
        print(s)
        return s

    # Cree tous les creeps de la vague selon la composition du niveau
    def creeCreep(self):
        composition = self._composition_vague()
        for classe in composition:
            self.creeps[self.creerId()] = classe(self)

    # Retourne la liste ordonnee des classes de creeps pour ce niveau.
    # Plus le niveau est eleve, plus il y a de creeps forts et rapides.
    def _composition_vague(self):
        nivo = self.parent.nivo
        total = self.parent.creepparnivo
        liste = []
        # Boss : 1 par vague a partir du niveau 5, 2 a partir du niveau 10
        nb_boss = 0
        if nivo >= 10:
            nb_boss = 2
        elif nivo >= 5:
            nb_boss = 1
        # Forts : 1/4 du total a partir du niveau 3
        nb_forts = max(0, (total // 4) if nivo >= 3 else 0)
        # Rapides : 1/4 du total a partir du niveau 2
        nb_rapides = max(0, (total // 4) if nivo >= 2 else 0)
        # Normaux : le reste
        nb_normaux = max(0, total - nb_boss - nb_forts - nb_rapides)
        liste  = [CreepNormal]  * nb_normaux
        liste += [CreepRapide]  * nb_rapides
        liste += [CreepFort]    * nb_forts
        liste += [CreepBoss]    * nb_boss
        return liste

    # ----------------------------------------------------------------
    # GESTION DU MOUVEMENT EN VAGUE
    # ----------------------------------------------------------------

    # Fait avancer tous les creeps actifs et libere progressivement
    # ceux en attente selon la densite definie
    def bougeCreep(self):
        # 1) Verifier s'il faut sortir un nouveau creep de la file d'attente
        if self.creeps:
            ajoute = 0
            c = self.creeps["creep_" + str(self.creepPopCount)]
            if self.creepsEnCours[:]:
                cPrecedent = self.creepsEnCours[0]
                if cPrecedent.cible == 1:
                    # Verifier qu'il y a assez d'espace avec le precedent
                    if cPrecedent.pos[c.axe] > c.pos[c.axe] + c.parent.densiteCreep:
                        ajoute = 1
            else:
                ajoute = 1

            # Liberer le creep en tete de file
            if ajoute:
                c = self.creeps.pop("creep_" + str(self.creepPopCount))
                self.creepPopCount += 1
                c.pos = self.parcours.noeuds[0][:]
                c.cible = 1
                self.creepsEnCours.insert(0, c)

        # 2) Deplacer chaque creep actif et retirer ceux qui sont morts
        #    ou arrives a la fin
        for i in self.creepsEnCours[:]:
            i.bouge()
            if i.creep_vie <= 0:
                self.creepsEnCours.remove(i)
                self.parent.cash += i.reward
            if i.cible >= len(self.parcours.noeuds):
                self.creepsEnCours.remove(i)

    # ----------------------------------------------------------------
    # FIN DE VAGUE
    # ----------------------------------------------------------------

    # Indique qu'on peut passer a la vague suivante
    def nextVague(self):
        return True


# ====================================================================
# CLASSE PARTIE
# ====================================================================
# Represente une partie complete : vie, argent, niveaux, tours posees.
class Partie():

    # ----------------------------------------------------------------
    # INITIALISATION
    # ----------------------------------------------------------------

    def __init__(self, choix_carte):
        self.vie = 100
        self.cash = 250
        self.creepparnivo = 10
        self.creepforce = 5
        self.nivo = 0
        self.compteur = 0
        self.tours = []              # Toutes les tours posees
        self.prix_tour = [0, 30, 50, 80, 100, 175]
        self.price = 0

        self.tourActuelle = 0
        ## chemin
        self.carteActive = choix_carte

    # Initialise un nouveau niveau / vague.
    # Chaque niveau augmente le nombre de creeps (+2 par niveau)
    # et scale leurs stats via un multiplicateur.
    def initPartie(self):
        self.nivo += 1
        # +2 creeps par niveau (ex: nivo 1 -> 10, nivo 5 -> 18)
        self.creepparnivo = 8 + self.nivo * 2
        # Multiplicateur de stats : +15 % par niveau
        self.difficulte = 1.0 + (self.nivo - 1) * 0.15
        self.nivoActif = Nivo(self)

    # Genere un identifiant unique (pour les emplacements de cases)
    def creerId(self):
        s = "id_" + str(self.compteur)
        self.compteur += 1
        print(s)
        return s

    # ----------------------------------------------------------------
    # GESTION DES TOURS
    # ----------------------------------------------------------------

    # Place une tour sur le niveau actif
    def setTour(self, pos_x, pos_y):
        print("MODELE", pos_x, pos_y)
        self.nivoActif.setTour(pos_x, pos_y)

    # Cree une tour si le joueur a assez d'argent
    def creerTour(self, pos_x, pos_y, type_selectionne):
        prix = CONFIG_TOURS[type_selectionne]["prix"]
        if self.acheter_tour(prix):
           dictionnaire_tours = {
                "tour_0": TourNormale,
                "tour_1": TourLaser,
                "tour_2": TourCrazy,
                "tour_3": TourRapidos,
                "tour_4": TourForte,
                "tour_5": TourClassique
            }
           
           classeChoisie = dictionnaire_tours.get(type_selectionne, TourNormale)
           nouvelle_tour = classeChoisie(self, pos_x, pos_y, type_selectionne)
           self.tours.append(nouvelle_tour)
           return True
        return False
    
    # Parcourt la liste des tours pour trouver celle aux coordonnées demandées
    def trouver_tour(self, pos_x, pos_y):
        for tour in self.tours:
            # On cherche la correspondance parfaite des coordonnées
            if tour.pos_x == pos_x and tour.pos_y == pos_y:
                self.tourActuelle = tour
                return tour
        return None

    # Fait tirer toutes les tours
    def toursTirent(self):
        for tour in self.tours:
            tour.tirer()

    def changerRayonTour(self):
        cout_upgrade = 20
        if self.tourActuelle and self.cash >= cout_upgrade:
            self.cash -= cout_upgrade
            self.tourActuelle.rayon += 10
            print(f"Rayon améliorée ! Reste {self.cash} argent.")
        else:
            print("Pas de tour sélectionnée ou pas assez d'argent !")

    def changerForceTour(self):
        cout_upgrade = 20
        if self.tourActuelle and self.cash >= cout_upgrade:
            self.cash -= cout_upgrade
            self.tourActuelle.force += 10
            print(f"Force améliorée ! Reste {self.cash} argent.")
        else:
            print("Pas de tour sélectionnée ou pas assez d'argent !")

    # ----------------------------------------------------------------
    # GESTION DES PROJECTILES
    # ----------------------------------------------------------------

    # Met a jour tous les projectiles et retire ceux qui ont touche
    def ajour_projectiles(self):
        for t in self.tours:
            for m in t.projectile.copy():
                touche = m.bouger_misile()
                if touche:
                    t.projectile.remove(m)

    # ----------------------------------------------------------------
    # ECONOMIE DU JEU
    # ----------------------------------------------------------------

    # Tente d'acheter une tour : deduit le prix si le joueur a assez d'argent
    def acheter_tour(self, prix):
        if self.cash >= prix:
            self.cash -= prix
            print(self.cash)
            return True
        else:
            print(self.cash)
            return False

    # ----------------------------------------------------------------
    # ETAT DE LA VAGUE
    # ----------------------------------------------------------------

    # Verifie si la vague est terminee (plus aucun creep en attente ni en cours)
    def vagueTerminee(self):
        if len(self.nivoActif.creeps) == 0 and len(self.nivoActif.creepsEnCours) == 0:
            return True
        else:
            return False
    def sauvegarder(self,valeur):
        with open("fichier.csv", mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([valeur, self.score])

    
    def sauvegarder_score_csv(self,nom_joueur):
        
        fichier = "scores.csv"
        score_calcule = (self.nivo * 100) + self.cash
        
        # Écrit le nom et le score
        with open(fichier, 'a', newline='', encoding='UTF-8') as f:
            writer = csv.writer(f)
            writer.writerow([nom_joueur, score_calcule])
        print("✓ Score sauvegardé dans scores.csv")

    def verifier_game_over(self):
        # Condition 1 : Vie <= 0 (défaite)
        if self.vie <= 0:
            return True, 
        # Condition 2 : Niveau 15 atteint (victoire)
        if self.nivo >= 2:
            return True, 
        
        return False, None
# ====================================================================
# CLASSE MODELE
# ====================================================================
# Point d'entree principal du modele : gere la partie en cours.
class Modele():

    def __init__(self, parent):
        self.parent = parent
        self.partie = None

    # Demarre une nouvelle partie et initialise son premier niveau
    def demarrePartie(self, choix_carte):
        self.partie = Partie(choix_carte)
        self.partie.initPartie()


# ====================================================================
# POINT D'ENTREE (TEST)
# ====================================================================

if __name__ == '__main__':
    m = Modele(1)
    m.demarrePartie()
    print("FIN")
#MODELE