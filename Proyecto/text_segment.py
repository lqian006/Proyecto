from node import *
from segment import *

n1 = Node("A", 0, 0)
n2 = Node("B", 3, 4)
n3 = Node("C", 6, 8)

segment1 = Segment("Segment1", n1, n2)
segment2 = Segment("Segment2", n2, n3)

print(f"{segment1.name}: Origin = {segment1.origin.name}, Destination = {segment1.destination.name}, Cost = {segment1.cost}")
print(f"{segment2.name}: Origin = {segment2.origin.name}, Destination = {segment2.destination.name}, Cost = {segment2.cost}")