# Propagation d'un feu dans une forêt
Simulation de la propagation d'un feu dans une forêt 
Plusieurs versions sont disponibles, avec à l'heure actuelle la version 6 qui est la plus rapide et claire dans son écriture (GUI)
Les régles de la simulation sont :
  - Un taux d'arbres ainsi qu'une taille donné par l'utilisateur
  - Un arbre en feu depuis deux passes de la boucle de la simulation devient brulé et ne propage plus le feu
  - Un arbre en feu peut enflammer uniquement les 4 cases directement adjacentes à lui
  - la simulation s'arrête lorsque qu'il n'y a plus d'arbres en feu (simulation bloquée)
