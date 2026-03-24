import json
import random
import sys
import utils

data = {}
NbNoeuds = int(input("Entrez le nombre de noeuds :"))

if NbNoeuds <= 0:
    print("Le nombre de noeuds doit être supérieur à 1.")
    sys.exit()


if NbNoeuds > 1:
    data['NbNoeuds'] = NbNoeuds
    data['Noeuds'] = []
    for i in range(0, NbNoeuds):
        arcs = utils.randomization(i, NbNoeuds-1)
        p = utils.randomProb(arcs)
        val = {'id': i, 'arcs': arcs, 'p':p}
        data['Noeuds'].append(val)
else:
    data['NbNoeuds'] = NbNoeuds
    data['Noeuds'] = []
    val = {'id': 0, 'arcs': [], 'p':[1]}
    data['Noeuds'].append(val)

with open('graphe.json', 'w') as out:
    json.dump(data, out, indent=5)
