from graph import *
from path import *



g = LoadGraphFromFile("Grafo1.txt")
PlotReachable(g, "A")
PlotShortestPathSimple(g, "A", "F")
