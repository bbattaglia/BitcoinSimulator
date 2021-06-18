from networkx.readwrite.json_graph import adjacency
from metrix import *
from simulator import *
import os
from varname import argname


NUMBER_OF_NODE = 100
sequence = []
DG = nx.DiGraph()


def addMLTransaction(DG):
    addTransaction(DG, '6', '33', 0.058764, color = True)
    addTransaction(DG, '33', '20', 0.058763, color = True)
    addTransaction(DG, '20', '54', 0.058762, color = True)
    addTransaction(DG, '54', '77', 0.058761, color = True)



def saveResultAsFile(x):
    fileRes = "res/"+argname(x)+".txt"
    os.makedirs(os.path.dirname(fileRes), exist_ok=True)
    with open(fileRes, 'w') as f:	
        print ("Saving "+str(argname(x))+" in the folder")	
        print(argname(x), file = f)
        for degree in x:
            print(degree, file =f)
    print('--------------')

def findSequence(DG):
    sequence.clear()
    amount = nx.get_edge_attributes(DG, 'value')
    for i in amount:
        sequence.append(amount[i])
    return sequence

try:
    with open('bitcoin.gexf') as f:
        if(f):
            DG = nx.read_gexf('bitcoin.gexf')
            #plotGraph(DG)
except IOError:
    DG = createGraph(NUMBER_OF_NODE)    
    calculateMetrix(DG, findSequence(DG))
    #plotGraph(DG)


metrix = graphMetrix(DG)
inDegree = metrix[1]
outDegree = metrix[2]
saveResultAsFile(inDegree)
saveResultAsFile(outDegree)

# addTransaction(DG, '66', '37', 0.058764, color = True)
# addTransaction(DG, '66', '37', 1.2, color = True)
# print(DG.edges('66'))
# plotGraph(DG)
#deleteTransaction(DG, '77', '76',1.2)
#plotGraph(DG)

#addMLTransaction(DG)

#metrix = graphMetrix(DG) #return density, in_degree, out_degree, density, closeness, betweenness



