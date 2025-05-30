import matplotlib.pyplot as plt
from Proyecto.node import *
from segment import *


class Graph:
    def __init__(self):
        self.nodes = []
        self.segments = []


def AddNode(g,n):
    for node in g.nodes:
        if node.name == n.name:
            return False
    g.nodes.append(n)
    return True


def AddSegment(g, name, nameOriginNode, nameDestinationNode):
    origin = next((n for n in g.nodes if n.name == nameOriginNode), None)
    destination = next((n for n in g.nodes if n.name == nameDestinationNode), None)

    if origin is None or destination is None:
        return False

    for seg in g.segments:
        if (seg.origin == origin and seg.destination == destination) or \
           (seg.origin == destination and seg.destination == origin):
            return False

    seg = Segment(name, origin, destination)
    g.segments.append(seg)

    AddNeighbor(origin, destination)
    AddNeighbor(destination, origin)

    return True


def GetClosest(g,x,y):
    mas_cercano=None
    dist_corta=None

    for node in g.nodes:
        dx=node.x-x
        dy=node.y-y
        distancia=(dx**2+dy**2)**0.5

        if dist_corta== None or distancia < dist_corta:
            dist_corta=distancia
            mas_cercano=node

    return mas_cercano


def Plot(g):

    for segment in g.segments:
        x_values = [segment.origin.x, segment.destination.x]
        y_values = [segment.origin.y, segment.destination.y]
        plt.plot(x_values, y_values, 'k-')
        mid_x = (segment.origin.x + segment.destination.x)/2
        mid_y = (segment.origin.y + segment.destination.y)/2
        plt.text(mid_x, mid_y, f"{segment.cost:.1f}", color = "black", fontsize = 8, ha = "center")

    for node in g.nodes:
        plt.plot(node.x, node.y, 'ko')
        plt.text(node.x, node.y, node.name, fontsize = 9, ha = "right", va = "bottom")

    plt.title("Graph")
    plt.axis("equal")
    plt.grid(True)


def PlotNode(g, nameOrigin):
    origin = next((n for n in g.nodes if n.name == nameOrigin), None)
    if origin is None:
        return False

    for segment in g.segments:

        if (segment.origin == origin and segment.destination in origin.neighbors) or \
                (segment.destination == origin and segment.origin in origin.neighbors):
            color = "r"
        else:
            color = "k"

        x_values = [segment.origin.x, segment.destination.x]
        y_values = [segment.origin.y, segment.destination.y]
        plt.plot(x_values, y_values, color)

        mid_x = (segment.origin.x + segment.destination.x) / 2
        mid_y = (segment.origin.y + segment.destination.y) / 2
        plt.text(mid_x, mid_y, f"{segment.cost:.1f}", color="black", fontsize=8, ha="center")

    for node in g.nodes:
        if node == origin:
            plt.plot(node.x, node.y, "bo")
        elif node in origin.neighbors:
            plt.plot(node.x, node.y, "go")
        else:
            plt.plot(node.x, node.y, "ko")

        plt.text(node.x, node.y, node.name, fontsize=9, ha="right", va="bottom")

    plt.title(f"Vecinos del nodo {origin.name}")
    plt.axis("equal")
    plt.grid(True)


def LoadGraphFromFile(filename):
    grafo = Graph()
    try:
        with open(filename, "r") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea == "":
                    continue

                partes = linea.split()
                tipo = partes[0]

                # Nodo: 4 campos
                if tipo == "NODE" and len(partes) == 4:
                    nombre_nodo = partes[1]
                    x_str = partes[2]
                    y_str = partes[3]
                    nodo = Node(nombre_nodo, float(x_str), float(y_str))
                    AddNode(grafo, nodo)

                elif tipo == "SEGMENT" and len(partes) == 4:
                    nombre_seg = partes[1]
                    origen = partes[2]
                    destino = partes[3]
                    AddSegment(grafo, nombre_seg, origen, destino)

    except FileNotFoundError:
        print(f"Error: no existe el fichero '{filename}'")
        return None

    return grafo


def DeleteNode(g, name):
    node = next((n for n in g.nodes if n.name == name), None)
    if not node:
        return False
    g.nodes.remove(node)
    g.segments = [s for s in g.segments if s.origin != node and s.destination != node]
    return True


def SaveGraphToFile(g, filename):
    with open(filename, 'w') as f:
        for node in g.nodes:
            f.write(f"NODE {node.name} {node.x} {node.y}\n")
        for seg in g.segments:
            f.write(f"SEGMENT {seg.name} {seg.origin.name} {seg.destination.name}\n")

