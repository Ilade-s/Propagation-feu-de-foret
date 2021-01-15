# Propagation d'un feu dans une forêt
Simulation de la propagation d'un feu dans une forêt 
Plusieurs versions sont disponibles, avec à l'heure actuelle la version 6 qui est la plus rapide et claire dans son écriture (GUI)
Les régles de la simulation sont :
  - Un taux d'arbres ainsi qu'une taille donné par l'utilisateur
  - Un arbre en feu depuis deux passes de la boucle de la simulation devient brulé et ne propage plus le feu
  - Un arbre en feu peut enflammer uniquement les 4 cases directement adjacentes à lui
  - la simulation s'arrête lorsque qu'il n'y a plus d'arbres en feu (simulation bloquée)
  - modules utilisés : tkinter, termcolor (à installer), matplotlib (à installer)
 
 ATTENTION : Pour la version 6, ToolsPerso.py doit être présent dans le même dossier pour fonctionner
_____________________________________________________________________
Simulation of the propagation of a fire in a forest. Several versions are available, with currently version 6 being the fastest and clearest in its writing (GUI) The rules of the simulation are :

  - A rate of trees as well as a size given by the user.
  - A tree that has been on fire for two passes of the simulation loop becomes burnt and no longer propagates fire.
  - A burning tree can only ignite the 4 squares directly adjacent to it.
  - the simulation stops when there are no more burning trees (blocked simulation)
  - Modules used : tkinter, termcolor (installation needed), matplotlib (installation needed)

WARNING: For version 6, ToolsPerso.py must be present in the same folder in order to work.
