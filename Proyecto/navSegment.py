import math
class NavSegment:
    def __init__(self, OriginNumber, DestinationNumber, Distance):
        self.OriginNumber = OriginNumber
        self.DestinationNumber = DestinationNumber
        self.Distance = Distance

def Distance(OriginNumber, DestinationNumber):
    return math.sqrt((DestinationNumber.x - OriginNumber.x) ** 2 + (DestinationNumber.y - OriginNumber.y) ** 2)

class Node:
    def __init__(self, name: str, x: float, y: float):
        self.name = name
        self.x = x
        self.y = y
        self.neighbors = []
