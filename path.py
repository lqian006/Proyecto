import matplotlib.pyplot as plt
from Proyecto.node import Distance, Node
from Proyecto.graph import Graph


class Path:

    def __init__(self):
        self.nodes = []
        self.cost = 0.0

    def last_node(self):
        return self.nodes[-1] if self.nodes else None


def AddNodeToPath(path: Path, node: Node, cost: float) -> Path:
    path.nodes.append(node)
    path.cost += cost
    return path


def ContainsNode(path: Path, node: Node) -> bool:
    return node in path.nodes


def CostToNode(path: Path, node: Node) -> float:

    if node not in path.nodes:
        return -1.0
    total = 0.0
    for i in range(len(path.nodes) - 1):
        if path.nodes[i] == node:
            break
        total += Distance(path.nodes[i], path.nodes[i + 1])
    return total


def PlotPath(graph: Graph, path: Path):
    if not path.nodes:
        return

    path_set = set(path.nodes)
    path_edges = set()

    for i in range(len(path.nodes) - 1):
        node1 = path.nodes[i]
        node2 = path.nodes[i + 1]
        path_edges.add((node1, node2))
        path_edges.add((node2, node1))

    for seg in graph.segments:
        x0, y0 = seg.origin.x, seg.origin.y
        x1, y1 = seg.destination.x, seg.destination.y

        if (seg.origin, seg.destination) in path_edges or (seg.destination, seg.origin) in path_edges:
            plt.plot([x0, x1], [y0, y1], color='gray', linewidth=2, zorder=1)
            dx, dy = x1 - x0, y1 - y0
            plt.arrow(x0, y0, dx * 0.9, dy * 0.9,
                      length_includes_head=True,
                      head_width=0.2, head_length=0.3,
                      color='gray', zorder=1)
        else:
            plt.plot([x0, x1], [y0, y1], color='lightgray', zorder=0)

    # Dibujar nodos
    origin = path.nodes[0]
    for node in graph.nodes:
        if node == origin:
            plt.plot(node.x, node.y, 'bo', markersize=8, zorder=3)
        elif node in path_set:
            plt.plot(node.x, node.y, 'ko', markersize=6, zorder=3)
        else:
            plt.plot(node.x, node.y, 'o', color='lightgray', markersize=6, zorder=2)
        plt.text(node.x, node.y, node.name, fontsize=9, ha="right", va="bottom", zorder=4)

    plt.title(f"Camino: {'-'.join(n.name for n in path.nodes)}")
    plt.axis('equal')
    plt.grid(True)



#---Reachability---#

def FindReachableNodes(graph: Graph, origin_name: str) -> list:

    origin = next((n for n in graph.nodes if n.name == origin_name), None)
    if not origin:
        return []

    reachable = []
    current_paths = []

    start = Path()
    AddNodeToPath(start, origin, 0.0)
    current_paths.append(start)

    while current_paths:
        min_path = min(current_paths, key=lambda p: p.cost)
        current_paths.remove(min_path)
        last = min_path.last_node()

        for neigh in last.neighbors:
            if ContainsNode(min_path, neigh):
                continue
            new_path = Path()
            new_path.nodes = min_path.nodes.copy()
            new_path.cost = min_path.cost
            AddNodeToPath(new_path, neigh, Distance(last, neigh))
            current_paths.append(new_path)
            if neigh not in reachable:
                reachable.append(neigh)

    return reachable


def PlotReachable(graph: Graph, origin_name: str):
    reachable = FindReachableNodes(graph, origin_name)
    reachable_set = set(reachable)
    origin = next((n for n in graph.nodes if n.name == origin_name), None)

    for seg in graph.segments:
        x0, y0 = seg.origin.x, seg.origin.y
        x1, y1 = seg.destination.x, seg.destination.y
        if seg.origin == origin or seg.origin in reachable_set:
            seg_color = 'gray'
            arrow = True
        else:
            seg_color = 'ko'
            arrow = False
        plt.plot([x0, x1], [y0, y1], seg_color)
        if arrow:
            dx, dy = x1 - x0, y1 - y0
            plt.arrow(x0, y0, dx * 0.9, dy * 0.9,
                      length_includes_head=True,
                      head_width=0.2, head_length=0.3,
                      color=seg_color)
    for n in graph.nodes:
        if n == origin:
            plt.plot(n.x, n.y, 'bo', markersize=8)
        elif n in reachable_set:
            plt.plot(n.x, n.y, 'ko', markersize=6)
        else:
            plt.plot(n.x, n.y, 'gray', markersize=6)
        plt.text(n.x, n.y, n.name, fontsize=9, ha="right", va="bottom")

    plt.title(f"Nodos alcanzables desde {origin_name}")
    plt.axis('equal')
    plt.grid(True)

    return [n.name for n in reachable]


#---Camino más corto---#

def FindShortestPath(graph: Graph, origin_name: str, dest_name: str) -> Path:

    origin = next((n for n in graph.nodes if n.name == origin_name), None)
    destination = next((n for n in graph.nodes if n.name == dest_name), None)
    if not origin or not destination:
        return None

    open_paths = []
    closed_paths = []

    start = Path()
    AddNodeToPath(start, origin, 0.0)
    open_paths.append(start)

    def heuristic(path):
        return path.cost + Distance(path.last_node(), destination)

    while open_paths:
        current = min(open_paths, key=heuristic)
        open_paths.remove(current)

        if current.last_node() == destination:
            return current

        closed_paths.append(current)

        for neigh in current.last_node().neighbors:
            if ContainsNode(current, neigh):
                continue

            new_path = Path()
            new_path.nodes = current.nodes.copy()
            new_path.cost = current.cost
            AddNodeToPath(new_path, neigh, Distance(current.last_node(), neigh))

            skip = False
            for p in open_paths + closed_paths:
                if p.last_node() == neigh and heuristic(p) <= heuristic(new_path):
                    skip = True
                    break

            if not skip:
                open_paths = [p for p in open_paths if
                              not (p.last_node() == neigh and heuristic(p) > heuristic(new_path))]
                open_paths.append(new_path)

    return None


def PlotShortestPath(graph: Graph, origin_name: str, dest_name: str):
    path = FindShortestPath(graph, origin_name, dest_name)
    if path:
        PlotPath(graph, path)
        return [n.name for n in path.nodes]
    else:
        print(f"No hay camino de {origin_name} a {dest_name}.")
        return None
