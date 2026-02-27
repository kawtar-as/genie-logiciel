import math


class Helper:
    """
    Classe utilitaire pour les calculs géométriques (Version 2026 - Refactorisée).
    """

    @staticmethod
    def get_angled_point(angle: float, longueur: float, cx: float, cy: float) -> tuple[float, float]:
        """
        Calcule un point à une distance et un angle donnés.

        Args:
            angle (float): Angle en radians.
            longueur (float): Distance du centre.
            cx (float): Centre X.
            cy (float): Centre Y.

        Returns:
            tuple[float, float]: (x, y) du point calculé.
        """
        x = (math.cos(angle) * longueur) + cx
        y = (math.sin(angle) * longueur) + cy
        return x, y

    @staticmethod
    def calc_angle(x1: float, y1: float, x2: float, y2: float) -> float:
        """Calcule l'angle en radians entre deux points."""
        dx = x2 - x1
        dy = y2 - y1
        return math.atan2(dy, dx)

    @staticmethod
    def calc_distance(x1: float, y1: float, x2: float, y2: float) -> float:
        """Calcule la distance euclidienne entre deux points."""
        dx = abs(x2 - x1) ** 2
        dy = abs(y2 - y1) ** 2
        return math.sqrt(dx + dy)

    # ------------------------------------------------------------------------
    # PONT DE COMPATIBILITÉ (À SUPPRIMER UNE FOIS LE REFACTORING TERMINÉ)
    # Ces alias permettent au vieux code (modele.py) de fonctionner
    # avec la nouvelle classe Helper sans planter.
    # ------------------------------------------------------------------------
    getAngledPoint = get_angled_point
    calcAngle = calc_angle
    calcDistance = calc_distance