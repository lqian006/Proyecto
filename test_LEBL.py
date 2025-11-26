import matplotlib.pyplot as plt
from airport import *
from aircraft import *
import webbrowser
import os
from math import radians, sin, cos, sqrt, atan2
import platform
import subprocess
from LEBL import *

print("="*60)
print("TESTING LEBL.PY - VERSION 3")
print("="*60)

# Test 1 - SetGates
print("\nTest 1 - SetGates:")

area = BoardingArea("A", "Schengen")
result = SetGates(area, 1, 5, "A_")

if result != 0:
    print("ERROR: SetGates failed")
else:
    if len(area.gate) != 5:
        print("ERROR: incorrect number of gates")
    else:
        expected_names = ["A_1", "A_2", "A_3", "A_4", "A_5"]
        real_names = [g.name for g in area.gate]

        if real_names != expected_names:
            print("ERROR: gate names do not match")
        else:
            print("PASS: SetGates works correctly")


# Test 2 - LoadAirlines
print("\nTest 2 - LoadAirlines:")

with open("TEST_Airlines.txt", "w") as f:
    f.write("IBE\n")
    f.write("VLG\n")
    f.write("RYR\n")

terminal = Terminal("TEST")
res = LoadAirlines(terminal, "TEST")

if res != 0:
    print("ERROR: Could not load airlines")
else:
    if terminal.codes == ["IBE", "VLG", "RYR"]:
        print("PASS: LoadAirlines works correctly")
    else:
        print("ERROR: airline list does not match")
        print("  Expected: ['IBE', 'VLG', 'RYR']")
        print("  Got:", terminal.codes)

os.remove("TEST_Airlines.txt")


# Test 3 - LoadAirportStructure
print("\nTest 3 - LoadAirportStructure:")

with open("LEBL_test.txt", "w") as f:
    f.write("LEBL\n")
    f.write("Terminal TX\n")  # Cambio: TX en lugar de T1
    f.write("BoardingArea A Schengen 1 3\n")
    f.write("Airlines\n")

with open("TX_Airlines.txt", "w") as f:  # Cambio: TX_Airlines.txt
    f.write("IBE\n")
    f.write("VLG\n")

airport = LoadAirportStructure("LEBL_test.txt")

if airport == -1:
    print("ERROR: could not load airport")
else:
    ok = True

    if airport.code != "LEBL":
        print("ERROR: incorrect airport code")
        ok = False

    if len(airport.terms) != 1:
        print("ERROR: incorrect number of terminals")
        ok = False

    if ok:
        t1 = airport.terms[0]
        if t1.Name != "TX":  # Cambio: TX
            print("ERROR: incorrect terminal name")
            ok = False

        if len(t1.BoardingArea) != 1:
            print("ERROR: incorrect number of boarding areas")
            ok = False

        if ok:
            area = t1.BoardingArea[0]
            if area.name != "A" or area.type != "Schengen":
                print("ERROR: incorrect area data")
                ok = False

            if len(area.gate) != 3:
                print("ERROR: incorrect number of gates")
                ok = False

            expected_gates = ["A1_1", "A1_2", "A1_3"]
            real_gates = [g.name for g in area.gate]

            if real_gates != expected_gates:
                print("ERROR: incorrect gate names")
                print("  Expected:", expected_gates)
                print("  Got:", real_gates)
                ok = False

            if t1.codes != ["IBE", "VLG"]:
                print("ERROR: airlines not loaded correctly")
                print("  Expected: ['IBE', 'VLG']")
                print("  Got:", t1.codes)
                ok = False

    if ok:
        print("PASS: LoadAirportStructure works correctly")

os.remove("LEBL_test.txt")
os.remove("TX_Airlines.txt")  # Cambio: TX_Airlines.txt


# Test 4 - GateOccupancy

print("\nTest 4 - GateOccupancy:")
bcn = LoadAirportStructure("Terminals.txt")
if bcn != -1:
    info = GateOccupancy(bcn)
    occupied = sum(1 for g in info if g[1] == 'Occupied')  
    free = sum(1 for g in info if g[1] == 'Free')          
    print(f"PASS: Total gates: {len(info)}, Occupied: {occupied}, Free: {free}")
else:
    print("ERROR: Could not load Terminals.txt")




# Test 5 - IsAirlineInTerminal
print("\nTest 5 - IsAirlineInTerminal:")

terminal = Terminal("T1")
terminal.codes = ["VLG", "IBE", "KLM"]

result1 = IsAirlineInTerminal(terminal, "VLG")
result2 = IsAirlineInTerminal(terminal, "RYR")

if result1 == True and result2 == False:
    print("PASS: IsAirlineInTerminal works correctly")
else:
    print("ERROR: IsAirlineInTerminal failed")


# Test 6 - SearchTerminal
print("\nTest 6 - SearchTerminal:")

with open("LEBL_test6.txt", "w") as f:
    f.write("LEBL\n")
    f.write("Terminal TA\n")  # Cambio: TA en lugar de T1
    f.write("Area A Schengen Gates 1 - 3\n")
    f.write("Terminal TB\n")  # Cambio: TB en lugar de T2
    f.write("Area M Schengen Gates 1 - 3\n")

with open("TA_Airlines.txt", "w") as f:  # Cambio: TA
    f.write("Vueling\tVLG\n")

with open("TB_Airlines.txt", "w") as f:  # Cambio: TB
    f.write("Ryanair\tRYR\n")

bcn = LoadAirportStructure("LEBL_test6.txt")

if bcn == -1:
    print("ERROR: could not load airport")
else:
    terminal1 = SearchTerminal(bcn, "VLG")
    terminal2 = SearchTerminal(bcn, "RYR")
    
    if terminal1 == "TA" and terminal2 == "TB":  # Cambio: TA, TB
        print("PASS: SearchTerminal works correctly")
    else:
        print("ERROR: SearchTerminal failed")
        print("  VLG expected: TA, got:", terminal1)
        print("  RYR expected: TB, got:", terminal2)

os.remove("LEBL_test6.txt")
os.remove("TA_Airlines.txt")  # Cambio: TA
os.remove("TB_Airlines.txt")  # Cambio: TB


# Test 7 - AssignGate
print("\nTest 7 - AssignGate:")

with open("LEBL_test7.txt", "w") as f:
    f.write("LEBL\n")
    f.write("Terminal TC\n")  # Cambio: TC
    f.write("Area A Schengen Gates 1 - 5\n")
    f.write("Area D non-Schengen Gates 1 - 5\n")

with open("TC_Airlines.txt", "w") as f:  # Cambio: TC
    f.write("Vueling\tVLG\n")

bcn = LoadAirportStructure("LEBL_test7.txt")

if bcn == -1:
    print("ERROR: could not load airport")
else:
    aircraft1 = Aircraft("ECMKV", "LYBE", "00:04", "VLG")
    result1 = AssignGate(bcn, aircraft1)
    
    aircraft2 = Aircraft("ECJGM", "EGCC", "00:05", "VLG")
    result2 = AssignGate(bcn, aircraft2)
    
    if result1 == 0 and result2 == 0:
        print("PASS: AssignGate works correctly")
    else:
        print("ERROR: AssignGate failed")
        print("  Schengen flight result:", result1, "(expected: 0)")
        print("  non-Schengen flight result:", result2, "(expected: 0)")

os.remove("LEBL_test7.txt")
os.remove("TC_Airlines.txt")  # Cambio: TC


print("\n" + "="*60)
print("ALL TESTS COMPLETED")
print("="*60)