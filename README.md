# GraphTheoriesAfin d'utiliser le programme assurez vous d'avoir ces bibliothèques :

    - json (Pour la lecture de fichier)
    - numpy (Pour les manipulation sur les matrices, format retourné par networkx)
    - networkx 
    - matplotlib.pyplot (Pour l'affichage du graphe, fonction prise depuis la documentation networkx)
    - argparse (pour "parser" les arguments du programme)

Le projet fonctionne sous la version 3.9.7 de Python. (et devrait fonctionner pour les autre versions de Python3...)

Afin de lancer le programme, il faut lancer cette commande :

        Python3 main.py -f [FICHIER].json [-p] [-d] [--show]

où [FICHIER] est le nom du fichier. [-p], [-d] et [--show] permettent, respectivement, d'avoir une autre distribution uniforme des probabilités, de lancer le mode de debogage et d'afficher le graphe. [-p], [-d] et [--show] sont des paramètres optionnels.

Si vous ne savez pas comment lancer le fichier, vous pouvez utiliser le programme de la sorte :

        Python3 main.py -h

cela vous retournera l'aide.

Afin de créer un graphe, il suffit de lancer la commande :

        Python3 generator.py 

le programme attendra une entrée utilisateur qui sera le nombre de sommets voulus. Le graphe fournit un fichier qui porte le nom : graphe.json

Des fichiers de tests fonctionnels sont présent dans le dossiers "fichiers".

Resultats de chaque fichiers :
    - cas1Sommet.json
        Ce fichier ne fera pas lancer le programme parce qu'il n'y a aucun intérêt de traverser un graphe dans lequel il n'y a pas d'arcs.

    - casNonConnexe.json
        Ce fichier ne fera pas lancer le programme parce que le graphe n'est pas connexe.
    
    - graphe10sommets.json
        Ce fichier fera fonctionner le graphe, les resultats attendus dépendront des entrées utilisateurs.
        Pour la probabilité de trouver un chemin de longueur exactement N (avec N = 10) et le numéro de noeuds (v = 5) : 0.010865441600677761
        Pour la probabilité de trouver un chemin de longueur au plus N (avec N = 10) et le numéro de noeuds (v = 5) : 0.0704339965204932
        Nous ne pouvons pas fournir plus d'informations sur ce que l'agent qui traverse le graphe pourrait fournir parce que chaque lancement de programme donne un résultat différent.

    => [OBSERVATION] Lorsque l'option [-p] est lancé, l'effectif total est toujours plus petit que lorsque l'option n'est pas lancée.

[ATTENTION] Prévoyez quelques temps au lancement du programme. Pour de grand graphes, le programme pourrait prendre plus de temps puisque l'agent parcourt tout le graphe. 
Cependant, pour les petits graphes les resutlats sont quasi-instantanés
