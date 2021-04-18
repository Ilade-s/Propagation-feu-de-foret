from random import shuffle, randint # Pour mélange aléatoire de la grille
from time import perf_counter,sleep # Commandes pauses + chronomètre performance
import matplotlib.pyplot as plt # Commandes plots
import matplotlib.gridspec as gridspec # Commandes multiplot
from termcolor import colored # Commandes pour couleur texte
from tkinter import * # GUI
import os # Pour effacer la console (affichage)
import tkinter.messagebox as msgbox # FoC (message d'info)
from functools import partial # tkinter appel de fonctions avec paramètres

def SupprCnsl():
    """
    Vide la console
    """
    if os.name == "nt":
        os.system('cls')
    elif os.name == "posix":
        os.system('clear')

def MatPrint(mat):
    """
    Affiche, en couleur, la grille/matrice, en console

    PARAMETRES :
        - mat : list[list[int]]
            matrice à afficher
    
    SORTIE : 
        - affichage de la matrice :
        - Couleurs :
            - 0 : bleu
            - 1 : vert
            - 2 : jaune
            - 3 : rouge
            - 4/autres valeurs : print simple (blanc)

    """
    for l in mat:
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
            elif c>=4 or c<0: # Cendres?
                print(c,end=' ') 
        print(' ')

def Proba(n):
    """Permet d'ajouter des condition de probabilité :
        - n : Nombre enntre 1 et 100 : %age de chance
        - sortie : True ou False
    """
    tirage = randint(1,100)
    if tirage<=n: return(True)
    else: return(False)

class Statistiques(object): # Class decorator
    """
    Class decorator de la fonction Passe, qui est une méthode de Simulation (Sim)
    """
    def __init__(self, arg): # Initialisation attributs (pour __call__)
        self._arg = arg
        self.tp = 0
        self._mem_ar = []
        self._mem_fr = []

    def __call__(self): # Pour décorer Passe
        retval = self._arg(Sim)
        self.tp += 1
        self._mem_fr.append(retval[0])
        self._mem_ar.append(retval[1])
        return retval
    
    def Affichage(self): # Plot Affichage final
        """
        Crée le plot (matplotlib), qui pourra ensuite être affiché par plt.show()
        """
        self.nl = Sim.nl
        self.nc = Sim.nc
        self.ta = Sim.ta
        # Création multi plots
        fig2 = plt.figure(constrained_layout=True)
        spec2 = gridspec.GridSpec(ncols=1, nrows=2, figure=fig2)
        # Remplissage plot arbres restants
        f2_ax1 = fig2.add_subplot(spec2[0, 0])
        f2_ax1.set_title('Nombre d\'arbres')
        if len(self._mem_ar)<100: # Courbe temps court
            f2_ax1.plot(self._mem_ar,'o-')
        else: # Courbe temps long
            f2_ax1.plot(self._mem_ar)
        # Remplissage plot feux
        f2_ax2 = fig2.add_subplot(spec2[1, 0])
        f2_ax2.set_title('Nombre de feux')
        if len(self._mem_fr)<100: # Courbe temps court
            f2_ax2.plot(self._mem_fr,'ro-')
        else: # Courbe temps long
            f2_ax2.plot(self._mem_fr,'r')
        # Affichage plots
        plt.suptitle('Configuration : '+str(self.nl)+'*'+str(self.nc)+" // Taux d'arbres : "+str(self.ta))
        plt.title("Arbres en feu initiaux : "+str(Sim.nfi))
        plt.xlabel('Temps passé')
        plt.ylabel('Nombre arbres')

class Creation:
    """
    SuperClass de Simulation, récupère les valeurs nécessaires puis crée la grille (self.grid)

    FONCTIONS :
        - GetValues
            - Récupère les valeurs nécessaires
            - Utilisation de fenêtres tkinter
        - GenGrid 
            - Génére la grille/forêt de simulation
            - Utilise les données récupérées par GetValues"""
    
    def __init__(self, PersMat):
        if PersMat==None:
            self.GetValues(PersMat)
            self.GenTime = self.GenGrid()
            print("Temps de génération :",self.GenTime,"s")
        else:
            self.grid = PersMat
            self.narbres = sum([il.count(1) for il in self.grid])
            self.nfi = sum([il.count(2)+il.count(3) for il in self.grid])
            self.GetValues(PersMat)
            
    def GetValues(self, PersMat):
        root = Tk()
        root.title("Mode d'affichage")
        Label(root, text='Ce programme permet de simuler un feu de forêt').pack(padx=10, pady=10)
        Label(root, text="Veuillez choisir le mode d'affichage").pack(padx=5,pady=5)
        value = IntVar() 

        Statecnsltk = "normal"
        Stateinst = "normal"
        value.set(0)
        if PersMat!=None:
            Label(root, text="Matrice prédéterminée/personnalisée").pack()
            if len(PersMat)>40 or len(PersMat[0])>40:
                Statecnsltk = "disabled"
                Stateinst = "normal"
                value.set(2)
        else:
            Label(root, text="Matrice aléatoire").pack()


        Radiobutton(root, text="Affichage en console (petites simulations uniquement)", variable=value, value=1, state=Statecnsltk).pack()
        Radiobutton(root, text="Affichage tkinter", variable=value, value=0, state=Statecnsltk).pack()
        Radiobutton(root, text="Pas d'affichage (graphes instantanés)", variable=value, value=2, state=Stateinst).pack()
        Button(root, text="Confirmer (ferme la fenêtre)", command=root.destroy).pack(anchor=CENTER,pady=10,padx=10)
        root.mainloop()
        self.TypeAffichage = value.get()
        if self.TypeAffichage==1 or self.TypeAffichage==0: # Console et Tkinter
            maxTo = 40
            Res = 1
        elif self.TypeAffichage==2: # Rien
            maxTo = 1000
            Res = 1
        else: return(-1)
        root = Tk()
        root.title("Configuration simulation")
        varL = IntVar()
        varC = IntVar()
        varTa = DoubleVar()
        varNfi = StringVar()
        varProb = IntVar()
        varFoC = BooleanVar()
        varProb.set(100)
        varTa.set(1)
        varNfi.set(1)
        varTp = StringVar()
        varTp.set("1")
        varFoC.set(False)

        if PersMat!=None:
            State = "disabled"
            StateArbre = "disabled"
            varL.set(len(PersMat))
            varC.set(len(PersMat[0]))
            Label(root, text="Matrice prédéterminée/personnalisée").pack()
            varTa.set(round(self.narbres/(len(PersMat)*len(PersMat[0])),2))
            varNfi.set(self.nfi)
        else:
            State = "normal"
            Label(root, text="Matrice aléatoire").pack()

        Scale(root, variable=varL,orient=HORIZONTAL,from_=1,to=maxTo,label="Nombre de lignes :",length=200, resolution=Res, state=State).pack()
        Scale(root, variable=varC,orient=HORIZONTAL,from_=1,to=maxTo,label="Nombre de colonnes :",length=200, resolution=Res, state=State).pack()
        Scale(root, variable=varTa,orient=HORIZONTAL,from_=0,to=1,resolution=0.01,label="Taux d'arbres :",length=200, state=State).pack()
        Scale(root, variable=varProb,orient=HORIZONTAL,from_=1,to=100,label="Probabilité mise à feu (%) :",length=200).pack()
        TxtArbre = Label(root, text="Nombre d'arbres en feu :", anchor=CENTER, width=50, state=State)
        TxtArbre.pack()
        EntryArbre = Entry(root, textvariable=varNfi, state=State)
        EntryArbre.pack()
        if self.TypeAffichage==0 or self.TypeAffichage==1:
            Label(root, text="Temps entre chaque étape (affichage)",anchor=CENTER,width=50).pack()
            Entry(root, textvariable=varTp).pack()
            if self.TypeAffichage==0 and PersMat==None: # tkinter (Fire on click)
                def isChecked(): # Action quand bouton coché ou décoché
                    if varFoC.get(): # Feu par clic
                        varNfi.set("0")
                        TxtArbre.configure(state="disabled")
                        EntryArbre.configure(state="disabled")
                    else:
                        varNfi.set("1")
                        TxtArbre.configure(state="normal")
                        EntryArbre.configure(state="normal")
                Label(root, text="Si coché, désactive le choix du nombre d'arbres en feu").pack()
                Checkbutton(root, text="Choix des cases en feu par clic", variable=varFoC, onvalue=True, offvalue=False, command=isChecked).pack()
                
        Button(root, text="Confirmer les valeurs (ferme la fenêtre)", command=root.destroy).pack(anchor=CENTER,pady=10,padx=10)
        root.mainloop()
        self.FoC = varFoC.get()
        self.nl = varL.get()
        self.nc = varC.get()
        self.ta = varTa.get()
        self.nfi = int(varNfi.get())
        self.tp = float(varTp.get())
        self.ProbFeu = varProb.get()
              
    def GenGrid(self):
        nC = self.nl*self.nc
        self.narbres = int(self.ta*nC)
        start = perf_counter()
        g = [2 for i in range(int(self.nfi))]+\
            [1 for j in range(int(self.narbres-self.nfi))]+\
            [0 for ii in range(int(nC-self.narbres))]
        shuffle(g) # Mélange aléatoire liste
        self.grid = [g[i*self.nc:(i+1)*self.nc] for i in range(self.nl)]
        end = perf_counter()
        execution_time = round(end - start,5)

        return execution_time
        
class Simulation(Creation):
    """
    Classe gérant la simulation 

    Subclass de Creation, qui prépare la simulation : hérite des tous les attributs (self.grid notamment)
    """
    def __init__(self, PersMat=None):
        """
        Initialise la simulation
         
        PARAMETRE :
            - PersMat : None || list[list[int]]
                - optionnel, si None, sera ignoré (génération aléatoire)
                - Sinon, est une matrice de taille régulière, en 2D
                - les valeurs doivent être des integers entre 0 et 3 inclus
                - default = None
                - doit avoir une taille inférieure ou égale à 1000, dans les deux dimensions
        """
        if PersMat!=None:
            for i in PersMat:
                for j in i:
                    assert j==0 or j==1 or j==2 or j==3, "matrice invalide"
            assert len(PersMat)<=1000 and len(PersMat[0])<=1000, "matrice trop importante (+1000 lignes ou colonnes)"
        super().__init__(PersMat)

    @Statistiques # Mémoire pour statisitiques
    def Passe(self):
        """
        Exécute une passe de propagation du feu

        PARAMETRES :
            - Aucun
        
        SORTIE :
            - tuple : (int, int)
                - [0] : nfr : nombre de feux restants (2)
                - [1] : nar : nombre d'arbres restants (1)
        """
        for l in range(len(self.grid)): # Boucle pour étude de tous les éléments de la grille (ligne)
            for c in range(len(self.grid[0])): # Boucle pour étude de tous les éléments de la grille (colonne)
                if self.grid [l] [c]==2 or self.grid [l] [c]==3: # Détection états case + mise à feu cases adjacentes (si applicable)
                    if l!=0:
                        if self.grid [l-1] [c]==1 and Proba(self.ProbFeu): # Voisin haut
                            self.grid [l-1] [c] = 5
                    if l!=self.nl-1:
                        if self.grid [l+1] [c]==1 and Proba(self.ProbFeu): # Voisin bas
                            self.grid [l+1] [c] = 5
                    if c!=self.nc-1:
                        if self.grid [l] [c+1]==1 and Proba(self.ProbFeu): # Voisin droite
                            self.grid [l] [c+1] = 5
                    if c!=0:
                        if self.grid [l] [c-1]==1 and Proba(self.ProbFeu): # Voisin gauche
                            self.grid [l] [c-1] = 5 
                    if self.grid [l] [c]==3:
                        self.grid [l] [c] = 4 # Changement d'état de l'arbre de feu à brulé (état inerte)
                    else:
                        self.grid [l] [c] = 3
        for il in self.grid: # Boucle pour remplacement nouveaux feux en feux normaux (Correction bug)
            il[:] = [2 if x==5 else x for x in il]
            il[:] = [3 if x==6 else x for x in il] 
        # Enregristrement résultat de la passe
        nar = sum([il.count(1) for il in self.grid])
        nfr = sum([il.count(2)+il.count(3) for il in self.grid])
        # Retour valeurs pour mémoire (Statistiques)
        return (nfr, nar)

    


if __name__=='__main__': # Test
    print("=========================================")
    print("Bienvenue dans ma simulation de feu de forêt !")
    print("Vous pouvez exécuter une simulation aléatoire ou prédéterminée :")
    print("\t- 1 : Simulation à matrice aléatoire")
    print("\t- 2 : Simulation à matrice prédéterminée")
    print("=========================================")

    Choix = input("Choix : ")
    
    if Choix=="1":
        Sim = Simulation()
    elif Choix=="2":
        mat = [[1,1,1],[1,2,2],[1,1,1]]
        Sim = Simulation(mat)
    else:
        exit()

    if Sim.TypeAffichage == 1: # Affichage console
        # Affichage initial
        MatPrint(Sim.grid)
        print("Forêt initiale :")
        print("Arbres restants :",Sim.narbres)
        print("Arbres en feu :",Sim.nfi)

        sleep(2) # pause

        # première passe
        Sim.Passe()
        MatPrint(Sim.grid)
        print("Arbres restants :",Sim.Passe._mem_ar[-1])
        print("Arbres en feu :",Sim.Passe._mem_fr[-1])
        print("Temps passé :",Sim.Passe.tp)
        sleep(Sim.tp) # pause

        while Sim.Passe._mem_fr[-1]>0: # Boucle des passes 
            Sim.Passe()
            SupprCnsl()
            MatPrint(Sim.grid)
            print("Arbres restants :",Sim.Passe._mem_ar[-1],"//",round((Sim.Passe._mem_ar[-1]+Sim.Passe._mem_fr[-1])/Sim.narbres*100,3),'%')
            print("Arbres en feu :",Sim.Passe._mem_fr[-1])
            print("Temps passé :",Sim.Passe.tp)
            sleep(Sim.tp) # pause

    elif Sim.TypeAffichage == 2: # Sans affichage
        Sim.Passe() # première passe
        while Sim.Passe._mem_fr[-1]>0: # Boucle des passes 
            Sim.Passe()

    elif Sim.TypeAffichage == 0: # Affichage tkinter
        def update(): # Rafraichisssement fenêtre
            Sim.Passe()
            SupprCnsl()
            print("Arbres restants :",Sim.Passe._mem_ar[-1],"//",round((Sim.Passe._mem_ar[-1]+Sim.Passe._mem_fr[-1])/Sim.narbres*100,3),'%')
            print("Arbres en feu :",Sim.Passe._mem_fr[-1])
            print("Temps passé :",Sim.Passe.tp)
            for i in range(Sim.nl):
                for j in range(Sim.nc):
                    cells[i][j].configure(bg=couleurs[Sim.grid[i][j]])
            if Sim.Passe._mem_fr[-1]>0: # Boucle passes    
                root.after(int(Sim.tp*1000),update)
            else:
                root.destroy()

        couleurs = {0:"blue",1:"green",2:"orange",3:"red",4:"black"}

        if Sim.FoC: # Premier affichage de choix des cases en feu (si demandé)
            def OnClick(i,j):
                Sim.grid[i][j] = 2
                # Rafraichissement
                cells[i][j].configure(bg=couleurs[Sim.grid[i][j]])
                if msgbox.askyesno("Confirmation","Avez-vous terminé votre sélection ?"): 
                    root.destroy()

            cells = [[0 for c in range(Sim.nc)] for l in range(Sim.nl)]
            root = Tk()
            msgbox.showinfo("Fire on click : information", 
            "Pour choisir les cases à mettre en feu, vous devrez cliquer sur chaque case souhaitée, et confirmer quand vous aurez fini (pas avant !)")
            root.title('Choix cases en feu (FoC)')
            root.resizable(False, False)
            root.geometry("600x600")
            for i in range(Sim.nl):
                root.rowconfigure(i,weight=1)
            for j in range(Sim.nc):
                root.columnconfigure(j,weight=1)
            for i in range(Sim.nl):
                for j in range(Sim.nc):
                    w = Button(root,borderwidth=1,relief=SOLID,bg=couleurs[Sim.grid[i][j]], command=partial(OnClick, i, j))
                    cells[i][j] = w
                    cells[i][j].grid(row=i,column=j\
                        ,ipadx=600/Sim.nc\
                        ,ipady=600/Sim.nl)
            root.mainloop()
            Sim.nfi = sum([il.count(2) for il in Sim.grid])

        # Affichage normal
        cells = [[0 for c in range(Sim.nc)] for l in range(Sim.nl)]
        root = Tk()
        root.title('Forêt')
        root.resizable(False, False)
        root.geometry("600x600")
        for i in range(Sim.nl):
            root.rowconfigure(i,weight=1)
        for j in range(Sim.nc):
            root.columnconfigure(j,weight=1)
        for i in range(Sim.nl):
            for j in range(Sim.nc):
                w = Label(root,borderwidth=1,relief=SOLID,bg=couleurs[Sim.grid[i][j]])
                cells[i][j] = w
                cells[i][j].grid(row=i,column=j\
                    ,ipadx=600/Sim.nc\
                    ,ipady=600/Sim.nl)
        root.after(int(Sim.tp*1000),update)
        root.mainloop()

    Sim.Passe.Affichage() # Création plot
    plt.show() # Affichage plot