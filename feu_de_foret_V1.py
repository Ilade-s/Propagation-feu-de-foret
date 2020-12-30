from random import* # Pour mélange aléatoire de la grille
from time import* # Commandes pauses + chronomètre performance
import matplotlib.pyplot as plt # Commandes plots
import matplotlib.gridspec as gridspec # Commandes pour multiplots
import matplotlib.colors as clr # Couleur plot de grille
import sys # Commandes suppression de texte + arrêt du programme
import ctypes # Pour lancement dans console IDLE python (support suppression de texte)
from termcolor import colored # Commandes pour couleur texte
kernel32 = ctypes.windll.kernel32 # IDLE
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7) # IDLE
def creerGrille(nombreLignes, nombreColonnes, narbres, nfi): # Boucle pour création grille initiale + retour graphique
    grid = []
    ncases=nombreColonnes*nombreLignes
    print('\tCréation cases...')
    while len(grid)<nfi: # Boucle ajout arbres en feu
        grid.append(2)
    while len(grid)<ncases: # Boucle ajout arbres + cases vides
        while (grid.count(1)+grid.count(2))<narbres:
            grid.append(1)
            print(str(len(grid))+' // '+str(round((len(grid)/ncases)*100,3))+'%')
            sys.stdout.write("\033[F")
        if len(grid)<ncases: # Correction case vide si taux d'arbres=1
            grid.append(0)
        print(str(len(grid))+' // '+str(round((len(grid)/ncases)*100,3))+'%')
        sys.stdout.write("\033[F")
    print('\t\t\tTerminé !')
    shuffle(grid) # Mélange aléatoire liste
    return(grid)
def affichage(grid,nl,nc,tinput,t,tp): # Séparation grille pour affichage
    if tinput==2: # Affichage grille en couleur
        #FF0000 = rouge
        #000000 = noir
        #00BE00 = vert
        #9A4A00 = marron
        cmap = clr.ListedColormap(['#9A4A00','#00BE00','#FF0000','#000000'])
        Boundaries = [-0.1,0.9,1.9,2.9,3.9]
        norm = clr.BoundaryNorm(Boundaries, ncolors=4)
        Z = grid 
        fig, ax = plt.subplots()
        #ax.pcolormesh(Z,cmap=cmap,norm=norm)
        plt.title('Forêt (Temps passé : '+str(t)+') : ')
        plt.xlabel('Colonnes')
        plt.ylabel('Lignes')
        ax.cla()
        ax.imshow(Z,cmap=cmap,norm=norm)
        plt.title('Forêt (Temps passé : '+str(t)+') : ')
        plt.xlabel('Colonnes')
        plt.ylabel('Lignes')
        plt.pause(tp)
        plt.close()
    else: # Affichage grille en console
        for i in grid:
            llist = []
            for ii in i:
                llist.append(ii)
            print(colored(llist, 'green')) # Impression d'une ligne (boucle)
def prop_feu(grid): # Boucle tests réactions entre les cases
    for l in range(0,len(grid)): # Boucle pour étude de tous les éléments de la grille (ligne)
        for c in range(0,len(grid[l])): # Boucle pour étude de tous les éléments de la grille (colonne)
            if grid [l] [c]==2: # Détection états case + mise à feu cases adjacentes (si applicable)
                if l==0: # Coté vertical haut
                    if c==0: # Coin en haut à gauche (2 voisins constants)
                        if grid [0] [1]==1: # Voisin droite
                            grid [0] [1] = 4
                        if grid [1] [0]==1: # Voisin bas
                            grid [1] [0] = 4                    
                    elif c==nc-1:  # Coin en haut à droite (2 voisins constants)
                        if grid [0] [c-1]==1: # Voisin gauche
                            grid [0] [c-1] = 4
                        if grid [1] [c]==1: # Voisin bas
                            grid [1] [c] = 4
                    else: # autres cases sauf coins (3 voisins)
                        if grid [0] [c-1]==1: # Voisin gauche
                            grid [0] [c-1] = 4
                        if grid [0] [c+1]==1: # Voisin droite
                            grid [0] [c+1] = 4
                        if grid [1] [c]==1: # Voisin bas
                            grid [1] [c] = 4
                elif l==nl-1:  # Coté vertical bas
                    if c==0: # Coin en bas à gauche (2 voisins constants)
                        if grid [l] [1]==1: # Voisin droite
                            grid [l] [1] = 4
                        if grid [l-1] [0]==1: # Voisin haut
                            grid [l-1] [0] = 4
                    elif c==nc-1:  # Coin en bas à droite (2 voisins constants)
                        if grid [l] [c-1]==1: # Voisin gauche
                            grid [l] [c-1] = 4
                        if grid [l-1] [c]==1: # Voisin haut
                            grid [l-1] [c] = 4
                    else: # autres cases sauf coins (3 voisins)
                        if grid [l] [c-1]==1: # Voisin gauche
                            grid [l] [c-1] = 4
                        if grid [l-1] [c]==1: # Voisin haut
                            grid [l-1] [c] = 4
                        if grid [l] [c+1]==1: # Voisin droite
                            grid [l] [c+1] = 4
                else: # Autres lignes non cotés
                    if c==0: # Coté latéral gauche sauf coins (3 voisins)
                        if grid [l-1] [0]==1: # Voisin haut
                            grid [l-1] [0] = 4
                        if grid [l+1] [0]==1: # Voisin bas
                            grid [l+1] [0] = 4
                        if grid [l] [1]==1: # Voisin droite
                            grid [l] [1] = 4
                    elif c==nc-1:  # Coin latéral droit sauf coins (3 voisins)
                        if grid [l-1] [c]==1: # Voisin haut
                            grid [l-1] [c] = 4
                        if grid [l+1] [c]==1: # Voisin bas
                            grid [l+1] [c] = 4
                        if grid [l] [c-1]==1: # Voisin gauche
                            grid [l] [c-1] = 4
                    else: # autres cases (4 voisins)
                        if grid [l-1] [c]==1: # Voisin haut
                            grid [l-1] [c] = 4
                        if grid [l+1] [c]==1: # Voisin bas
                            grid [l+1] [c] = 4
                        if grid [l] [c+1]==1: # Voisin droite
                            grid [l] [c+1] = 4
                        if grid [l] [c-1]==1: # Voisin gauche
                            grid [l] [c-1] = 4
                grid [l] [c] = 3 # Changement d'état de l'arbre de feu à brulé (état inerte)
    for il in grid: # Boucle pour remplacement nouveaux feux en feux normaux (Correction bug)
        il[:] = [2 if x==4 else x for x in il] 
    return(grid)
# Interface utilisateur + initialisation boucle
print('Ce programme permet de simuler un feu de forêt')
nl = int(input('Nombre lignes : '))
nc = int(input('Nombre colonnes : '))
if nc<=0 or nl<=0: # Arrêt du programme en cas de valeurs impossibles
    print('Valeurs impossibles (nombre nul ou négatif)')
    sys.exit()
nC = nl*nc
if nC>50000: # Avertissement pour simulation trop grande
    print('Attention, cette simulation va prendre un certain moment pour être générée')
    if input('Appuyez sur 0 pour continuer, une autre touche pour quitter... ')!='0':
        print('Arrêt du programme')
        sys.exit()
    print('Suite du programme...')
    sleep(1)
    sys.stdout.write("\033[F")
ta = round(float(input('Taux d\'arbres (0 à 1): ')),2)
nfi = int(input('Combien d\'arbres en feu au départ ? : '))
na = ta*nc*nl
print('Création forêt aléatoire...')
start = perf_counter()
g = creerGrille(nl, nc, na, nfi) # Création de la grille
end = perf_counter()
execution_time = round(end - start,3)
print('\tTemps d\'exécution : '+str(execution_time)+' secondes')
grid = []
for i in range(nl):
    grid.append(g[i*nc:(i+1)*nc])
tinput = int(input('Pause de 1s entre chaque étape (affichage console) : retourner 0 ; Pause de 1s entre chaque étape (affichage plot) : retourner 2 ; ou résultat instantané : retourner 1 : '))
# Fin interface utilisateur
t=0
tp=0
if tinput==0 or tinput==2: # Affichage forêt initiale si demandé
    plt.ion()
    if tinput==2:
        tp = round(float(input('\tCombien de temps entre entre chaque graphe ? : ')),2)
    print('Forêt de départ : ')
    print('Nombre d\'arbres au départ : '+str(na))
    print('Temps passé : '+str(t))
    affichage(grid,nl,nc,tinput,t,tp)
    if tinput==0:
        sleep(2)
nar=na
nfr=nfi
list_plot_ar = []
list_plot_af = []
if tinput==1:
    print('Simulation en cours...')
start = perf_counter()
while nar!=0 and nfr!=0: # Boucle états de la forêt
    nar=0
    nfr=0 
    t=t+1
    igrid = prop_feu(grid)
    for il in igrid:
        nar = nar+il.count(1)
        nfr = nfr+il.count(2)
    if tinput==0 or tinput==2:
        if tinput==0:
            for s in range(nl+3): # Suppression grille précédente
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
        elif tinput==2:
            for s in range(3): # Suppression grille précédente
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
        print('Arbres restants : '+str(nar+nfr)+' // '+str(round(((nar+nfr)/na)*100,3))+'%')
        print('Arbres en feu : '+str(nfr))
        print('Temps passé : '+str(t))
        affichage(igrid,nl,nc,tinput,t,tp)
    list_plot_ar.append(nar+nfr)
    list_plot_af.append(nfr)
    if tinput==0:
        sleep(1)
if nfr!=0: # Correction dernier arbre en feu
    nar=0
    nfr=0  
    igrid = prop_feu(grid)
    for il in igrid:
        nar = nar+il.count(1)
        nfr = nfr+il.count(2)
        nbr = na-nar
    t=t+1
    if tinput==0 or tinput==2:
        if tinput==0:
            for s in range(nl+3): # Suppression grille précédente
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
        elif tinput==2:
            for s in range(3): # Suppression grille précédente
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
        if tinput==0:
            affichage(igrid,nl,nc,tinput,t,tp)
    list_plot_ar.append(nar+nfr)
    list_plot_af.append(nfr)
end = perf_counter()
execution_time = round(end - start,3)
# Etat final de la simulation
print('\tTerminé !', end=' ')
print('\tTemps d\'exécution : '+str(execution_time)+' secondes')
print('Arbres restants : '+str(nar+nfr)+' // '+str(round(((nar+nfr)/na)*100,3))+'%')
print('Arbres en feu : '+str(nfr))
print('Temps passé : '+str(t))
plt.close()
plt.ioff()
# Création multi plots
fig2 = plt.figure(constrained_layout=True)
spec2 = gridspec.GridSpec(ncols=1, nrows=2, figure=fig2)

# Remplissage plot arbres restants
f2_ax1 = fig2.add_subplot(spec2[0, 0])
f2_ax1.set_title('Nombre d\'arbres')
if len(list_plot_ar)<100: # Courbe temps court
    f2_ax1.plot(list_plot_ar,'o-')
else: # Courbe temps long
    f2_ax1.plot(list_plot_ar)

# Remplissage plot feux
f2_ax2 = fig2.add_subplot(spec2[1, 0])
f2_ax2.set_title('Nombre de feux')
if len(list_plot_af)<100: # Courbe temps court
    f2_ax2.plot(list_plot_af,'ro-')
else: # Courbe temps long
    f2_ax2.plot(list_plot_af,'r')

# Affichage plots
plt.xlabel('Temps passé')
plt.ylabel('Nombre arbres')
plt.show()