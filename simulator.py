import networkx as nx
import random
from metrix import *
import sys

numTransaction = 0
toList = []

def diff(list1, list2):
	for i in range(len(list2)):
		if list2[i] in list1:
			list1.remove(list2[i])		
	return list1



def addTransaction(DG, sender, receiver, amount):
	global numTransaction
	color = ' '
	if(amount>0.1):
		color = 'r'
	else:
		color ='b'
	#one to one transaction
	if isinstance(sender, int):
		if isinstance(receiver, int):
			DG.add_edge(sender,receiver, value = amount, edge_color = color)
			numTransaction += 1
		else:
			#batched transaction
			for j in range(len(receiver)):
				DG.add_edge(sender,receiver[j], value = amount, edge_color = color)
				numTransaction += 1
	else:
		#multi input transaction
		for i in range(len(sender)):
			if isinstance(receiver, int):
				DG.add_edge(sender[i],receiver, value = amount, edge_color = color)
				numTransaction += 1
			else:
				#multi input and multi output transaction
				for j in range(len(receiver)):
					DG.add_edge(sender[i],receiver[j], value = amount, edge_color = color)
					numTransaction += 1


def init(DG):
	node = []
	global toList
	toList = list(DG)
	multiInpuntTransaction = random.sample(toList, int(0.07*len(toList)))
	#print(multiInpuntTransaction)
	#sys.exit()
	for i in range(len(toList)):
		node.append([])
		node[i].append(toList[i])
		node[i].append(0)
		
	outDegreeNode = node[:]
	inDegreeNode = node[:]
	singleOutputNode = []
	doubleOutputNode = []
	singleInputNode = []
	doubleInputNode = []
	
	ghostInputNode = random.sample(inDegreeNode, (int(0.26*len(node))))
	inDegreeNode = diff(inDegreeNode, ghostInputNode)
	singleInputNode = random.sample(inDegreeNode, (int(0.63*len(node))))
	inDegreeNode = diff(inDegreeNode, singleInputNode)
	doubleInputNode = random.sample(inDegreeNode, (int(0.05*len(node))))
	inDegreeNode = diff(inDegreeNode, doubleInputNode)
	for i in range(len(inDegreeNode)):
		inDegreeNode[i][1] = 3

	ghostOutputNode = random.sample(outDegreeNode, (int(0.22*len(node))))
	outDegreeNode = diff(outDegreeNode, ghostOutputNode)
	singleOutputNode = random.sample(outDegreeNode, (int(0.25*len(node))))
	outDegreeNode = diff(outDegreeNode, singleOutputNode) 
	doubleOutputNode = random.sample(outDegreeNode, (int(0.5*len(node))))
	outDegreeNode = diff(outDegreeNode, doubleOutputNode)
	# print("single Output "+str(len(singleOutputNode)))
	# print("--------------")
	# print("double Output "+str(len(doubleOutputNode)))
	# print("--------------")
	# print("multiple Output "+str(len(outDegreeNode)))
	maxnumTransaction = sum((len(singleOutputNode),(2*len(doubleOutputNode)),(8*len(outDegreeNode))))
	return ghostInputNode,singleInputNode,doubleInputNode,inDegreeNode,ghostOutputNode,singleOutputNode,doubleOutputNode,outDegreeNode,multiInpuntTransaction, maxnumTransaction

def chooseReceiver(singleInputNode, doubleInputNode, multiInputNode):
	rnd = random.randrange(1,4)
	node = 0
	if rnd == 1 and len(singleInputNode) != 0:
		node = random.choice(singleInputNode)
	elif rnd == 2 and len(doubleInputNode) != 0:
		node = random.choice(doubleInputNode)
	elif rnd == 3 and len(multiInputNode) != 0:
		node = random.choice(multiInputNode)
	return node
	
def chooseSender(singleOutputNode, doubleOutputNode, multiOutputNode):
	sender = None
	index = None
	currentList = None
	randomOutput = random.randrange(1,4)	
	if(randomOutput == 1 and len(singleOutputNode) !=0):
		currentList = singleOutputNode
		sender = random.choice(currentList)
		index = 1	
	elif(randomOutput == 2 and len(doubleOutputNode) !=0):
		currentList = doubleOutputNode
		sender = random.choice(currentList)
		index = 2
	elif(randomOutput == 3 and len(multiOutputNode) !=0):
		currentList = multiOutputNode
		sender = random.choice(currentList)
		index = random.randrange(3,8)
	else:
		chooseSender(singleOutputNode, doubleOutputNode, multiOutputNode )
	return sender, index, currentList

def fillGraph(DG):
	x = init(DG)
	#ghostInputNode = x[0]
	singleInputNode = x[1]
	doubleInputNode = x[2]
	multiInputNode = x[3]
	#ghostOutputNode = x[4]
	singleOutputNode = x[5]
	doubleOutputNode = x[6]
	multiOutputNode = x[7]
	#multiInpuntTransaction = x[8]
	maxNumTransaction = x[9]
	while(True):
		while(True):
			data = chooseSender(singleOutputNode, doubleOutputNode, multiOutputNode)
			if(data[0] != None and data[1] != None and data[2] != None):
				break
		sender = data[0]
		if(numTransaction <= int(maxNumTransaction*0.9)):
			amount = round(random.uniform(0.00001,0.1),8)
		else:
			amount = round(random.uniform(0.1,14),8)
		index = data[1]
		currentList = data[2]
		for i in range(index):
			while(True): 
				receiver = chooseReceiver(singleInputNode, doubleInputNode, multiInputNode)
				if(receiver != 0 and receiver != sender):
					break
			addTransaction(DG, sender[0],receiver[0], amount)
			receiver[1] = receiver[1]+1
			if(receiver in singleInputNode and receiver[1] == 1):
				singleInputNode.remove(receiver)
			elif(receiver in doubleInputNode and receiver[1] == 2):
				doubleInputNode.remove(receiver)
		currentList.remove(sender)
		if(len(singleOutputNode) == 0 and len(doubleOutputNode) == 0 and len(multiOutputNode) == 0) :
			break

def checkReceiver(sender, receiver):
	for j in receiver:
		if j in sender:
			receiver.remove(j)
			if(len(receiver) == 0):
				receiver = random.sample(toList,random.randint(2,int(0.05*len(toList))))
				checkReceiver(sender, receiver)
	return receiver

def insertMultiInput():
	size = int(numTransaction*0.07)
	for i in range(size):
		senderNum = random.randint(2,int(0.05*len(toList)))
		sender = random.sample(toList,senderNum)
		receiverNum = random.randint(2,int(0.05*len(toList)))
		receiver = random.sample(toList,receiverNum)
		receiver = checkReceiver(sender, receiver)
		amount = round(random.uniform(0.001,3.5), 3) #important to define a correct amount
		addTransaction(DG, sender, receiver, amount)


DG = nx.DiGraph()
for i in range(100):
	DG.add_node(i)
fillGraph(DG)
#insertMultiInput()

#calculateMetrix(DG)
edge = DG.edges()
colors = nx.get_edge_attributes(DG,'edge_color').values()
values = nx.get_edge_attributes(DG, 'value') 
pos=nx.spring_layout(DG)
nx.draw_networkx(DG, pos=pos, arrows = True, with_labels= True, edge_color=list(colors))
nx.draw_networkx_edge_labels(DG, pos=pos, edge_labels=values, font_size=7)
nx.write_gexf(DG, "bitcoin.gexf")
plt.show()
