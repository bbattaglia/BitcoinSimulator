from metrix import *
from simulator import *
import os
from varname import argname



NUMBER_OF_NODE = 100
sequence = []
DG = nx.DiGraph()

def identifyActivity(DG, node):
    path = []
    ego_network = nx.ego_graph(DG,'48',5)
    adjacent_node = ego_network.edges('48')
    #plotGraph(ego_network)
    # path = nx.all_simple_paths(ego_network, '50', '48')
    # print(list(path))
    for u, v in adjacent_node: 
        try:
            path.append(nx.all_simple_paths(ego_network, str(v), node))
        except:
            pass
    for i in range(len(path)):
        print(list(path[i]))
    



def addMLTransaction(DG):
    addTransaction(DG, '48', '50', 0.058764, color = True)
    addTransaction(DG, '50', '55', 0.058763, color = True)
    addTransaction(DG, '55', '13', 0.058762, color = True)
    addTransaction(DG, '13', '91', 0.058761, color = True)
    addTransaction(DG, '91', '48', 0.056, color = True)    



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


#metrix = graphMetrix(DG,'48')
#new_metrix = graphMetrix(DG,'48') #return density, in_degree, out_degree, density, closeness, betweenness
# inDegree = metrix[1]
# outDegree = metrix[2]
# saveResultAsFile(inDegree)
# saveResultAsFile(outDegree)

addMLTransaction(DG)
identifyActivity(DG, '48')




