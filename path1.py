from node import Distance

class Path:
    def __init__(self, nodes, real_cost, estimated_cost):
        self.nodes = nodes  # Lista de objetos Node
        self.real_cost = real_cost  # Coste real acumulado
        self.estimated_cost = estimated_cost  # Estimación heurística hasta destino

    def total_cost(self):
        return self.real_cost + self.estimated_cost

# ------------------------
# FUNCIONES AUXILIARES
# ------------------------

def ContainsNode(path, node):
    """Devuelve True si el nodo ya está en el camino (evita bucles)"""
    return node in path.nodes

def AddNodeToPath(path, node, cost):
    """Crea un nuevo camino agregando un nodo al camino existente"""
    new_nodes = path.nodes + [node]
    new_real_cost = path.real_cost + cost
    return Path(new_nodes, new_real_cost, 0.0)  # El estimated_cost se actualiza aparte

def CostToNode(path, node):
    """Devuelve el coste real desde el origen hasta el nodo indicado"""
    if node not in path.nodes:
        return -1

    cost = 0.0
    for i in range(len(path.nodes) - 1):
        if path.nodes[i + 1] == node:
            cost += Distance(path.nodes[i], path.nodes[i + 1])
            break
        else:
            cost += Distance(path.nodes[i], path.nodes[i + 1])
    return cost

def PlotPath(graph, path):
    """Dibuja el camino sobre el grafo"""
    import matplotlib.pyplot as plt

    # Dibuja todos los nodos y segmentos
    graph.Plot()

    # Dibuja el camino en rojo
    for i in range(len(path.nodes) - 1):
        n1 = path.nodes[i]
        n2 = path.nodes[i + 1]
        plt.plot([n1.x, n2.x], [n1.y, n2.y], 'r-', linewidth=2)

    plt.title("Camino más corto")
    plt.show()