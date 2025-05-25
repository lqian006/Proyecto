from airSpace import *

#---Para mostrar el grafo---#

airspace = LoadAirSpace("Cat_nav.txt", "Cat_seg.txt", "Cat_aer.txt")
PlotAirSpace(airspace)

#---Para mostrar vecinos---#

space = LoadAirSpace("Cat_nav.txt", "Cat_seg.txt", "Cat_aer.txt")
PlotNode(space, "MARTA")

#---Para mostrar reachables---#

airspace = LoadAirSpace("Cat_nav.txt", "Cat_seg.txt", "Cat_aer.txt")
PlotReachable(airspace, "ALT.D")

#---Camino más corto---#

airspace = LoadAirSpace("Cat_nav.txt", "Cat_seg.txt", "Cat_aer.txt")
PlotShortestPathSimple(airspace, "CDP", "VAKIN")