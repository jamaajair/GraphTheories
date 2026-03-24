import random
import math
import collections
import numpy as np

debug = False
p = False
show = False

#Procédure pour activer la fonction debug afin de voir les comportements du programme
def debugOn():
    global debug
    debug = True
    
#Procédure pour activer la fonction afin d'avoir une distribution non-uniforme des probas
def pOn():
    global p
    p = True

def showOn():
    global show
    show = True

def randomProb(arcs):
    precision = 1000000
    probs = []
    sum = 0
    crtPrec = precision

    #Soit une liste de taille N, on distribue des valeurs jusqu'à l'indice N-2
    for i in range(0, len(arcs)-1):
        val = random.randrange(crtPrec)
        sum = sum + val
        probs.append(float(val)/precision)
        crtPrec = crtPrec - val
     
    #à l'indice N-1 on ajoute la valeur restante des probabilités afin d'avoir une probabilité totale de 1
    probs.append(float(precision-sum)/precision)

    return probs


#Fonction utilisée dans generator.py afin de créer une liste d'arcs
def randomization(index, max):
    arcs = []

    #arcsNb = random.randint(2, max)
    if index == max:
        arcs.append(0)
    else:
        arcs.append(index+1)

    for j in range(1, random.randint(2, max)):
        val = random.randint(0, max)
        if (val not in arcs) and (val != index) and (val != index+1):
            arcs.append(val)

    return arcs

#Fonction utilisée dans file.py afin de génerer une matrice de liste à une valeur val donnée.
def initList(matrix, val):
    myList = list()
    #On initialise une liste qui contiendra des listes
    for i in range(0, int(math.sqrt(matrix.size))):
        tmp = list()
        #On ajoute une liste contenant la valeur de val (de taille n dans le cas d'une matrice carré n)
        for j in range(0, int(math.sqrt(matrix.size))):
            tmp.append(val)
        myList.append(tmp)
    return myList

#Fonction utilisée dans file.py afin de rentre une matrice de liste en une liste de 1D
def flatten(t):
    flat = list()
    for i in range(0, len(t)):
        for j in range(0, len(t[i])):
            flat.append(t[i][j])
    
    return flat

#Fonction utilisée dans file.py afin de compter le nombre d'occurences d'une liste dans une liste
def occurences(liste):

    myList = flatten(liste)

    newlist = map(tuple, myList)

    occ = collections.Counter(newlist)

    return occ

#Fonction utilisée dans file.py afin d'écrire un fichier
def writeStat(effectif, datas, smallestPath, biggestPath, meanLen, varianceLen):

    with open("stat.txt", "w") as file:
        file.write("Le plus grand chemin est : " + str(biggestPath) + '\n')
        file.write("Le plus petit chemin est : " + str(smallestPath) + '\n')
        file.write("L'effectif total est : " + str(effectif) + '\n')
        file.write("La moyenne des longueurs de chemins est : " + str(meanLen) + '\n')
        file.write("La variance des longueurs de chemins est : " + str(varianceLen) + '\n')
        file.write("((Chemins), effectif, frequence)" + '\n')
        for i in range(0, len(datas)):
            file.write(str(datas[i]) + '\n')
        file.close()