from file import main
import sys, os, argparse #Pour les options en ligne de commande
import utils #Pour avoir la variable global debug.


parser = argparse.ArgumentParser(description="Fait des statistiques à partir d'un graphe lu d'un fichier")
parser.add_argument('-f', '--file',
                    nargs=1, 
                    metavar='FILE',
                    type=str,
                    required=True,
                    help='Un fichier de format JSON à lire')

parser.add_argument('-d', '--debug',
                    action='store_true',
                    help='Active le mode débug')

parser.add_argument('-p',
                    action='store_true',
                    help='Utilise une distribution non-uniforme des probabilités des chemins')

parser.add_argument('--show',
                    action='store_true',
                    help='Affichage du graphe')

args = parser.parse_args()

inputPath = args.file #Produit une liste contenant les arguments entrés
inputDebug = args.debug
inputP = args.p
inputShow = args.show


#Pour mettre la variable globale debug en True
if inputDebug == True:
    utils.debugOn()

#Pour mettre la variable p (comme probabilité) en True
if inputP == True:
    utils.pOn()

#Pour mettre la variable show (pour l'affichage du graphe) en True
if inputShow == True:
    utils.showOn()

#On verifie si les arguments en entrée ne sont pas vide
if inputPath is not None:
    #On vérifie si le dossier/fichier existe
    if os.path.isfile(inputPath[0]):
        #On verifie l'extention du fichier
        if os.path.splitext(inputPath[0])[1] != ".json":
            print("L'extention du fichier n'est pas correct, format .json attendu ")
            sys.exit()
        else: 
           main(inputPath[0]) #On lance le programme.    
    else:
        print("Le fichier entré n'existe pas. ")
        sys.exit()
