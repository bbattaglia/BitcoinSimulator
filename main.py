from metrix import *
from simulator import *


try:
    with open('./bitcoin.gexf') as f:
        if(f):
            DG = nx.read_gexf('./bitcoin.gexf')
            plotGraph(DG)
except IOError:
    DG = createGraph(100)
    plotGraph(DG)
