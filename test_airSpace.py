from airSpace import *

airspace = LoadAirSpace("Catalonia_graph/Cat_nav.txt", "Catalonia_graph/Cat_seg.txt", "Catalonia_graph/Cat_aer.txt")

PlotAirSpace(airspace)
PlotNode(airspace, "LEVC")
PlotReachable(airspace, "LEBL")
PlotShortestPathSimple(airspace, "MARTA", "GODOX")

