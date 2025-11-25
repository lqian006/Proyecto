import matplotlib.pyplot as plt
from airport import *
from aircraft import *
import webbrowser
import os
from math import radians, sin, cos, sqrt, atan2
import platform
import subprocess
from LEBL import *

# Test 1 — SetGates
print("\nTest SetGates:")

area = BoardingArea("A", "Schengen")
result = SetGates(area, 1, 5, "A_")

if result != 0:
    print("SetGates error")
else:
    if len(area.gate) != 5:
        print("número incorrecto de gates")
    else:
        expected_names = ["A_1", "A_2", "A_3", "A_4", "A_5"]
        real_names = [g.name for g in area.gate]

        if real_names != expected_names:
            print("los nombres de gates no coinciden")
        else:
            print("Gates setted")


# Test 2 — LoadAirlines

print("\nTest LoadAirLines:")
with open("T1_Airlines.txt", "w") as f:
    f.write("IBE\n")
    f.write("VLG\n")
    f.write("RYR\n")

terminal = Terminal("T1")

res = LoadAirlines(terminal, "T1")

if res != 0:
    print("Error")
else:
    if terminal.codes == ["IBE", "VLG", "RYR"]:
        print("LoadAirlines ha corrido")
    else:
        print("la lista de aerolíneas no coincide")

#os.remove("T1_Airlines.txt")

# Test 3 — LoadAirportStructure
'''print("\nTest LoadAirportStructure:")

with open("LEBL.txt", "w") as f:
    f.write("LEBL\n")
    f.write("Terminal T1\n")
    f.write("BoardingArea A Schengen 1 3\n")
    f.write("Airlines\n")

with open("T1_Airlines.txt", "w") as f:
    f.write("IBE\n")
    f.write("VLG\n")

airport = LoadAirportStructure("LEBL.txt")

if airport == -1:
    print("error")
else:
    ok = True

    if airport.code != "LEBL":
        print("Código de aeropuerto incorrecto")
        ok = False

    if len(airport.terms) != 1:
        print("Número incorrecto de terminales")
        ok = False

    t1 = airport.terms[0]
    if t1.Name != "T1":
        print("Nombre de terminal incorrecto")
        ok = False

    if len(t1.BoardingArea) != 1:
        print("Número incorrecto de boarding areas")
        ok = False

    area = t1.BoardingArea[0]
    if area.name != "A" or area.type != "Schengen":
        print("Datos incorrectos del área")
        ok = False

    if len(area.gate) != 3:
        print("Número incorrecto de gates")
        ok = False

    expected_gates = ["A1_1", "A1_2", "A1_3"]
    real_gates = [g.name for g in area.gate]

    if real_gates != expected_gates:
        print("Nombres de gates incorrectos")
        ok = False

    if t1.codes != ["IBE", "VLG"]:
        print("Aerolíneas cargadas incorrectamente")
        ok = False

    if ok:
        print("LoadAirportStructure se ha corrido")

os.remove("LEBL.txt")
#os.remove("T1_Airlines.txt")'''

bcn = LoadAirportStructure("Terminals.txt")

if isinstance(bcn, BarcelonaAP):
    print("Aeropuerto cargado correctamente:", bcn.code)
    for t in bcn.terms:
        print("Terminal:", t.Name, "Áreas:", len(t.BoardingArea))
        for a in t.BoardingArea:
            print("  Área:", a.name, "-", a.type, "Gates:", len(a.gate))
else:
    print("Error cargando aeropuerto")



# Test 4 - GateOccupancy
bcn = LoadAirportStructure("Terminals.txt")
info = GateOccupancy(bcn)
for name, status, aircraft in info:
    print(name, status, aircraft)

