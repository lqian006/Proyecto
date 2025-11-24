import matplotlib.pyplot as plt
from airport import *
from aircraft import *
import webbrowser
import os
from math import radians, sin, cos, sqrt, atan2
import platform
import subprocess

# Class BarcelonaAP will contain a code and a list of objects of class Terminal.
class BarcelonaAP ():
    def __init__(self,code):
        self.code = code
        self.terms = []

# Class Terminal will contain a name, a list of objects of class BoardingArea and a list with the ICAO codes of the airline companies which work in the terminal.
class Terminal ():
    def __init__(self, Names):
        self.Name= Names
        self.BoardingArea= []
        self.codes= []

# Class BoardingArea will contain a name, the type (Schengen/nonSchengen) and a list of objects of class Gate.
class BoardingArea():
    def __init__(self, Name, Type):
        self.name= Name
        self.type= Type
        self.gate= []

# Class Gate will contain a name, a boolean about gate occupancy, and the aircraft id in case the gate is occupied.
class Gate ():
    def __init__(self, name):
        self.name= name
        self.occupancy = False
        self.id= ''

if __name__ == "__main__":
    bcn = BarcelonaAP("LEBL")

def SetGates(area, init_gate, end_gate, prefix):
    if end_gate <= init_gate:
        return -1

    area.gate = []

    for num in range(init_gate, end_gate + 1):
        gate_name = f"{prefix}{num}"
        new_gate = Gate(gate_name)
        new_gate.occupancy = False
        new_gate.id = ""
        area.gate.append(new_gate)

    return 0  # éxito

def LoadAirlines(terminal, t_name):
    filename = f"{t_name}_Airlines.txt"

    if not os.path.isfile(filename):
        return -1  # error

    # leer el archivo
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except:
        return -1  #error

    terminal.codes = []

    for line in lines:
        clean = line.strip()
        if clean != "":
            terminal.codes.append(clean)

    return 0

def LoadAirportStructure(filename):

    if not os.path.isfile(filename):
        return -1

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]
    except:
        return -1

    # crear aeropuerto
    #código del aeropuerto
    if len(lines) == 0:
        return -1

    ap_code = lines[0]
    airport = BarcelonaAP(ap_code)

    i = 1
    prefix_counter = 1

    current_terminal = None

    while i < len(lines):
        line = lines[i]

        # Terminal
        if line.startswith("Terminal"):
            _, t_name = line.split(maxsplit=1)
            current_terminal = Terminal(t_name)
            airport.terms.append(current_terminal)
            i += 1
            continue

        # area de embarque
        if line.startswith("BoardingArea"):
            parts = line.split()
            # BoardingArea
            if len(parts) != 5:
                return -1

            _, ba_name, ba_type, g1, g2 = parts
            g1 = int(g1)
            g2 = int(g2)

            area = BoardingArea(ba_name, ba_type)

            prefix = f"A{prefix_counter}_"
            prefix_counter += 1

            # crear gates
            result = SetGates (area, g1, g2, prefix)
            if result != 0:
                return -1

            current_terminal.BoardingArea.append(area)

            i += 1
            continue

        if line.startswith("Airlines"):
            if LoadAirlines(current_terminal, current_terminal.Name) != 0:
                return -1
            i += 1
            continue

        i += 1

    return airport


