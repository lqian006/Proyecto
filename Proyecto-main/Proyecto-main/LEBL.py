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
    """
    Carga la estructura de un aeropuerto desde un archivo de texto.
    Devuelve un objeto BarcelonaAP con terminales, áreas de embarque y gates.
    """

    if not os.path.isfile(filename):
        print("Archivo no encontrado:", filename)
        return -1

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f.readlines()]
    except Exception as e:
        print("Error leyendo el archivo:", e)
        return -1

    if len(lines) == 0:
        print("Archivo vacío")
        return -1

    # Primera línea -> código del aeropuerto
    ap_code = lines[0].split()[0]
    airport = BarcelonaAP(ap_code)

    current_terminal = None
    prefix_counter = 1

    i = 1
    while i < len(lines):
        line = lines[i].lstrip()  # Quita espacios al inicio

        # Ignorar líneas vacías
        if line == "":
            i += 1
            continue

        # ----- Terminal -----
        if line.startswith("Terminal"):
            parts = line.split()
            if len(parts) < 2:
                print("Formato incorrecto de Terminal en línea:", line)
                return -1

            t_name = parts[1]
            current_terminal = Terminal(t_name)
            airport.terms.append(current_terminal)
            # print(f"Terminal creada: {t_name}")
            i += 1
            continue

        # ----- Area de embarque -----
        if line.startswith("Area"):
            if current_terminal is None:
                print("Área encontrada antes de cualquier terminal:", line)
                return -1

            parts = line.split()
            if len(parts) < 6:
                print("Formato incorrecto de Área en línea:", line)
                return -1

            ba_name = parts[1]
            ba_type = parts[2]

            # Extraer números de gates (después de 'Gates')
            try:
                gate_start = int(parts[-3])
                gate_end = int(parts[-1])
            except ValueError:
                print("Error al convertir números de gates en línea:", line)
                return -1

            area = BoardingArea(ba_name, ba_type)

            prefix = f"A{prefix_counter}_"
            prefix_counter += 1

            if SetGates(area, gate_start, gate_end, prefix) != 0:
                print("Error al crear gates para área:", ba_name)
                return -1

            current_terminal.BoardingArea.append(area)
            # print(f"Área creada: {ba_name} ({ba_type}) Gates: {gate_start}-{gate_end}")
            i += 1
            continue

        # Si la línea no coincide con Terminal o Area, la ignoramos
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

