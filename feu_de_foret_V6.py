from random import shuffle # Pour mélange aléatoire de la grille
from time import perf_counter,sleep # Commandes pauses + chronomètre performance
import matplotlib.pyplot as plt # Commandes plots
import matplotlib.gridspec as gridspec # Commandes multiplot
from termcolor import colored # Commandes pour couleur texte
from ToolsPerso import Tools # Outils personnels
from tkinter import * # GUI
import ctypes # Pour lancement dans console IDLE python (support suppression de texte)
kernel32 = ctypes.windll.kernel32 # IDLE
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7) # IDLE
class FeuDeForet: # Objet grid feu
    def __init__(self) -> None: # Initialisation données
        self.grid = []
        self.GetValues()
        self.GenGrid()
        self.t = 0
    def GetValues(self) -> None: # Récupération des valeurs pas GUI tkinter
        """Récupère les valeurs nécessaires pour la simulation"""
        root = Tk()
        root.title("Mode d'affichage")
        label = Label(root, text='Ce programme permet de simuler un feu de forêt')
        label2 = Label(root, text="Veuillez choisir le mode d'affichage")
        label.pack(padx=10, pady=10)
        label2.pack(padx=5,pady=5)
        value = IntVar() 
        bouton1 = Radiobutton(root, text="Affichage en console (petites simulations uniquement)", variable=value, value=1)
        bouton2 = Radiobutton(root, text="Affichage tkinter", variable=value, value=0)
        bouton3 = Radiobutton(root, text="Pas d'affichage (graphes instantanés)", variable=value, value=2)
        bouton1.pack()
        bouton2.pack()
        bouton3.pack()
        ExitButton = Button(root, text="Confirmer (ferme la fenêtre)", command=root.destroy)
        ExitButton.pack(anchor=CENTER,pady=10,padx=10)
        root.mainloop()
        self.TypeAffichage = value.get()
        if self.TypeAffichage==1 or self.TypeAffichage==0: # Console et Tkinter
            maxTo = 40
            Res = 1
        elif self.TypeAffichage==2: # Rien
            maxTo = 1000
            Res = 50
        else: return(-1)
        root = Tk()
        root.title("Configuration simulation : forme et taux")
        varL = IntVar()
        varC = IntVar()
        varTa = DoubleVar()
        varNfi = StringVar()
        varProb = IntVar()
        varProb.set(100)
        varTa.set(1)
        varNfi.set("Entrer...")
        scale1 = Scale(root, variable=varL,orient=HORIZONTAL,from_=1,to=maxTo,label="Nombre de lignes :",length=200,resolution=Res)
        scale2 = Scale(root, variable=varC,orient=HORIZONTAL,from_=1,to=maxTo,label="Nombre de colonnes :",length=200,resolution=Res)
        scale3 = Scale(root, variable=varTa,orient=HORIZONTAL,from_=0,to=1,resolution=0.01,label="Taux d'arbres :",length=200)
        scale4 = Scale(root, variable=varProb,orient=HORIZONTAL,from_=1,to=100,label="Probabilité mise à feu (%) :",length=200)
        labelEntry = Label(root, text="Nombre d'arbres en feu :",anchor=CENTER,width=50)
        entry = Entry(root, textvariable=varNfi)
        scale1.pack()
        scale2.pack()
        scale3.pack()
        scale4.pack()
        labelEntry.pack()
        entry.pack()
        ExitButton = Button(root, text="Confirmer les valeurs (ferme la fenêtre)", command=root.destroy)
        ExitButton.pack(anchor=CENTER,pady=10,padx=10)
        root.mainloop()
        self.nc = varL.get()
        self.nl = varC.get()
        self.ta = varTa.get()
        self.nfi = int(varNfi.get())
        self.ProbFeu = varProb.get()
        if self.TypeAffichage!=2:
            root = Tk()
            root.title("Configuration simulation : temps")
            labelWarning = Label(root, text="La fenêtre ne peut pas être rafraichie plus vite que toutes les 0.5 secondes", anchor=CENTER)
            labelWarning.pack()
            varTp = StringVar()
            varTp.set("Entrer...")
            labelEntryTp = Label(root, text="Temps entre chaque étape (affichage)",anchor=CENTER,width=50)
            entryTp = Entry(root, textvariable=varTp)
            labelEntryTp.pack()
            entryTp.pack()
            ExitButton = Button(root, text="Confirmer (ferme la fenêtre)", command=root.destroy)
            ExitButton.pack(anchor=CENTER,pady=10,padx=10)
            root.mainloop()
            self.tp = float(varTp.get())
    def GenGrid(self) -> None: # Génération Forêt (fonction fille de __init__)
        """Génére la grille de foret et affiche le temps d'exécution dans console"""
        nC = self.nl*self.nc
        self.narbres = int(self.ta*nC)
        print('\tCréation cases...')
        start = perf_counter()
        g = [2 for i in range(int(self.nfi))]+\
            [1 for j in range(int(self.narbres-self.nfi))]+\
            [0 for ii in range(int(nC-self.narbres))]
        print('\t\t\tTerminé !')
        print('\tMélange...')
        shuffle(g) # Mélange aléatoire liste
        print('\t\t\tTerminé !')
        for i in range(self.nl):
            self.grid.append(g[i*self.nc:(i+1)*self.nc])
        end = perf_counter()
        execution_time = round(end - start,3)
        print('\tTemps d\'exécution : ',execution_time,' secondes')
    def FuncMere(self) -> None: # Fonction principale programme
        """Fonction principale, appelle le reste des fonctions"""
        # Initialisation variables pour boucle
        nar=self.narbres
        nfr=self.nfi
        self.listArbresRestants = []
        self.listFeuxRestants = []
        print('Simulation en cours...')
        start = perf_counter()
        if self.TypeAffichage!=0:
            self.affichage(True) # Setup affichage
            while nfr!=0: # Boucle êtat de la foret
                self.t+=1
                self.FuncPropFeu()
                nar = sum([il.count(1) for il in self.grid])
                nfr = sum([il.count(2)+il.count(3) for il in self.grid])
                if self.TypeAffichage!=2:
                    print('Arbres restants :',nar+nfr,'//',int((nar+nfr)/self.narbres)*100,'%')
                    print('Arbres en feu :',nfr)
                    print('Temps passé : ',self.t)
                self.affichage()
                self.listArbresRestants.append(nar+nfr)
                self.listFeuxRestants.append(nfr)
            if nfr!=0: # Passe supplémentaire (correction bug)
                self.t+=1
                self.FuncPropFeu()
                nar = sum([il.count(1) for il in self.grid])
                nfr = sum([il.count(2)+il.count(3) for il in self.grid])
                self.listArbresRestants.append(nar+nfr)
                self.listFeuxRestants.append(nfr)
        else: # Affichage tkinter (boucle tkinter gérée)
            self.affichage(True) # Setup affichage
        self.FuncFinProg(start)
    def FuncPropFeu(self) -> None: # Fonction fille de FuncMere utilisée dans la boucle
        """Exécute une passe de propagation du feu dans self.grid (la forêt)"""
        for l in range(self.nl): # Boucle pour étude de tous les éléments de la grille (ligne)
            for c in range(self.nc): # Boucle pour étude de tous les éléments de la grille (colonne)
                if self.grid [l] [c]==2 or self.grid [l] [c]==3: # Détection états case + mise à feu cases adjacentes (si applicable)
                    if l!=0:
                        if self.grid [l-1] [c]==1 and Tools.Proba(self.ProbFeu): # Voisin haut
                            self.grid [l-1] [c] = 5
                    if l!=self.nl-1:
                        if self.grid [l+1] [c]==1 and Tools.Proba(self.ProbFeu): # Voisin bas
                            self.grid [l+1] [c] = 5
                    if c!=self.nc-1:
                        if self.grid [l] [c+1]==1 and Tools.Proba(self.ProbFeu): # Voisin droite
                            self.grid [l] [c+1] = 5
                    if c!=0:
                        if self.grid [l] [c-1]==1 and Tools.Proba(self.ProbFeu): # Voisin gauche
                            self.grid [l] [c-1] = 5 
                    if self.grid [l] [c]==3:
                        self.grid [l] [c] = 4 # Changement d'état de l'arbre de feu à brulé (état inerte)
                    else:
                        self.grid [l] [c] = 3
        for il in self.grid: # Boucle pour remplacement nouveaux feux en feux normaux (Correction bug)
            il[:] = [2 if x==5 else x for x in il]
            il[:] = [3 if x==6 else x for x in il]  
    def affichage(self, setup=False) -> None: # Affichage de la foret
        """Affiche la foret en console ou en plot en fonction de self.TypeAffichage (0 : tkinter ; 1 : console ; 2 : instantané)
            - rouge (3)
            - noir (4)
            - vert (1)
            - bleu (0)
            - orange (2)"""
        if self.TypeAffichage==2: return(-1) # Vérif si affichage demandé ou non
        if setup: # Demandes et actions si il s'agit du premier affichage ou non
            print('Forêt de départ : ')
            print('Nombre d\'arbres au départ : ',self.narbres)
            print('Temps passé : ',self.t)
        else:
            if self.TypeAffichage==1:
                Tools.suppr(self.nl+4)
            elif self.TypeAffichage==0:
                Tools.suppr(3)
        # Affichage en lui même
        if self.TypeAffichage==0: # Affichage grille sur tkinter
            def updateTkinter(): # Mise à jour fenêtre
                Feu.FuncPropFeu()
                self.t+=1
                Feu.nar = sum([il.count(1) for il in Feu.grid])
                Feu.nfr = sum([il.count(2)+il.count(3) for il in Feu.grid])
                Feu.listArbresRestants.append(Feu.nar+Feu.nfr)
                Feu.listFeuxRestants.append(Feu.nfr)
                Tools.suppr(3)
                print('Arbres restants :',Feu.nar+Feu.nfr,'//',round((Feu.nar+Feu.nfr)/self.narbres*100,3),'%')
                print('Arbres en feu :',Feu.nfr)
                print('Temps passé : ',self.t)
                if Feu.nfr==0: 
                    root.destroy()
                    return(-1)
                for i in range(self.nl):
                    for j in range(self.nc):
                        Feu.cells[i][j].configure(bg=Feu.couleurs[Feu.grid[i][j]])
                root.after(int(self.tp*1000),updateTkinter)
            # Init
            self.nar=self.narbres
            self.nfr=self.nfi
            self.couleurs = {0:"blue",1:"green",2:"orange",3:"red",4:"black"}
            self.cells = [[0 for c in range(self.nc)] for l in range(self.nl)]
            root = Tk()
            root.title('Forêt')
            root.resizable(False, False)
            root.geometry("600x600")
            for i in range(self.nl):
                root.rowconfigure(i,weight=1)
            for j in range(self.nc):
                root.columnconfigure(j,weight=1)
            for i in range(self.nl):
                for j in range(self.nc):
                    w = Label(root,borderwidth=1,relief=SOLID,bg=self.couleurs[self.grid[i][j]])
                    self.cells[i][j] = w
                    self.cells[i][j].grid(row=i,column=j\
                        ,ipadx=600/self.nc\
                        ,ipady=600/self.nl)
            root.after(int(self.tp*1000),updateTkinter)
            root.mainloop()
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
    def FuncFinProg(self,start) -> None: # Fin de programme (graphes)
        # Création multi plots
        fig2 = plt.figure(constrained_layout=True)
        spec2 = gridspec.GridSpec(ncols=1, nrows=2, figure=fig2)
        # Remplissage plot arbres restants
        f2_ax1 = fig2.add_subplot(spec2[0, 0])
        f2_ax1.set_title('Nombre d\'arbres')
        if len(self.listArbresRestants)<100: # Courbe temps court
            f2_ax1.plot(self.listArbresRestants,'o-')
        else: # Courbe temps long
            f2_ax1.plot(self.listArbresRestants)
        # Remplissage plot feux
        f2_ax2 = fig2.add_subplot(spec2[1, 0])
        f2_ax2.set_title('Nombre de feux')
        if len(self.listFeuxRestants)<100: # Courbe temps court
            f2_ax2.plot(self.listFeuxRestants,'ro-')
        else: # Courbe temps long
            f2_ax2.plot(self.listFeuxRestants,'r')
        # Affichage plots
        plt.suptitle('Configuration :'+str(self.nl)+'*'+str(self.nc)+' // Taux d\'arbres : '+str(self.ta))
        plt.xlabel('Temps passé')
        plt.ylabel('Nombre arbres')
        nar = sum([il.count(1) for il in self.grid])
        nfr = sum([il.count(2)+il.count(3) for il in self.grid])
        end = perf_counter()
        execution_time = round(end - start,3)
        if self.TypeAffichage!=0:
            # Etat final de la simulation
            self.affichage()
            print('\tTerminé !', end=' ')
            print('\tTemps d\'exécution : '+str(execution_time)+' secondes')
            print('Arbres restants : '+str(nar+nfr)+' // '+str(round(((nar+nfr)/self.narbres)*100,3))+'%')
            print('Temps passé : '+str(self.t))
            plt.show()
        else:
            plt.ion()
            plt.show()
            root = Tk()
            root.title("Etat final simulation")
            label = Label(root,text="Terminé !",anchor=CENTER)
            labelTe = Label(root,text='\tTemps d\'exécution : '+str(execution_time)+' secondes')
            labelAr = Label(root, text="Arbres en feu : "+str(nfr))
            labelTp = Label(root, text='Arbres restants : '+str(nar+nfr)+' // '+str(round(((nar+nfr)/self.narbres)*100,3))+'%')
            label.pack()
            labelTe.pack()
            labelAr.pack()
            labelTp.pack()
            ExitButton = Button(root, text="Confirmer (ferme la fenêtre)", command=exit)
            ExitButton.pack(anchor=CENTER,pady=10,padx=10)
            root.mainloop()
Feu = FeuDeForet()
Feu.FuncMere()
