import random
import sys
import ctypes # Pour lancement dans console IDLE python (support suppression de texte)
kernel32 = ctypes.windll.kernel32 # IDLE suppression
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7) # IDLE suppression
class Tools:
    """Outils personnels pour routines :
        - suppression de lignes : suppr(n)
        - conversion nombre en lettre : nbr_abc(n)
        - conversion lettre en nombre : abc_nbr(lettre)
        - Valeur absolue d'un nombre : ValeurAbsolue(n)"""
    def suppr(nlignes) -> None:
        """Supprime n lignes de la console"""
        for i in range(nlignes):
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
    def nbr_abc(n) -> str:
        """Renvoie la lettre à la position n correspondante dans l'alphabet"""
        abc_list=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        return(abc_list[n-1])
    def abc_nbr(a) -> int:
        """Renvoie la position n de la lettre dans l'alphabet"""
        abc_list=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        return(abc_list.index(a)+1)
    def ValeurAbsolue(n) -> int: # Revoie valeur absolue de n
        """Retourne la valeur absolue (positive) de n"""
        if n<0:
            return(-(n))
        else:
            return(n)
    def Proba(n) -> bool:
        """Permet d'ajouter des condition de probabilité :
            - n : Nombre enntre 1 et 100 : %age de chance
            - sortie : True ou False
        """
        tirage = random.randint(1,100)
        if tirage<=n: return(True)
        else: return(False)