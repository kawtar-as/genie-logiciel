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


# ====================================================================
# CONFIGURATION DES TOURS
# ====================================================================
# Dictionnaire central qui regroupe toutes les caracteristiques de chaque
# type de tour : prix, force d'attaque, rayon d'action, vitesse de tir.
CONFIG_TOURS = {
    "tour_0": {"prix": 0,   "force": 5, "rayon": 150, "vitesse": 5},
    "tour_1": {"prix": 20,  "force": 5, "rayon": 20,  "vitesse": 6},
    "tour_2": {"prix": 40,  "force": 5, "rayon": 20,  "vitesse": 7},
    "tour_3": {"prix": 80,  "force": 5, "rayon": 25,  "vitesse": 8},
    "tour_4": {"prix": 100, "force": 5, "rayon": 30,  "vitesse": 9},
    "tour_5": {"prix": 175, "force": 7, "rayon": 30,  "vitesse": 10},
}


# ====================================================================
# CLASSE PARCOURS
# ====================================================================
# Definit les chemins (suite de noeuds) que les creeps doivent suivre.
class Parcours():

    def __init__(self):
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
        self.noeuds = [[0, 0],
                       [22, 35],
                       [53, 35],
                       [53, 23],
                       [75, 23],
                       [75, 55],
                       [33, 55],
                       [33, 77],
                       [100, 77]]


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

        # Lecture de la configuration selon le type de tour
        config = CONFIG_TOURS[type]
        self.type = type
        self.prix = config["prix"]
        self.force = config["force"]
        self.rayon = config["rayon"]
        self.vitesse_tir = config["vitesse"]

        # Liste des projectiles actifs tires par cette tour
        self.projectile = []

        # Cible actuellement visee
        self.focus = None

        # Cadence de tir (en ticks)
        self.cooldown = 0
        self.cooldown_max = 10        # ex: 20 ticks = 1 seconde si delai=50ms

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
        for creep in reversed(self.parent.nivoActif.creepsEnCours):
            if creep.creep_vie > 0 and self.creep_a_portee(creep):
                self.focus = creep
                return
        self.focus = None

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

        # 4) Tirer si on a une cible ET que le cooldown est fini
        if self.focus is not None and self.cooldown == 0:
            missile = Missile(self.pos_x, self.pos_y,
                              self.vitesse_tir, self.force, 2)
            missile.cible_creep = self.focus
            missile.cible_x = self.focus.pos[0]
            missile.cible_y = self.focus.pos[1]
            self.projectile.append(missile)
            self.cooldown = self.cooldown_max


# ====================================================================
# CLASSE MISSILE
# ====================================================================
# Projectile tire par une tour qui suit un creep jusqu'a l'impact.
class Missile():

    def __init__(self, x, y, vitesse, dmg, taille):
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.dmg = dmg
        self.taille = taille
        self.cible_x = 0
        self.cible_y = 0
        self.cible_creep = None      # Reference au creep vise

    # Deplace le missile vers son creep cible. Retourne True s'il touche
    # ou si la cible n'existe plus.
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
            self.cible_creep.creep_vie -= self.dmg
            return True


# ====================================================================
# CLASSE CREEP
# ====================================================================
# Ennemi qui parcourt le chemin pour atteindre la base du joueur.
class Creep():

    # ----------------------------------------------------------------
    # INITIALISATION
    # ----------------------------------------------------------------

    def __init__(self, parent):
        self.parent = parent
        self.pos = self.parent.parcours.noeuds[0][:]
        self.cible = 1               # Indice du prochain noeud a atteindre
        self.vitesse = 2
        self.force = 10
        self.creep_vie = 10
        self.axe = 0

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

    # ----------------------------------------------------------------
    # ACCESSEURS
    # ----------------------------------------------------------------

    # Retourne la position actuelle du creep
    def getPosition(self):
        return self.pos[0], self.pos[1]

    # ----------------------------------------------------------------
    # DEPLACEMENT
    # ----------------------------------------------------------------

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

    # ----------------------------------------------------------------
    # IMPACT SUR LE JOUEUR
    # ----------------------------------------------------------------

    # Le creep atteint la fin : retire de la vie au joueur
    def perdre_vie_joueur(self, valeur=1):
        self.parent.parent.vie -= valeur
        print(self.parent.parent.vie)


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

    # Cree tous les creeps de la vague
    def creeCreep(self):
        for i in range(self.parent.creepparnivo):
            self.creeps[self.creerId()] = Creep(self)

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
            if self.creepsEnCours:
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
        for i in self.creepsEnCours:
            i.bouge()
            if i.creep_vie <= 0:
                self.creepsEnCours.remove(i)
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

    def __init__(self):
        self.vie = 200
        self.cash = 20
        self.creepparnivo = 10
        self.creepforce = 5
        self.nivo = 0
        self.compteur = 0
        self.tours = []              # Toutes les tours posees
        self.prix_tour = [0, 30, 50, 80, 100, 175]
        self.price = 0

    # Initialise un nouveau niveau / vague
    def initPartie(self):
        self.nivo = self.nivo + 1
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
            nouvelle_tour = Tour(self, pos_x, pos_y, type_selectionne)
            self.tours.append(nouvelle_tour)
            return True
        return False

    # Fait tirer toutes les tours
    def toursTirent(self):
        for tour in self.tours:
            tour.tirer()

    # ----------------------------------------------------------------
    # GESTION DES PROJECTILES
    # ----------------------------------------------------------------

    # Met a jour tous les projectiles et retire ceux qui ont touche
    def ajour_projectiles(self):
        for t in self.tours:
            for m in t.projectile[:]:
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


# ====================================================================
# CLASSE MODELE
# ====================================================================
# Point d'entree principal du modele : gere la partie en cours.
class Modele():

    def __init__(self, parent):
        self.parent = parent
        self.partie = None

    # Demarre une nouvelle partie et initialise son premier niveau
    def demarrePartie(self):
        self.partie = Partie()
        self.partie.initPartie()


# ====================================================================
# POINT D'ENTREE (TEST)
# ====================================================================

if __name__ == '__main__':
    m = Modele(1)
    m.demarrePartie()
    print("FIN")
