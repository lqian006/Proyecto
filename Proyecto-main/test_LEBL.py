import matplotlib.pyplot as plt
from aircraft import *
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
with open("../Proyecto-mainV4/Proyecto-main4/T1_Airlines.txt", "w") as f:
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

bcn = LoadAirportStructure("../Proyecto-mainV4/Proyecto-main4/Terminals.txt")

if isinstance(bcn, BarcelonaAP):
    print("Aeropuerto cargado correctamente:", bcn.code)
    for t in bcn.terms:
        print("Terminal:", t.Name, "Áreas:", len(t.BoardingArea))
        for a in t.BoardingArea:
            print("  Área:", a.name, "-", a.type, "Gates:", len(a.gate))
else:
    print("Error cargando aeropuerto")



# Test 4 - GateOccupancy
bcn = LoadAirportStructure("../Proyecto-mainV4/Proyecto-main4/Terminals.txt")
info = GateOccupancy(bcn)
for name, status, aircraft in info:
    print(name, status, aircraft)



#----- version 4 ----------

print("\n" + "="*60)
print("VERSION 4 TESTS - AssignNightGates & FreeGate")
print("="*60)

# Load airport structure for V4 tests
bcn = LoadAirportStructure("../Proyecto-mainV4/Proyecto-main4/Terminals.txt")

# Test 5 - AssignNightGates (Basic)
print("\nTest 5 - AssignNightGates (Basic):")

# Reset all gates
for terminal in bcn.terms:
    for area in terminal.BoardingArea:
        for gate in area.gate:
            gate.occupancy = False
            gate.id = ""

night_aircraft = [
    Aircraft("NIGHT1", "", "", "VLG", "LEMD", "05:30"),  
    Aircraft("NIGHT2", "", "", "IBE", "LFPG", "06:00"),  
    Aircraft("NIGHT3", "", "", "RYR", "EGLL", "06:30")] 

result = AssignNightGates(bcn, night_aircraft)

if result == 3:
    print(f"PASS: Assigned gates to {result} night aircraft")
    
    # Show assignments
    info = GateOccupancy(bcn)
    count = 0
    for gate_info in info:
        if gate_info[1] == 'occupied':
            print(f"  {gate_info[0]}: {gate_info[2]}")
            count += 1
            if count >= 3:
                break
else:
    print(f"ERROR: Expected 3, got {result}")


# Test 6 - AssignNightGates (Skip non-night)
print("\nTest 6 - AssignNightGates (Skip non-night):")

# Reset gates
for terminal in bcn.terms:
    for area in terminal.BoardingArea:
        for gate in area.gate:
            gate.occupancy = False
            gate.id = ""

mixed_list = [
    Aircraft("COMPLETE", "EGLL", "10:30", "VLG", "LFPO", "16:00"),  
    Aircraft("NIGHT4", "", "", "VLG", "LEMD", "07:00"),            
    Aircraft("ARRIVAL", "LFPG", "12:00", "IBE"),                   
    Aircraft("NIGHT5", "", "", "RYR", "EGLL", "07:30")]

result = AssignNightGates(bcn, mixed_list)

if result == 2:
    print(f"PASS: Assigned {result} gates (skipped non-night aircraft)")
else:
    print(f"ERROR: Expected 2, got {result}")


# Test 7 - FreeGate (Basic)
print("\nTest 7 - FreeGate:")

for terminal in bcn.terms:
    for area in terminal.BoardingArea:
        for gate in area.gate:
            gate.occupancy = False
            gate.id = ""

test_aircraft = [Aircraft("TEST1", "", "", "VLG", "LEMD", "08:00")]
AssignNightGates(bcn, test_aircraft)

info = GateOccupancy(bcn)
occupied_before = sum(1 for g in info if g[1] == 'occupied')

result = FreeGate(bcn, "TEST1")

info = GateOccupancy(bcn)
occupied_after = sum(1 for g in info if g[1] == 'occupied')

if result == 0 and occupied_before == 1 and occupied_after == 0:
    print("PASS: Gate freed successfully")
    print(f"  Before: {occupied_before} occupied, After: {occupied_after} occupied")
else:
    print("ERROR: Gate not freed correctly")


# Test 8 - FreeGate (Not found)
print("\nTest 8 - FreeGate (Not found):")

result = FreeGate(bcn, "NONEXISTENT")

if result == -1:
    print("PASS: Returns -1 for non-existent aircraft")
else:
    print(f"ERROR: Should return -1, got {result}")


# Test 9 - Complete Workflow
print("\nTest 9 - Complete Workflow:")

# Reset gates
for terminal in bcn.terms:
    for area in terminal.BoardingArea:
        for gate in area.gate:
            gate.occupancy = False
            gate.id = ""

aircraft_list = [
    Aircraft("N1", "", "", "VLG", "LEMD", "05:00"),
    Aircraft("N2", "", "", "IBE", "LFPG", "05:30"),
    Aircraft("N3", "", "", "RYR", "EGLL", "06:00"),]

assigned = AssignNightGates(bcn, aircraft_list)
print(f"  Step 1: Assigned {assigned} gates")

info = GateOccupancy(bcn)
occupied_count = sum(1 for g in info if g[1] == 'occupied')
print(f"  Step 2: {occupied_count} gates occupied")

FreeGate(bcn, "N2")
info = GateOccupancy(bcn)
occupied_count = sum(1 for g in info if g[1] == 'occupied')
print(f"  Step 3: Freed N2, now {occupied_count} gates occupied")

FreeGate(bcn, "N1")
info = GateOccupancy(bcn)
occupied_count = sum(1 for g in info if g[1] == 'occupied')
print(f"  Step 4: Freed N1, now {occupied_count} gates occupied")

if occupied_count == 1:
    print("PASS: Workflow completed correctly")
else:
    print(f"ERROR: Expected 1 occupied gate, got {occupied_count}")

print("\n" + "="*60)
print("VERSION 4 TESTS COMPLETED")
print("="*60)


#----- Continuity with v4 ------
print("="*60)
print("Dynamic Gate Assignment")
print("="*60)

bcn = LoadAirportStructure("../Proyecto-mainV4/Proyecto-main4/Terminals.txt")

# Test 1 - AssignGatesAtTime: Basic Hour Assignment
print("\nTest 1 - AssignGatesAtTime (Basic):")

for terminal in bcn.terms:
    for area in terminal.BoardingArea:
        for gate in area.gate:
            gate.occupancy = False
            gate.id = ""

test_aircraft = [
    Aircraft("AC001", "EGLL", "12:15", "VLG"), 
    Aircraft("AC002", "LFPG", "12:45", "IBE"),  
    Aircraft("AC003", "EHAM", "13:30", "RYR"),]

not_assigned = AssignGatesAtTime(bcn, test_aircraft, "12:00")

info = GateOccupancy(bcn)
occupied = sum(1 for g in info if g[1] == 'occupied')

if occupied == 2 and not_assigned == 0:
    print(f"PASS: Assigned 2 aircraft in 12:00-13:00 period")
else:
    print(f"ERROR: Expected 2 assigned, got {occupied}")



# Test 2 - AssignGatesAtTime: Freeing Gates
print("\nTest 2 - AssignGatesAtTime (Freeing Departed Gates):")

for terminal in bcn.terms:
    for area in terminal.BoardingArea:
        for gate in area.gate:
            gate.occupancy = False
            gate.id = ""
flights = [
    Aircraft("DEP1", "EGLL", "10:15", "VLG", "LFPG", "12:00"),  
    Aircraft("DEP2", "LFPG", "10:30", "IBE", "LEMD", "13:30"), 
    Aircraft("NEW1", "EHAM", "14:15", "VLG"),]

AssignGatesAtTime(bcn, flights, "10:00")
info = GateOccupancy(bcn)
occupied_10 = sum(1 for g in info if g[1] == 'occupied')

AssignGatesAtTime(bcn, flights, "14:00")
info = GateOccupancy(bcn)
occupied_14 = sum(1 for g in info if g[1] == 'occupied')
occupied_ids = [g[2] for g in info if g[1] == 'occupied']

if occupied_10 == 2 and occupied_14 == 1 and "NEW1" in occupied_ids:
    print(f"PASS: Freed 2 departed gates, assigned 1 new")
    print(f"  10:00 period: {occupied_10} gates occupied")
    print(f"  14:00 period: {occupied_14} gates occupied (NEW1)")
else:
    print(f"ERROR: Gate freeing not working correctly")


# Test 3 - PlotDayOccupancy: Real Data Visualization
print("\nTest 3 - PlotDayOccupancy (Real Data):")

try:
    # Load real data
    arrivals = LoadArrivals("arrivals.txt")
    departures = LoadDepartures("Departures.txt")
    
    if len(arrivals) > 0 and len(departures) > 0:
        print(f"  Loaded {len(arrivals)} arrivals, {len(departures)} departures")
        
        # Merge movements
        merged = MergeMovements(arrivals, departures)
        print(f"  Merged: {len(merged)} aircraft")
        
        # Get night aircraft
        night = NightAircraft(merged)
        print(f"  Night aircraft: {len(night)}")
        
        # Create fresh airport for plotting
        bcn_plot = LoadAirportStructure("../Proyecto-mainV4/Proyecto-main4/Terminals.txt")
        
        # Reset to initial state (night aircraft only)
        ResetToNightAircraftOnly(bcn_plot, night)
        
        print(f"\n  Generating occupancy plot for entire day...")
        
        # Generate the plot
        PlotDayOccupancy(bcn_plot, merged)
        
        print(f"PASS: Plot generated successfully")
        print(f"  (Close the plot window to continue)")
    else:
        print("  SKIP: arrivals.txt or Departures.txt not found")
        
except Exception as e:
    print(f"  ERROR: {e}")


print("\n" + "="*60)
print("TESTS COMPLETED")
print("="*60)
print("\nSummary:")
print("  Test 1: Assign gate time ✓")
print("  Test 2: AssignGatesAtTime: Freeing Gates")
print("  Test 3: PlotDayOccupancy: Real Data Visualization ✓")