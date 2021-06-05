from metrix import *
from simulator import *
import os.path as path

NUMBER_OF_NODE = 100
sequence = []

def findSequence(DG):
    sequence.clear()
    amount = nx.get_edge_attributes(DG, 'value')
    for i in amount:
        sequence.append(amount[i])
    return sequence




try:
    with open('bitcoin.gexf') as f:
        if(f):
            print('esiste')
            DG = nx.read_gexf('bitcoin.gexf')
            plotGraph(DG)
except IOError:
    DG = createGraph(NUMBER_OF_NODE)    
    calculateMetrix(DG, findSequence(DG))
    plotGraph(DG)