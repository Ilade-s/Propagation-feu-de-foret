from random import shuffle # Pour mélange aléatoire de la grille
from time import perf_counter,sleep # Commandes pauses + chronomètre performance
import matplotlib.pyplot as plt # Commandes plots
import matplotlib.gridspec as gridspec # Commandes pour multiplots
import matplotlib.colors as clr # Couleur plot de grille
import sys # Commandes suppression de texte + arrêt du programme
import ctypes # Pour lancement dans console IDLE python (support suppression de texte)
from termcolor import colored # Commandes pour couleur texte
kernel32 = ctypes.windll.kernel32 # IDLE
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7) # IDLE
def suppr(nlignes) -> None: # Fonction suppression de n lignes
    for i in range(nlignes):
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")
class FeuDeForet: # Objet grid feu
    def __init__(self) -> None: # Initialisation variables (+ génération)
        self.grid = []
        self.GenGrid()
        self.TypeAffichage = int(input('Pause entre chaque étape (affichage console) : retourner 1 ; Pause de 1s entre chaque étape (affichage plot) : retourner 0 ; ou résultat "instantané" : retourner 2 : '))
        self.t = 0
        self.tp = 0
    def GenGrid(self) -> None: # Génération Forêt (fonction fille de __init__)
        """Génére la grille de foret et affiche le temps d'exécution dans console"""
        self.nl = int(input('Nombre lignes : '))
        self.nc = int(input('Nombre colonnes : '))
        nC = self.nl*self.nc
        self.ta = round(float(input('Taux d\'arbres (0 à 1): ')),2)
        self.nfi = int(input('Combien d\'arbres en feu au départ ? : '))
        self.narbres = round(self.ta*nC)
        print('\tCréation cases...')
        start = perf_counter()
        g = [2 for i in range(int(self.nfi))]+[1 for j in range(int(self.narbres-self.nfi))]+[0 for ii in range(int(nC-self.narbres))]
        print('\t\t\tTerminé !')
        print('\tMélange...')
        shuffle(g) # Mélange aléatoire liste
        print('\t\t\tTerminé !')
        for i in range(self.nl):
            self.grid.append(g[i*self.nc:(i+1)*self.nc])
        end = perf_counter()
        execution_time = round(end - start,3)
        print('\tTemps d\'exécution : '+str(execution_time)+' secondes')
    def FuncMere(self) -> None: # Fonction principale programme
        """Fonction principale, appelle le reste des fonctions"""
        self.affichage(True) # Setup affichage
        # Initialisation variables pour boucle
        nar=self.narbres
        nfr=self.nfi
        listArbresRestants = []
        listFeuxRestants = []
        print('Simulation en cours...')
        start = perf_counter()
        while nfr!=0: # Boucle êtat de la foret
            self.t+=1
            self.FuncPropFeu()
            nar = sum([il.count(1) for il in self.grid])
            nfr = sum([il.count(2)+il.count(3) for il in self.grid])
            if self.TypeAffichage!=2:
                print('Arbres restants : '+str(nar+nfr)+' // '+str(round(((nar+nfr)/self.narbres)*100,3))+'%')
                print('Arbres en feu : '+str(nfr))
                print('Temps passé : '+str(self.t))
            self.affichage()
            listArbresRestants.append(nar+nfr)
            listFeuxRestants.append(nfr)
        if nfr!=0: # Passe supplémentaire (correction bug)
            self.t+=1
            self.FuncPropFeu()
            nar = sum([il.count(1) for il in self.grid])
            nfr = sum([il.count(2)+il.count(3) for il in self.grid])
            self.affichage()
            listArbresRestants.append(nar+nfr)
            listFeuxRestants.append(nfr)
        end = perf_counter()
        execution_time = round(end - start,3)
        # Etat final de la simulation
        self.affichage()
        print('\tTerminé !', end=' ')
        print('\tTemps d\'exécution : '+str(execution_time)+' secondes')
        print('Arbres restants : '+str(nar+nfr)+' // '+str(round(((nar+nfr)/self.narbres)*100,3))+'%')
        print('Arbres en feu : '+str(nfr))
        print('Temps passé : '+str(self.t))
        # Création multi plots
        fig2 = plt.figure(constrained_layout=True)
        spec2 = gridspec.GridSpec(ncols=1, nrows=2, figure=fig2)

        # Remplissage plot arbres restants
        f2_ax1 = fig2.add_subplot(spec2[0, 0])
        f2_ax1.set_title('Nombre d\'arbres')
        if len(listArbresRestants)<100: # Courbe temps court
            f2_ax1.plot(listArbresRestants,'o-')
        else: # Courbe temps long
            f2_ax1.plot(listArbresRestants)

        # Remplissage plot feux
        f2_ax2 = fig2.add_subplot(spec2[1, 0])
        f2_ax2.set_title('Nombre de feux')
        if len(listFeuxRestants)<100: # Courbe temps court
            f2_ax2.plot(listFeuxRestants,'ro-')
        else: # Courbe temps long
            f2_ax2.plot(listFeuxRestants,'r')

        # Affichage plots
        plt.suptitle('Configuration : '+str(self.nl)+'*'+str(self.nc)+' // Taux d\'arbres : '+str(self.ta))
        plt.xlabel('Temps passé')
        plt.ylabel('Nombre arbres')
        plt.show()
    def FuncPropFeu(self) -> None: # Fonction fille de FuncMere utilisée dans la boucle
        """Exécute une passe de propagation du feu dans self.grid (la forêt)"""
        for l in range(self.nl): # Boucle pour étude de tous les éléments de la grille (ligne)
            for c in range(self.nc): # Boucle pour étude de tous les éléments de la grille (colonne)
                if self.grid [l] [c]==2 or self.grid [l] [c]==3: # Détection états case + mise à feu cases adjacentes (si applicable)
                    if l!=0:
                        if self.grid [l-1] [c]==1: # Voisin haut
                            self.grid [l-1] [c] = 5
                    if l!=self.nl-1:
                        if self.grid [l+1] [c]==1: # Voisin bas
                            self.grid [l+1] [c] = 5
                    if c!=self.nc-1:
                        if self.grid [l] [c+1]==1: # Voisin droite
                            self.grid [l] [c+1] = 5
                    if c!=0:
                        if self.grid [l] [c-1]==1: # Voisin gauche
                            self.grid [l] [c-1] = 5 
                    if self.grid [l] [c]==3:
                        self.grid [l] [c] = 4 # Changement d'état de l'arbre de feu à brulé (état inerte)
                    else:
                        self.grid [l] [c] = 3
        for il in self.grid: # Boucle pour remplacement nouveaux feux en feux normaux (Correction bug)
            il[:] = [2 if x==5 else x for x in il]
            il[:] = [3 if x==6 else x for x in il]  
    def affichage(self, setup=False) -> None: # Affichage de la foret
        """Affiche la foret en console ou en plot en fonction de self.TypeAffichage (0 : plot ; 1 : console ; 2 : instantané)
            - #FF0000 = rouge (3)
            - #000000 = noir (4)
            - #00BE00 = vert (1)
            - #9A4A00 = marron (0) (bleu en console)
            - #FFBF00 = orange (2)"""
        if self.TypeAffichage==2: return(-1) # Vérif si affichage demandé ou non
        if setup: # Demandes et actions si il s'agit du premier affichage ou non
            while self.tp==0: # Demande du temps d'intervalle si il n'a pas déjà été défini 
                self.tp = round(float(input('\tCombien de temps entre entre chaque étape ? : ')),2)
                if self.tp==0:
                    suppr(1)
            print('Forêt de départ : ')
            print('Nombre d\'arbres au départ : '+str(self.narbres))
            print('Temps passé : '+str(self.t))
        else:
            if self.TypeAffichage==1:
                suppr(self.nl+4)
            elif self.TypeAffichage==0:
                suppr(3)
        # Affichage en lui même
        if self.TypeAffichage==0: # Affichage grille en couleur
            cmap = clr.ListedColormap(['#9A4A00','#00BE00','#FFBF00','#FF0000','#000000'])
            Boundaries = [-0.1,0.9,1.9,2.9,3.9,4.9]
            Z = self.grid
            norm = clr.BoundaryNorm(Boundaries, ncolors=5)
            fig, ax = plt.subplots()
            ax.pcolormesh(Z,cmap=cmap,norm=norm)
            # Ajout texte plot
            plt.suptitle('Forêt (Temps passé : '+str(self.t)+') : ')
            plt.title('Configuration : '+str(self.nl)+'*'+str(self.nc)+' // Taux d\'arbres : '+str(self.ta))
            plt.xlabel('Colonnes')
            plt.ylabel('Lignes')
            plt.savefig("feu_de_foret/fig")
            plt.close()
            plt.pause(self.tp)
        elif self.TypeAffichage==1: # Affichage grille en console (couleur aussi)
            for l in self.grid:
                print('\t',end=' ')
                for c in l:
                    if c==0: # Case vide (eau?)
                        print(colored(c, 'blue'),end=' ')  
                    elif c==1: # Arbre
                        print(colored(c, 'green'),end=' ') 
                    elif c==2: # Feu 1
                        print(colored(c, 'yellow'),end=' ') 
                    elif c==3: # Feu 2
                        print(colored(c, 'red'),end=' ') 
                    elif c==4: # Cendres?
                        print(c,end=' ') 
                print(' ')
            sleep(self.tp)
print('Ce programme permet de simuler un feu de forêt')
Feu = FeuDeForet()
Feu.FuncMere()
