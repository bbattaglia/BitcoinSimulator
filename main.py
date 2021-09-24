from metrix import *
from simulator import *
import os
from varname import argname



NUMBER_OF_NODE = 100
sequence = []
DG = nx.DiGraph()


#-------------------------------Functions definition-----------------------------
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
    
    
def identifyML(DG, node):  
    
    path = []
    toReturn = []
    ego_network = nx.ego_graph(DG,node,radius = 5)
    adjacent_node = ego_network.edges(node)
    
    #calculate all the paths from the node to the node
    for u, v in adjacent_node: 
        try:
            path.extend(nx.all_simple_paths(ego_network, str(v), node))
        except:
            pass
    currentTimestamp = 0
    #if a node of the path is in a mixer cluster, then the path could be dangerous
    for i in range(len(path)):
        previousTimestamp = 0
        validPath = True
        for j in range(len(path[i])):
            try:
                mixer = ego_network.nodes[path[i][j]]['mixer']
                if mixer:
                    toReturn.append(path[i])
                    break
            except:
                pass
            #if not, it is verified that the node have a coherent timestamp
            if(j+1) < len(path[i]) and validPath == True:
                currentTimestamp = DG.get_edge_data(path[i][j],path[i][j+1])
                if(j == 0):
                    previousTimestamp = DG.get_edge_data(node,path[i][j])

                if(previousTimestamp[0]['date']< currentTimestamp[0]['date']):
                    previousTimestamp = currentTimestamp
                else:
                    validPath = False
                    break

            if (j+2) == len(path[i]) and validPath:
                toReturn.append(path[i])
    for i in toReturn:
        print(str(i))
    



def addMLTransaction(DG):
    DG.nodes['91']['mixer'] = True
    addTransaction(DG, '48', '50', 0.058764, 1620575060, color = True)
    addTransaction(DG, '50', '55', 0.058763, 1620575061, color = True)
    addTransaction(DG, '55', '13', 0.058762, 1620575062, color = True)
    addTransaction(DG, '13', '91', 0.058761, 1620575063, color = True)
    addTransaction(DG, '91', '48', 0.056, 1620575064, color = True)    



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


#------------------------main block----------------------------
try:
    with open('bitcoin.gexf') as f:
        if(f):
            DG = nx.read_gexf('bitcoin.gexf')
            #plotGraph(DG)
except IOError:
    DG = createGraph(NUMBER_OF_NODE)    
    calculateMetrix(DG, findSequence(DG))
    plotGraph(DG)
    
addMLTransaction(DG)
identifyML(DG, '48')

#metrix = graphMetrix(DG,'48')
#new_metrix = graphMetrix(DG,'48') #return density, in_degree, out_degree, density, closeness, betweenness

# inDegree = metrix[1]
# outDegree = metrix[2]
# saveResultAsFile(inDegree)
# saveResultAsFile(outDegree)


#identifyActivity(DG, '48')
#DG.nodes['100']['mixer'] = True
# attribute = DG.get_edge_data('42','19')
# print(attribute[0]['date'])
