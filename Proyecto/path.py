from node import *
from graph import *

def ReadFileNode(filename):
    g = Graph()
    try:
        with open(filename, "r") as file:
            mode = None
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    if "NODE" in line.upper():
                        mode = "nodes"
                    continue
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    return g

def ReadFileSegment(filename):
    g = Graph()
    try:
        with open(filename, "r") as file:
            mode = None
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    if "SEGMENT" in line.upper():
                        mode = "segments"
                    continue
                if mode == "nodes":
                    parts = line.split()
                    if len(parts) != 3:
                        continue
                    name, x, y = parts
                    AddNode(g, Node(name, float(x), float(y)))
                elif mode == "segments":
                    parts = line.split()
                    if len(parts) != 3:
                        continue
                    seg_name, origin, dest = parts
                    AddSegment(g, seg_name, origin, dest)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    return g

def AddNodeToPath(Path, Node):

def ShortestPath():
    ReadFileNode()
    ReadFileSegment()
    n1=SEGMENT
    n2=NODE

lista=[]
len lista etc
if tal < tal1: tal 1


