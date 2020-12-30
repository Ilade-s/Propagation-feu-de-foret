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
def creerGrille(narbres, nfi, nC): # Boucle pour création grille initiale + retour graphique
    print('\tCréation cases...')
    grid = [2 for i in range(int(nfi))]+[1 for j in range(int(narbres-nfi))]+[0 for ii in range(int(nC-narbres))]
    print('\t\t\tTerminé !')
    print('\tMélange...')
    shuffle(grid) # Mélange aléatoire liste
    print('\t\t\tTerminé !')
    return(grid)
def affichage(grid,nl,nc,tinput,t,tp): # Séparation grille pour affichage
    if tinput==2: # Affichage grille en couleur
        #FF0000 = rouge 3
        #000000 = noir 4
        #00BE00 = vert 1
        #9A4A00 = marron 0
        #FFBF00 = orange 2
        cmap = clr.ListedColormap(['#9A4A00','#00BE00','#FFBF00','#FF0000','#000000'])
        Boundaries = [-0.1,0.9,1.9,2.9,3.9,4.9]
        Z = grid
        norm = clr.BoundaryNorm(Boundaries, ncolors=5)
        fig, ax = plt.subplots()
        ax.pcolormesh(Z,cmap=cmap,norm=norm)
        # Ajout texte plot
        plt.suptitle('Forêt (Temps passé : '+str(t)+') : ')
        plt.title('Configuration : '+str(nl)+'*'+str(nc)+' // Taux d\'arbres : '+str(ta))
        plt.xlabel('Colonnes')
        plt.ylabel('Lignes')
        plt.pause(tp)
        plt.close()
    else: # Affichage grille en console
        for l in grid:
            print('[',end=' ')
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
            print(']')
def prop_feu(grid): # Boucle tests réactions entre les cases
    for l in range(nl): # Boucle pour étude de tous les éléments de la grille (ligne)
        for c in range(nc): # Boucle pour étude de tous les éléments de la grille (colonne)
            if grid [l] [c]==2 or grid [l] [c]==3: # Détection états case + mise à feu cases adjacentes (si applicable)
                if l==0: # Coté vertical haut
                    if c==0: # Coin en haut à gauche (2 voisins constants)
                        if grid [0] [1]==1: # Voisin droite 1
                            grid [0] [1] = 5
                        if grid [1] [0]==1: # Voisin bas 1
                            grid [1] [0] = 5                   
                    elif c==nc-1:  # Coin en haut à droite (2 voisins constants)
                        if grid [0] [c-1]==1: # Voisin gauche 1
                            grid [0] [c-1] = 5
                        if grid [1] [c]==1: # Voisin bas 1
                            grid [1] [c] = 5
                    else: # autres cases sauf coins (3 voisins)
                        if grid [0] [c-1]==1: # Voisin gauche
                            grid [0] [c-1] = 5
                        if grid [0] [c+1]==1: # Voisin droite
                            grid [0] [c+1] = 5
                        if grid [1] [c]==1: # Voisin bas
                            grid [1] [c] = 5
                elif l==nl-1:  # Coté vertical bas
                    if c==0: # Coin en bas à gauche (2 voisins constants)
                        if grid [l] [1]==1: # Voisin droite
                            grid [l] [1] = 5
                        if grid [l-1] [0]==1: # Voisin haut
                            grid [l-1] [0] = 5
                    elif c==nc-1:  # Coin en bas à droite (2 voisins constants)
                        if grid [l] [c-1]==1: # Voisin gauche
                            grid [l] [c-1] = 5
                        if grid [l-1] [c]==1: # Voisin haut
                            grid [l-1] [c] = 5
                    else: # autres cases sauf coins (3 voisins)
                        if grid [l] [c-1]==1: # Voisin gauche
                            grid [l] [c-1] = 5
                        if grid [l-1] [c]==1: # Voisin haut
                            grid [l-1] [c] = 5
                        if grid [l] [c+1]==1: # Voisin droite
                            grid [l] [c+1] = 5
                else: # Autres lignes non cotés
                    if c==0: # Coté latéral gauche sauf coins (3 voisins)
                        if grid [l-1] [0]==1: # Voisin haut
                            grid [l-1] [0] = 5
                        if grid [l+1] [0]==1: # Voisin bas
                            grid [l+1] [0] = 5
                        if grid [l] [1]==1: # Voisin droite
                            grid [l] [1] = 5
                    elif c==nc-1:  # Coin latéral droit sauf coins (3 voisins)
                        if grid [l-1] [c]==1: # Voisin haut
                            grid [l-1] [c] = 5
                        if grid [l+1] [c]==1: # Voisin bas
                            grid [l+1] [c] = 5
                        if grid [l] [c-1]==1: # Voisin gauche
                            grid [l] [c-1] = 5
                    else: # autres cases (4 voisins)
                        if grid [l-1] [c]==1: # Voisin haut
                            grid [l-1] [c] = 5
                        if grid [l+1] [c]==1: # Voisin bas
                            grid [l+1] [c] = 5
                        if grid [l] [c+1]==1: # Voisin droite
                            grid [l] [c+1] = 5
                        if grid [l] [c-1]==1: # Voisin gauche
                            grid [l] [c-1] = 5
                if grid [l] [c]==3:
                    grid [l] [c] = 4 # Changement d'état de l'arbre de feu à brulé (état inerte)
                else:
                    grid [l] [c] = 3
    for il in grid: # Boucle pour remplacement nouveaux feux en feux normaux (Correction bug)
        il[:] = [2 if x==5 else x for x in il]
        il[:] = [3 if x==6 else x for x in il]  
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
na = round(ta*nC,0)
print('Création forêt aléatoire...')
start = perf_counter()
g = creerGrille(na, nfi, nC) # Création de la grille
end = perf_counter()
execution_time = round(end - start,3)
print('\tTemps d\'exécution : '+str(execution_time)+' secondes')
grid = []
for i in range(nl):
    grid.append(g[i*nc:(i+1)*nc])
tinput = int(input('Pause entre chaque étape (affichage console) : retourner 0 ; Pause de 1s entre chaque étape (affichage plot) : retourner 2 ; ou résultat "instantané" : retourner 1 : '))
# Fin interface utilisateur
t=0
tp=0
if tinput==0 or tinput==2: # Affichage forêt initiale si demandé
    tp = round(float(input('\tCombien de temps entre entre chaque étape ? : ')),2)
    print('Forêt de départ : ')
    print('Nombre d\'arbres au départ : '+str(na))
    print('Temps passé : '+str(t))
    affichage(grid,nl,nc,tinput,t,tp)
    if tinput==0:
        sleep(tp)
nar=na
nfr=nfi
list_plot_ar = []
list_plot_af = []
if tinput==1:
    print('Simulation en cours...')
start = perf_counter()
while nfr!=0: # Boucle états de la forêt 
    t+=1
    igrid = prop_feu(grid)
    nar=0
    nfr=0
    for il in igrid:
        nar += il.count(1)
        nfr += il.count(2)+il.count(3)
    if tinput==0: # Affichage console
        for s in range(nl+3): # Suppression grille précédente
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
        affichage(igrid,nl,nc,tinput,t,tp)
        print('Arbres restants : '+str(nar+nfr)+' // '+str(round(((nar+nfr)/na)*100,3))+'%')
        print('Arbres en feu : '+str(nfr))
        print('Temps passé : '+str(t))
    elif tinput==2: # Affichage plot
        for s in range(3): # Suppression grille précédente
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
        print('Arbres restants : '+str(nar+nfr)+' // '+str(round(((nar+nfr)/na)*100,3))+'%')
        print('Arbres en feu : '+str(nfr))
        print('Temps passé : '+str(t))
        affichage(igrid,nl,nc,tinput,t,tp)
    list_plot_ar.append(nar+nfr)
    list_plot_af.append(nfr)
    sleep(tp)
if nfr!=0: # Correction dernier arbre en feu 
    t+=1
    igrid = prop_feu(grid)
    nar=0
    nfr=0
    for il in igrid:
        nar += il.count(1)
        nfr += il.count(2)+il.count(3)
    if tinput==0: # Affichage console
        for s in range(nl+3): # Suppression grille précédente
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
        affichage(igrid,nl,nc,tinput,t,tp)
    elif tinput==2: # Affichage plot
        for s in range(3): # Suppression grille précédente
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
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
plt.close() # Fermeture dernier plot grille (si appliquable)
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
plt.suptitle('Configuration : '+str(nl)+'*'+str(nc)+' // Taux d\'arbres : '+str(ta))
plt.xlabel('Temps passé')
plt.ylabel('Nombre arbres')
plt.show()