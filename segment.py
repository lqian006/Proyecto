from Proyecto import node

class Segment:
    def __init__(self, name: str, origin: node, destination: node):
        self.name=name
        self.origin= origin
        self.destination = destination
        self.cost = node.Distance(origin, destination)

