import collections
from typing import Generator
import networkx as nx #Pour les manipulations basiques des graphes
import matplotlib.pyplot as plt #Pour afficher des graphes afin d'avoir un visuel (c.f. https://networkx.org/documentation/stable/tutorial.html)
import json #Pour lire le format json d'un graphe 
import numpy as np
import math
import random
import decimal
from scipy.stats import uniform
import statistics 



def load_graph(name=str):
    """[summary]

    Args:
        name (string): le nom du fichier en entrée par l'utilisateur

    Return:
        Retourne un graphe orienté lu à partir d'un fichier JSON
    """
    try:
        #ouverture du fichier
        file = open(name) 

        #chargement du fichier sous le format JSON
        data = json.load(file) 

        #on charge le nombre de noeuds
        Nombre_noeuds = data['NbNoeuds'] 

        #on construit un graphe non orienté
        graphe = nx.DiGraph()

        #On ajoute un seul si le nombre < 1 sinon on ajoute une serie de noeuds 
        graphe.add_nodes_from(range(0,Nombre_noeuds)) if Nombre_noeuds >= 1 else graphe.add_node(Nombre_noeuds)
        
        #Comme toutes les informations des noeuds sous directement fournis sous forme de dictionnaires
        #Nous avons pas eu d'autres choix que de créer une liste vide qui contiendra une liste avec les numéros de
        #noeuds
        Noeudsetinfos = []

        #Nous utilisons cette boucle afin de connecter les noeuds entre eux mais aussi pour collecter les informations des noeuds
        #Tout a été fait en une boucle pour éviter de faire 2 fois la même chose
        """for i in data['Noeuds']:
            #print(type(i)
            #print("%s" % (data['Noeuds'][i]['params']))
            #print("%s" % (data['Noeuds'][i]['arcs']))
            index = data['Noeuds'][i]['id']

            tuple_tmp = (index, data['Noeuds'][i]['params'])
            Noeudsetinfos.append(tuple_tmp)
            
            #Cette boucle permet de connecter les noeuds entre eux
            z = 0
            while z != len(data['Noeuds'][i]['arcs']):
                print("\t %d" % (data['Noeuds'][i]['arcs'][z]))
                graphe.add_edge(index, data['Noeuds'][i]['arcs'][z])
                z = z + 1
        """
        i = 0
        while i <= Nombre_noeuds:
            index = data['Noeuds'][i]['id']
            print("index = %d" % (index))

            #tuple_tmp = (index, data['Noeuds'][i]['p'])
            #Noeudsetinfos.append(tuple_tmp)

            #print(data['Noeuds'][i]['arcs'])            
            #Cette boucle permet de connecter les noeuds entre eux
            z = 0
            while z != len(data['Noeuds'][i]['arcs']):
                #print("\t %d" % (data['Noeuds'][i]['arcs'][z]))
                graphe.add_edge(index, data['Noeuds'][i]['arcs'][z])
                prob = data['Noeuds'][i]['p'][z]
                nx.set_edge_attributes(graphe, {(index, data['Noeuds'][i]['arcs'][z]): {"p" : prob}})
                print(graphe.get_edge_data(index, data['Noeuds'][i]['arcs'][z]))
                z = z + 1

            i = i + 1
            
        graphe.add_nodes_from(Noeudsetinfos) #On ajoute les informations sur les noeuds
        
        j = 0
        while j < Nombre_noeuds:
            print("i %d" % (j))
            print(graphe.nodes[j])
            j = j + 1

        #print(nx.info(graphe))



        file.close()
    except FileNotFoundError:
        print("Le fichier que vous fournissez n'existe pas !!")

    return graphe


"""def getAdjMatrix(graph= str, debug=bool):
    test = nx.adjacency_matrix(graph)
    print(type(test.todense()))
    A = np.linalg.matrix_power(test.todense(), 4) #augmente la puissance de la matrice de 4
    print(A)"""

def getAdjMatrix(graph):
    """Donne la matrice d'adjacence du graphe

    Args:
        graph (Graph): Un graphe orienté (ou non)

    Returns:
        np.array: Retourne la matrice adjacente du graphe
    """
    Matrix = nx.adjacency_matrix(graph)

    """if utils.debug == True:
         print(Matrix.todense())"""

    return Matrix.todense()

def ifMatrixirreductible(graph=np.matrix, debug=bool):
    """if np.any(graph <= 0) == False:
        return False"""
    #Matrice est dite irreductible ssi la valeur en i,j quand la matrice^N est > 0

    return True

def showGraph(graph):
    """Affiche le graphe dans une fenêtre

    Args:
        graph (Graph): Un graphe orienté (ou non)
    """
    layout = nx.random_layout(graph)
    nx.draw_networkx_nodes(graph, pos=layout, node_size=250, node_color='red')
    nx.draw_networkx_edges(graph, pos=layout, style='dotted', edge_color='blue')
    nx.draw_networkx_labels(graph, pos=layout)
    plt.show()

def pluslongchemin(liste):
    curr = 0
    max = len(liste[0][0])

    for i in range(0, len(liste)):
        for j in range(0, len(liste[i])):
            curr = len(liste[i][j])
            
            if(curr > max):
                max = curr
    return max

def pluspetitchemin(liste):
    if liste:    
        curr = 0
        min = len(liste[0][0])

        for i in range(0, len(liste)):
            for j in range(0, len(liste[i])):
                curr = len(liste[i][j])
                
                if(curr < min):
                    min = curr
        
        return min
    else:
        print("...")
        sys.exit()

def paths(g, v):
    ret = []
    path = None
    tmpV = None
    tmpPath = None
    trigg = None

    for z in range(0,100):
        path = []
        while True:
            tmpV = np.random.choice(list(g.successors(v)))

            if g.out_degree(tmpV) != 0:
                tmpPath = []
                tmpPath.append(v)
                tmpPath.append(tmpV)
                trigg = True
                while True:
                    tmpV = np.random.choice(list(g.successors(tmpV)))

                    if (nx.has_path(g, tmpV, v) == False) or g.out_degree(tmpV) == 0 :
                        trigg = False
                        break
                    elif (tmpV == v):
                        break
                    else:
                        tmpPath.append(tmpV)

                if (tmpPath not in path) and (trigg == True):
                    path.append(tmpPath)
                else:
                    break
            else:
                print("Pas de chemins possible")
                break
        
        ret.append(path)

    return ret

def prfile(liste):
    with open("listes.txt", "w") as file :
        for i in range(0,len(liste)):
            for j in range(0,len(liste[i])):
                file.write(str(liste[i][j]) + '\n')

    file.close()

def prfile2(liste):
    with open("distrib.txt", "w") as file :
        for i in range(0,len(liste)):
                file.write(str(liste[i]) + '\n')

    file.close()

def flatten(t):
    flat = list()
    for i in range(0, len(t)):
        for j in range(0, len(t[i])):
            flat.append(t[i][j])
    
    return flat

def occurences(liste):
    newlist = map(tuple, liste)

    occ = collections.Counter(newlist)

    return occ

def effTot(liste):
    effTotal = 0
    for i in range(0, len(liste)):
        effTotal = effTotal + liste[i][1]
    
    return effTotal

def distributionEff(liste):
    effTotal = effTot(liste)

    distribEff = list()

    for i in range(0, len(liste)):
        effTmp = liste[i][1]/effTotal
        distribEff.append((liste[i][0], effTmp))
    
    return distribEff

"""def irr(matrix):
    B = list()
    for i in range(0, int(math.sqrt(matrix.size))):
        tmp = list()
        for j in range(0, int(math.sqrt(matrix.size))):
            tmp.append(-1)
        B.append(tmp)

    nonz = np.nonzero(matrix)

    for z in range(0, len(nonz[0])):
        B[nonz[0][z]][nonz[1][z]] = 1
    
    return B"""

def initList(matrix):
    B = list()
    for i in range(0, int(math.sqrt(matrix.size))):
        tmp = list()
        for j in range(0, int(math.sqrt(matrix.size))):
            tmp.append(-1)
        B.append(tmp)
    return B

def mulMatrix(matrix, n):
    """Multiplie la matrice

    Args:
        matrix (np.array): La matrice d'adjacence du graphe
        n (int): le degré de puissance de la matrice

    Returns:
        np.array: La matrice d'adjacence puissance n
    """
    Matrix = np.linalg.matrix_power(matrix, n)

    """if utils.debug == True:
        print("Matrice puissance %d " % (n))
        print(Matrix)"""

    return Matrix

def irr(matrix):
    B = initList(matrix)

    for m in range(1, matrix.size+1):
        matriceTmp = mulMatrix(matrix, m)
        nonzeros = np.nonzero(matriceTmp)
        for z in range(0, len(nonzeros[0])):
            B[nonzeros[0][z]][nonzeros[1][z]] = 1

    if np.any(np.array(B) <= 0) == True:
        return False

    return True

def getProbs(graph, v):
    succ = list(graph.successors(v))   
    prob = list()

    for i in succ:
        tmp = graph.get_edge_data(v, i)
        prob.append(tmp.get('p'))
    
    return prob


graphe = load_graph("test.json")

def randomProb(arcs):
    
    TOTAL = 1.00
    probTmp = TOTAL
    prob = []

    for i in range(0, len(arcs)):
        tmp = random.uniform(0, probTmp)
        test = decimal.Decimal(tmp)
        #print(test.quantize(decimal.Decimal('0.001'), rounding=decimal.ROUND_UP))

        probTmp = probTmp - tmp
        if probTmp > 0:
            prob.append(tmp)
        else:
            prob.append(0)
        
        #prob[len(prob)-1] = probTmp

    return prob

print(nx.strongly_connected.is_strongly_connected(graphe))
showGraph(graphe)

#print(getProbs(graphe, 3))

#print(graphe.out_degree(3))
#print(list(graphe.successors(3)))
#print(paths(graphe,70,None))
#listee = paths(graphe, 2)
#print("plus long chemin = ",pluslongchemin(listee))
#print("plus petit chemin = ", pluspetitchemin(listee))
#test = occurences(flatten(listee))
#print(test)
"""print("effectif Total:", effTot(test.most_common()))
prfile(listee)
prfile2(distributionEff(test.most_common()))"""

"""matrix = getAdjMatrix(graphe)
#print(int(math.sqrt(matrix.size)))
#print(matrix)
#noz = np.nonzero(matrix)
#print(noz[0][0], noz[1][0])
showGraph(graphe)
print(irr(matrix))"""

#print(nx.has_path(graphe, 4,1))



