import math

class Node:
    def __init__(self, name: str, x: float, y: float):
        self.name = name
        self.x = x
        self.y = y
        self.neighbors = []

def AddNeighbor(n1, n2):
    if n2 in n1.neighbors:
        return False
    else:
        n1.neighbors.append(n2)
        return True
def Distance(n1, n2):
    return math.sqrt((n2.x - n1.x) ** 2 + (n2.y - n1.y) ** 2)

