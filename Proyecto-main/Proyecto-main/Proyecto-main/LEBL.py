"""
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


def GateOccupancy (bcn):
    result=[]
    for terminal in bcn.terms:
        for area in terminal.BoardingArea:
            for gate in area.gate:
                if gate.occupancy==False:
                    status='free'
                else:
                    status='occupied'

                if status=='occupied':
                    aircraft_id = gate.id
                else:
                    aircraft_id=None

                result.append((gate.name,status,aircraft_id))

    return result


def IsAirlineInTerminal(terminal, name):
    if not name or name.strip() == "":
        return False
    
    if len(terminal.codes) == 0:
        return False
    
    return name in terminal.codes


def SearchTerminal(bcn, name):
    for terminal in bcn.terms:
        if IsAirlineInTerminal(terminal, name):
            return terminal.Name
    
    return ""


def AssignGate(bcn, aircraft):
    terminal_name = SearchTerminal(bcn, aircraft.AirlineCompany)
    
    if terminal_name == "":
        return -1
    
    terminal = None
    for t in bcn.terms:
        if t.Name == terminal_name:
            terminal = t
            break
    
    if terminal is None:
        return -1
    
    is_schengen = IsSchengenAirport(aircraft.OriginAirport)
    flight_type = "Schengen" if is_schengen else "non-Schengen"
    
    for area in terminal.BoardingArea:
        if area.type == flight_type:
            for gate in area.gate:
                if not gate.occupancy:
                    gate.occupancy = True
                    gate.id = aircraft.id
                    return 0
    
    return -1

"""
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

    return 0


def LoadAirlines(terminal, t_name):
    filename = f"{t_name}_Airlines.txt"

    if not os.path.isfile(filename):
        return -1

    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except:
        return -1

    terminal.codes = []

    for line in lines:
        clean = line.strip()
        if clean != "":
            
            if '\t' in clean:
                parts = clean.split('\t')
                if len(parts) >= 2:
                    code = parts[1].strip()
                    terminal.codes.append(code)
            else:
                
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

    if len(lines) == 0:
        return -1

    # Primera linea: codigo del aeropuerto
    ap_code = lines[0].split()[0]
    airport = BarcelonaAP(ap_code)

    current_terminal = None
    prefix_counter = 1
    i = 1

    while i < len(lines):
        line = lines[i]

        if line == "":
            i += 1
            continue

        if line.startswith("Terminal"):
            parts = line.split()
            if len(parts) >= 2:
                t_name = parts[1]
                current_terminal = Terminal(t_name)
                airport.terms.append(current_terminal)
            i += 1
            continue

        if line.startswith("Area"):
            if current_terminal is None:
                return -1

            parts = line.split()
            if len(parts) < 6:
                return -1

            ba_name = parts[1]
            ba_type = parts[2]
            
            try:
                gate_start = int(parts[-3])
                gate_end = int(parts[-1])
            except ValueError:
                return -1

            area = BoardingArea(ba_name, ba_type)

            prefix = f"{ba_name}{prefix_counter}_"
            prefix_counter += 1

            if SetGates(area, gate_start, gate_end, prefix) != 0:
                return -1

            current_terminal.BoardingArea.append(area)
            i += 1
            continue

        if line.startswith("BoardingArea"):
            if current_terminal is None:
                return -1

            parts = line.split()
            if len(parts) != 5:
                return -1

            ba_name = parts[1]
            ba_type = parts[2]
            gate_start = int(parts[3])
            gate_end = int(parts[4])

            area = BoardingArea(ba_name, ba_type)

            prefix = f"A{prefix_counter}_"
            prefix_counter += 1

            if SetGates(area, gate_start, gate_end, prefix) != 0:
                return -1

            current_terminal.BoardingArea.append(area)
            i += 1
            continue

        if line.startswith("Airlines"):
            if current_terminal is not None:
                LoadAirlines(current_terminal, current_terminal.Name)
            i += 1
            continue

        i += 1

    for terminal in airport.terms:
        LoadAirlines(terminal, terminal.Name)

    return airport

def GateOccupancy(bcn):

    result = []
    for terminal in bcn.terms:
        for area in terminal.BoardingArea:
            for gate in area.gate:
                if gate.occupancy == False:
                    status = 'Free'      # English
                else:
                    status = 'Occupied'  # English

                if status == 'Occupied':
                    aircraft_id = gate.id
                else:
                    aircraft_id = None

                result.append((gate.name, status, aircraft_id))

    return result


def IsAirlineInTerminal(terminal, name):
    if not name or name.strip() == "":
        return False
    
    if len(terminal.codes) == 0:
        return False
    
    return name in terminal.codes


def SearchTerminal(bcn, name):
    for terminal in bcn.terms:
        if IsAirlineInTerminal(terminal, name):
            return terminal.Name
    
    return ""


def AssignGate(bcn, aircraft):
    terminal_name = SearchTerminal(bcn, aircraft.AirlineCompany)
    
    if terminal_name == "":
        return -1
    
    terminal = None
    for t in bcn.terms:
        if t.Name == terminal_name:
            terminal = t
            break
    
    if terminal is None:
        return -1
    
    is_schengen = IsSchengenAirport(aircraft.OriginAirport)
    flight_type = "Schengen" if is_schengen else "non-Schengen"
    
    for area in terminal.BoardingArea:
        if area.type == flight_type:
            for gate in area.gate:
                if not gate.occupancy:
                    gate.occupancy = True
                    gate.id = aircraft.id
                    return 0
    
    return -1

