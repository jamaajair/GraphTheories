
import json
import os
import random

def randomization(index, max ):

    arcs = []
   
    nb_arcs = random.randint(0, max)

    for i in range(0, nb_arcs):
        val = random.randint(0, max)
        if ((val not in arcs) and (val != index)) :
            arcs.append(val)

    return arcs


data = {}
#data['NomGraphe'] = str(input("Entrez un nom pour le graphe"))
NbNoeuds = int(input("Entrez le nombre de noeuds : "))
data['NbNoeuds'] = NbNoeuds-1
data['Noeuds'] =  []
 
i = 0
while i < NbNoeuds:
    arcs = randomization(i, NbNoeuds-1)
    dicti = {'id': i, 'arcs': arcs}
    data['Noeuds'].append(dicti)
    
    i = i + 1

with open('test.json', 'w') as outfile:
    json.dump(data, outfile, indent=5)
