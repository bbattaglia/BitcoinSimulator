import networkx as nx
import matplotlib.pyplot as plt
import powerlaw
#from simulator import *

def calculateAverageDegree(G):
	sum = 0
	averageDegree = 0
	averageDegree = nx.average_degree_connectivity(G)
	for value in averageDegree:
		sum = sum + averageDegree[value]
	averageDegree = sum/len(averageDegree)
	return averageDegree


def calculateMetrix(DG,sequence):

	sumOut = sumIn = singleIn = singleOut = doubleIn = doubleOut = zeroIn = zeroOut = totOut = totIn = 0
	fit = powerlaw.Fit(sequence) 
	print(fit.alpha)
	print("--------------")
	if(1.75<fit.alpha and fit.alpha > 3.5):
		return False
	else:	
		for i in range(len(DG)):
			#in degree 
			totOut = totOut + DG.out_degree(i)
			if DG.out_degree(i) ==1 :
				singleOut = singleOut+1
			elif DG.out_degree(i) == 2:
				doubleOut = doubleOut+1
			elif DG.out_degree(i) == 0:
				zeroOut = zeroOut+1
			elif DG.out_degree(i) >2:
				sumOut = sumOut+1
			#out degree
			totIn = totIn + DG.in_degree(i)
			if DG.in_degree(i) == 1 :
				singleIn = singleIn+1
			elif DG.in_degree(i) == 2:
				doubleIn = doubleIn+1
			elif DG.in_degree(i) == 0:
				zeroIn = zeroIn+1
			elif DG.in_degree(i) >2:
				sumIn = sumIn+1 
		print("Transazioni per nodo:")
		print("OutDregree (#numtransaction, #node): zero: "+str(zeroOut)+", single: "+str(singleOut)+", double: "+str(doubleOut)+". multi: "+str(sumOut))
		print("InDegree (#numtransaction, #node): "+str(zeroIn)+", single: "+str(singleIn)+", double: "+str(doubleIn)+". multi: "+str(sumIn))
		print("InDegree medio: "+str(totIn/len(list(DG))))
		print("OutDegree medio: "+str(totOut/len(list(DG)))) 
		print("--------------")
	
		#degree medio main component
		G = nx.to_undirected(DG)
		mainComponents = sorted(nx.connected_components(G), key=len, reverse=True)
		MC = G.subgraph(mainComponents[0])
		print("Net average degree: "+str(calculateAverageDegree(DG)))
		print("MC average degree: "+str(calculateAverageDegree(MC)))
		print("--------------")

		#average clustering coefficient
		
		print("ACC MC: "+str(nx.average_clustering(MC)))
		print("--------------")
		
		print("ASPL MC: "+str(nx.average_shortest_path_length(MC)))
		S = [DG.subgraph(c).copy() for c in nx.weakly_connected_components(DG)]
		for index,value in enumerate(S):
			try: aspl
			except NameError: aspl = 0
			aspl = aspl + nx.average_shortest_path_length(value)
			if index == (len(S)-1):
				aspl = aspl/len(S)
		print("ASPL: "+str(aspl)) 
		return True

