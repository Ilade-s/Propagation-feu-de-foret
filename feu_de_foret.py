from random import shuffle # Pour mélange aléatoire de la grille
from time import perf_counter,sleep # Commandes pauses + chronomètre performance
import matplotlib.pyplot as plt # Commandes plots
import matplotlib.gridspec as gridspec # Commandes multiplot
from termcolor import colored # Commandes pour couleur texte
from tkinter import * # GUI

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

class Creation:

    def __init__(self, name="Creation") -> None:
        self.SuperClass = name
        self.GetValues()
        #self.GenGrid()
        print("Temps de génération :",self.GenGrid())

    
    def GetValues(self):
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
        varNfi.set(1)
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
            varTp.set(1)
            labelEntryTp = Label(root, text="Temps entre chaque étape (affichage)",anchor=CENTER,width=50)
            entryTp = Entry(root, textvariable=varTp)
            labelEntryTp.pack()
            entryTp.pack()
            ExitButton = Button(root, text="Confirmer (ferme la fenêtre)", command=root.destroy)
            ExitButton.pack(anchor=CENTER,pady=10,padx=10)
            root.mainloop()
            self.tp = float(varTp.get())
        
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
        execution_time = round(end - start,3)

        return execution_time

    def __init_subclass__(cls, **kwargs) -> None:
        print("Original class name :",cls.name)
        cls.name = "Subclass"
        
class Simulation(Creation, name="Simulation"):
    name = "Simulation"

    


if __name__=='__main__': # Test
    Sim = Simulation()
    print("Class name :",Sim.name)
    print("Original Class name :",Sim.SuperClass)
    print("Nombre de colonnes :",Sim.nc)

    MatPrint(Sim.grid)