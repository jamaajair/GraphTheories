import networkx as nx #Pour les manipulations basiques des graphes
import sys
import json #Pour lire le format json d'un graphe 
import matplotlib.pyplot as plt #Pour afficher des graphes afin d'avoir un visuel (c.f. https://networkx.org/documentation/stable/tutorial.html)
import numpy as np #Pour la matrice d'adjacence 
import utils #Pour avoir la variable global debug.
import math


def showGraph(graph):
    """Affiche le graphe dans une fenêtre

    Args:
        graph (Graph): Un graphe orienté (ou non)
    """
    layout = nx.random_layout(graph)
    nx.draw_networkx_nodes(graph, pos=layout, node_size=500, node_color='red')
    nx.draw_networkx_edges(graph, pos=layout, style='dotted', edge_color='blue')
    nx.draw_networkx_labels(graph, pos=layout)
    plt.show()

def loadGraph(name):
    """Charge le graphe à partir d'un fichier

    Args:
        name (string): le nom du fichier en entrée par l'utilisateur
    Return:
        Retourne un graphe orienté (ou non)
    """
    global MAX
    try:
        file = open(name, 'r')
        data = json.load(file)
        nodesNbr = MAX = data['NbNoeuds']
        graph = nx.DiGraph()

        graph.add_nodes_from(range(0, nodesNbr)) if nodesNbr >= 1 else graph.add_node(nodesNbr)
        nodes = []

        i = 0
        #On veut accéder à chaque noeuds
        while i < nodesNbr:
            index = data['Noeuds'][i]['id']

            z = 0
            #On crée les arcs sur chaque éléments de la liste de noeuds
            while z != len(data['Noeuds'][i]['arcs']):
                graph.add_edge(i, data['Noeuds'][i]['arcs'][z])
                prob = data['Noeuds'][i]['p'][z]
                nx.set_edge_attributes(graph, {(index, data['Noeuds'][i]['arcs'][z]): {"p" : prob}})
                z = z + 1
            
            i = i + 1

        graph.add_nodes_from(nodes)

        if utils.debug == True:
            print("Nombre de Noeuds [NbNoeuds] = %d " % (nodesNbr+1))
            print("Nombre de Noeuds [nombre d'iterations] = %d " % (i+1))
            print("Nombre de Noeuds [nombre de dict dans la liste] = %d " % (len(data['Noeuds'])))  
            print("-----")

            j = 0
            while j < nodesNbr:
                print(graph.nodes[j])
                j += 1
            
            print("-----")
            print(nx.info(graph))

        file.close()

    except FileNotFoundError:
        sys.exit("Le fichier que vous fournissez n'existe pas !! ")

    return graph

def getAdjMatrix(graph):
    """Donne la matrice d'adjacence du graphe

    Args:
        graph (Graph): Un graphe orienté (ou non)

    Returns:
        np.array: Retourne la matrice adjacente du graphe
    """
    Matrix = nx.adjacency_matrix(graph)

    if utils.debug == True:
         print(Matrix.todense())
    
    return Matrix.todense()

def isStronglyConn(graph):
    """Verifie si le graphe est fortement connexe

    Args:
        graph (DiGraph): Le graphe entré par l'utilisateur

    Returns:
        bool: Vrai si le graphe est fortement connexe, Faux sinon
    """
    if nx.strongly_connected.is_strongly_connected(graph) == False:
        return False

    return True

def mulMatrix(matrix, n):
    """Multiplie la matrice à la puissance n

    Args:
        matrix (np.array): La matrice d'adjacence du graphe
        n (int): le degré de puissance de la matrice

    Returns:
        np.array: La matrice d'adjacence puissance n
    """
    Matrix = np.linalg.matrix_power(matrix, n)

    if utils.debug == True:
        print("Matrice puissance %d " % (n))
        print(Matrix)

    return Matrix

def exactLength(matrix, v):
    """Retourne une estimation de la probabilité de revenir en v avec une longueur de chemin qui vaut exactement n

    Args:
        matrix (np.array): La matrice d'adjacence du graphe
        v (int): le sommet voulu

    Returns:
        float: la probabilité de revenir en v avec une longueur de chemin qui vaut exactement n
    """

    value = 0
    matrix = matrix = matrix.astype('float64') #Pour éviter les problèmes d'overflow

    for i in range(0, MAX):
        for j in range(0, MAX):
            value = value + matrix[i,j]

    return matrix[v,v]/value

def atMostLength(matrix, v, n):
    """Retourne une estimation de la probabilité de revenir en v avec une longueur de chemin au plus n

    Args:
        matrix (np.array): La matrice d'adjacence du graphe
        v (int): le sommet voulu

    Returns:
        float: la probabilité de revenir en v avec un chemin de longueur au plus n
    """

    value = 0
    tmp = 0
    matrix = matrix = matrix.astype('float64') #Pour éviter les problèmes d'overflow
    
    for z in range(1, n+1):
        tmpMatrix = mulMatrix(matrix, z)
        for i in range(0, MAX):
            for j in range(0, MAX):
                    tmp = tmp + tmpMatrix[i,j]

        
        value = value + (tmpMatrix[v,v]/tmp)

    return value

def smallestPath(paths):
    """Donne la longueur du plus petit chemin emprunté par l'agent

    Args:
        paths (list): La liste des chemins emprunté par l'agent

    Returns:
        int: la taille du chemin le plus petit
    """
    if paths:
        curr = 0
        min = len(paths[0][0])

        #On parcourt la liste de liste de chemins parcouru par l'agent
        for i in range(0, len(paths)):
            #On parcourt chaque liste individuellement
            for j in range(0, len(paths[i])):
                curr = len(paths[i][j])

                if (curr < min):
                    min = curr

        return min
    else:
        sys.exit("La liste de chemins est invalide")

def biggestPath(paths):
    """Donne la valeur du plus grand chemin emprunté par l'agent

    Args:
        paths (list): La liste des chemins emprunté par l'agent

    Returns:
        int: la taille du chemin
    """
    if paths:
        curr = 0
        max = len(paths[0][0])

        #On parcourt la liste de liste de chemins parcouru par l'agent
        for i in range(0, len(paths)):
            #On parcourt chaque liste individuellement
            for j in range(0, len(paths[i])):
                curr = len(paths[i][j])

                if (curr > max):
                    max = curr

        return max
    else:
        print()
        sys.exit("La liste de chemin est invalide")

def Total(occurencesPathsList):
    """Retourne l'effectif total des chemins parcourus

    Args:
        occurencesPathsList (list): La liste de chemins

    Returns:
        int: l'effectif total des chemins
    """
    if occurencesPathsList:
        occurences = occurencesPathsList.most_common()
        tot = 0
        
        #On parcours la liste contenant les occurences de chaque chemins
        for i in range(0, len(occurences)):
            tot = tot + occurences[i][1]

        return tot
    else:
        sys.exit("La liste d'effectif est invalide")

def frequencyDistribution(occurencesPathsList):
    """Retourne la distribution des fréquences des chemins

    Args:
        occurencesPathsList (liste): La liste de chemins

    Returns:
        list: Une liste de tuple ((chemin), frequence))
    """
    if occurencesPathsList:
        occurences = occurencesPathsList.most_common()
        tot = Total(occurencesPathsList)

        frequencyList = list()

        #On parcours la liste contenant les occurences de chaque chemins
        for i in range(0, len(occurences)):
            effTmp = occurences[i][1]/tot
            frequencyList.append((occurences[i][0], effTmp))

        return frequencyList
    else:
        sys.exit("La liste d'effectif est invalide.")

def stats(occurencesPathsList, freqDist):
    """Crée une liste contenant diverses informations sur les chemins : fréquences et effectifs

    Args:
        occurencesPathsList (list): La liste de chemins
        freqDist (list): Une liste de tuple ((chemin), frequence))

    Returns:
        list: Une liste de tuple ((chemin), effectif, frequence)
    """
    if occurencesPathsList and freqDist:
        occurences = occurencesPathsList.most_common()
        stat = list()

        #On parcours la liste contenant les occurences de chaque chemins
        for i in range(0, len(occurences)):
            stat.append((occurences[i][0], occurences[i][1], freqDist[i][1]))

        return stat
    else:
        print("La liste statistique est invalide ")
        sys.exit()
    
def meanLenPaths(stats, tot):
    """Calcule la moyenne de la longueur des chemins

    Args:
        stats (list): une liste statistiques (liste de tuples) de type ((chemin), effectif, frequence)
        tot (int): l'effectif total

    Returns:
        float: la moyenne des longueurs de chemins
    """
    if stats:
        mean = 0
        for i in range(0, len(stats)):
            #On multiplie la longueur du chemin par son effectif
            mean = mean + (len(stats[i][0]) * stats[i][1])

        meanPaths = mean/tot

        return meanPaths
    else:
        print("La liste statistique est invalide ")
        sys.exit()

def variance(stats, tot, mean):
    """Calcule la variance des longueurs de chemins

    Args:
        stats (list): une liste statistiques (liste de tuples) de type ((chemin), effectif, frequence)
        tot (int): l'effectif total des chemins
        mean (float): la moyenne des longueurs de chemins

    Returns:
        float: la variance des longueurs de chemins
    """
    if stats:
        var = 0
        for i in range(0, len(stats)):
            #On multiplie la longueur du chemin par son effectif puis on soustrait la moyenne au carré
            var = var + (math.pow((len(stats[i][0]) * stats[i][1]), 2) - math.pow(mean, 2))

        variance = var/tot

        return variance
    else:
        print("Pas de liste statistiques")
        sys.exit()

def getProbs(graph, v):
    """Donne les probabilités des arcs des successeurs de v

    Args:
        graph (Digraph): le graphe orienté
        v (int): le noeud

    Returns:
        list: une liste de probabilités de chaque successeurs
    """
    succ = list(graph.successors(v))   
    prob = list()
    
    #On parcours la liste des successeurs afin d'en tirer les probabilités
    for i in succ:
        tmp = graph.get_edge_data(v, i)
        prob.append(tmp.get('p'))
    
    return prob

def paths(graph, v):
    """Traverse aléatoirement le graphe à partir d'un sommet v donné

    Args:
        graph (DiGraph): Le graph orienté à parcourir
        v (int): Le sommet de départ

    Returns:
        list: Une liste de chemins parcouru aléatoirement dans le graphe
    """
    ret = list()

    #On parcourt le graphe 100 fois à partir du sommet v
    for z in range(0, 100):
        path = list()

        #à partir du sommet v donné, on traverse le graphe plusieurs fois afin d'avoir des chemins uniques
        while True:
            #ici, on verifie si on veut ou non une distribution uniforme des probabilités
            if utils.p == True :
                probs = getProbs(graph, v)
                tmpV = np.random.choice(list(graph.successors(v)), p=probs)
            else:
                tmpV = np.random.choice(list(graph.successors(v)))

            if graph.out_degree(tmpV) != 0:
                tmpPath = list()
                tmpPath.append(v)
                tmpPath.append(tmpV)
                hasPath_outdegree = True
                #On traverse le graphe à partir d'un autre point (les successeurs des successeurs de v)
                while True:
                    #ici, on verifie si on veut ou non une distribution uniforme des probabilités
                    if utils.p == True:
                        probs = getProbs(graph, tmpV)
                        tmpV = np.random.choice(list(graph.successors(tmpV)), p=probs)
                    else:
                        tmpV = np.random.choice(list(graph.successors(tmpV)))

                    if (nx.has_path(graph, tmpV, v) == False) or (graph.out_degree(tmpV) == 0):
                        hasPath_outdegree = False
                        break
                    elif (tmpV == v):
                        break
                    else:
                        tmpPath.append(tmpV)
                
                #On cherche des chemins unique pour arrêter la boucle, d'où la boucle avec range(0, 100) afin de traverser le graphe plusieurs fois
                if (tmpPath not in path) and (hasPath_outdegree == True):
                    path.append(tmpPath)
                else:
                    break
            else:
                break

        ret.append(path)

    return ret

def main(name):
    #Charger le graphe
    graph = loadGraph(name)

    #On verifie la forte connexité du graphe
    isStronglyConnected = isStronglyConn(graph)
    if isStronglyConnected == False:
        sys.exit("Le graphe n'est pas fortement connexe ")

    if graph.number_of_nodes() <= 1:
        sys.exit("Le graphe n'a qu'un seul sommet.")
    
    #taille du chemin
    N = int(input("Entrez la taille du chemin "))

    if N <= 0 :
        sys.exit("Le nombre entré doit être plus grand que 0")

    print("Entrez un numéro de noeuds entre 0 et %d" % (MAX-1))
    v = int(input())

    if v < 0 or v >= MAX:
        sys.exit("Numéro de noeuds invalide.") 

    #matrice adjointe
    matrix = getAdjMatrix(graph)

    #Puissance de la matrice
    matrixExp = mulMatrix(matrix, N)

    #Afficher la longueur du chemin
    print("[ATTENTION] Si la valeur du chemin est negative, cela signifie que c'est une TRES grande valeur")
    print("La longueur du chemin est de : ", matrixExp[v,v])

    #Proababilité de chemin N et chemin au plus N
    probN = exactLength(matrixExp, v)
    print("La probabilité de retourner en v avec un chemin de longueur exactement n est de : ", probN)

    probAtMost = atMostLength(matrix, v, N)
    print("La probabilité de retourner en v avec un chemin de longueur au plus n", probAtMost)

    #On informe que la probabilité ne sera pas de 1/t
    if utils.p : 
        print("La distribution des probabilités n'est plus de 1/t")


    print("[ATTENTION] Cette opération peut prendre quelques temps")

    #on traverse le graphe aléatoirement
    tmpPath = paths(graph, v) 

    #On filtre les listes vides (-> chemins ne menant pas au sommet choisit)
    pathsList = list(filter(None, tmpPath)) 
    del tmpPath #On libère la mémoire
    
    #On cherche la taille du plus petit chemin
    smallPath = smallestPath(pathsList)
    print("La longueur du plus petit chemin est de : %d" % (smallPath))

    #On cherche la taille du plus grand chemin
    bigPath = biggestPath(pathsList)
    print("La longueur du plus grand chemin est de : %d" % (bigPath))

    #Occurencces des chemins
    occ = utils.occurences(pathsList)

    #On cherche l'effectif total
    tot = Total(occ)
    print("L'effectif Total est : %d" % (tot))

    #On cherche la distribution de fréquence
    freqDist = frequencyDistribution(occ)

    #On met en lien les effectifs et la distribution de fréquence
    datas = stats(occ, freqDist)

    #On cherche la longueur moyenne des chemins
    meanLen = meanLenPaths(datas, tot)
    print("La moyenne de la longueur des chemins = %f" % (meanLen))
    
    #On cherche la variance de la longueur des chemins
    varianceLen = variance(datas, tot, meanLen)
    print("La variance de la longueur des chemins = %f" % (varianceLen))
    
    #On écrit tout dans un fichier
    utils.writeStat(tot, datas, smallPath, bigPath, meanLen, varianceLen)

    if utils.show:
        showGraph(graph)
