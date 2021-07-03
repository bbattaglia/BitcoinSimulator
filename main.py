from metrix import *
from simulator import *
import os
from varname import argname



NUMBER_OF_NODE = 100
sequence = []
DG = nx.DiGraph()

def identifyActivity(DG, node):
    path = []
    visitedNode = []
    i = 1
    addTransaction(DG, '50', '48', 0.04, color = True)
    while(True):

        ego_network = nx.ego_graph(DG,node,i)
        if(i == 1):
            adjacent_node = ego_network.edges()
            adjacent_node = list(adjacent_node)
            for i in range(len(adjacent_node)):
                current = adjacent_node[i][1]
                if(current == node):
                    firstValue = ego_network.get_edge_data(node,adjacent_node[i][0])
                    secondValue = ego_network.get_edge_data(adjacent_node[i][0],node)
                    if(firstValue[0]['value'] > secondValue[0]['value']):
                        path.append(node)
                        path.append(adjacent_node[i][0])
            break
    
    
def identifyMixerAddress(DG, node):  
    
    path = []
    toReturn = []
    ego_network = nx.ego_graph(DG,node,5)
    adjacent_node = ego_network.edges(node)
    
    for u, v in adjacent_node: 
        try:
            path.extend(nx.all_simple_paths(ego_network, str(v), node))
        except:
            pass
    for i in range(len(path)):
        for j in range(len(path[i])):
            try:
                if ego_network.nodes[path[i][j]]['mixer'] == True:
                    toReturn.append(path[i])
                    print("hi")
            except:
                pass
    print(toReturn)
    



def addMLTransaction(DG):
    DG.nodes['22']['mixer'] = True
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
# identifyActivity(DG, '48')
identifyMixerAddress(DG, '48')



