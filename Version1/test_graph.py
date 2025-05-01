from graph import *
from node import Node
def CreateGraph_1 ():
    G = Graph()
    AddNode(G, Node("A",1,20))
    AddNode(G, Node("B",8,17))
    AddNode(G, Node("C",15,20))
    AddNode(G, Node("D",18,15))
    AddNode(G, Node("E",2,4))
    AddNode(G, Node("F",6,5))
    AddNode(G, Node("G",12,12))
    AddNode(G, Node("H",10,3))
    AddNode(G, Node("I",19,1))
    AddNode(G, Node("J",13,5))
    AddNode(G, Node("K",3,15))
    AddNode(G, Node("L",4,10))
    AddSegment(G, "AB", "A", "B")
    AddSegment(G, "AE", "A", "E")
    AddSegment(G, "AK", "A", "K")
    AddSegment(G, "BA", "B", "A")
    AddSegment(G, "BC", "B", "C")
    AddSegment(G, "BF", "B", "F")
    AddSegment(G, "BK", "B", "K")
    AddSegment(G, "BG", "B", "G")
    AddSegment(G, "CD", "C", "D")
    AddSegment(G, "CG", "C", "G")
    AddSegment(G, "DG", "D", "G")
    AddSegment(G, "DH", "D", "H")
    AddSegment(G, "DI", "D", "I")
    AddSegment(G, "EF", "E", "F")
    AddSegment(G, "FL", "F", "L")
    AddSegment(G, "GB", "G", "B")
    AddSegment(G, "GF", "G", "F")
    AddSegment(G, "GH", "G", "H")
    AddSegment(G, "ID", "I", "D")
    AddSegment(G, "IJ", "I", "J")
    AddSegment(G, "JI", "J", "I")
    AddSegment(G, "KA", "K", "A")
    AddSegment(G, "KL", "K", "L")
    AddSegment(G, "LK", "L", "K")
    AddSegment(G, "LF", "L", "F")

    return G


def CreateGraph_2():
   G = Graph()
   AddNode(G, Node("A", 10, 20))
   AddNode(G, Node("B", 0, 0))
   AddNode(G, Node("C", 20, 0))
   AddSegment(G, "AB", "A", "B")
   AddSegment(G, "AC", "A", "C")
   AddSegment(G, "CB", "C", "B")
   return G


def CreateGraph_3():
    print("\nProbando carga de grafo desde archivo...")
    G2 = LoadGraphFromFile("Datos.txt")
    return G2



if __name__ == "__main__":
    #Ejecuta el primer grafo
    G = CreateGraph_1()
    Plot(G)
    PlotNode(G, "C")
    n = GetClosest(G, 15, 5)
    print(n.name)  # Debe ser J
    n = GetClosest(G, 8, 19)
    print(n.name)  # Debe ser B

    #Ejecuta el segundo grafo
    G1 = CreateGraph_2()
    Plot(G1)

    #Ejecuta el terer grafo
    G2 = CreateGraph_3()
    Plot(G2)
