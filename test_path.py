from node import Node, Distance
from path1 import *


# Función auxiliar para crear un grafo de ejemplo
def create_sample_graph():
    A = Node("A", 0, 0)
    B = Node("B", 3, 0)
    C = Node("C", 3, 4)
    D = Node("D", 6, 0)
    E = Node("E", 6, 4)

    A.neighbors = [B, C]
    B.neighbors = [A, D]
    C.neighbors = [A, E]
    D.neighbors = [B, E]
    E.neighbors = [C, D]

    nodes = [A, B, C, D, E]
    return nodes, A, B, C, D, E


def test_add_node_to_path():
    _, A, B, C, _, _ = create_sample_graph()
    path = Path()
    AddNodeToPath(path, A)
    AddNodeToPath(path, B)
    AddNodeToPath(path, C)

    assert path.nodes == [A, B, C]
    assert abs(path.real_cost - 7.0) < 1e-6


def test_contains_node():
    _, A, B, C, _, _ = create_sample_graph()
    path = Path()
    AddNodeToPath(path, A)
    AddNodeToPath(path, B)

    assert ContainsNode(path, A)
    assert ContainsNode(path, B)
    assert not ContainsNode(path, C)


def test_cost_to_node():
    _, A, B, C, _, _ = create_sample_graph()
    path = Path()
    AddNodeToPath(path, A)
    AddNodeToPath(path, B)
    AddNodeToPath(path, C)

    expected_cost = Distance(A, B) + Distance(B, C)
    assert abs(CostToNode(path, C) - expected_cost) < 1e-6
    assert CostToNode(path, Node("X", 0, 0)) == -1


def test_reachability():
    nodes, A, _, _, _, _ = create_sample_graph()
    reachable = reachability(A)

    # All nodes should be reachable from A in this graph
    for node in nodes:
        assert node in reachable


def test_find_shortest_path():
    graph, A, B, C, D, F = create_sample_graph()
    path = FindShortestPath(graph, A, F)

    assert path is not None
    assert path.nodes[0].name == "A"
    assert path.nodes[-1].name == "F"
    assert "F" in [n.name for n in path.nodes]
    assert path.real_cost > 0


# Ejecutar todos los tests
if __name__ == "__main__":
    test_add_node_to_path()
    print("test_add_node_to_path passed.")

    test_contains_node()
    print("test_contains_node passed.")

    test_cost_to_node()
    print("test_cost_to_node passed.")

    test_reachability()
    print("test_reachability passed.")

    test_find_shortest_path()
    print("test_find_shortest_path passed.")
