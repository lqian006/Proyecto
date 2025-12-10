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
            
            # Load airlines for this terminal
            LoadAirlines(current_terminal, t_name)
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

#---- version 4 -----

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
    # Buscar terminal de la aerolínea
    terminal_name = SearchTerminal(bcn, aircraft.AirlineCompany)
    
    if terminal_name == "":
        return -1
    
    # Encontrar el objeto terminal
    terminal = None
    for t in bcn.terms:
        if t.Name == terminal_name:
            terminal = t
            break
    
    if terminal is None:
        return -1
    
    # Determinar si el vuelo es Schengen o non-Schengen
    is_schengen = IsSchengenAirport(aircraft.OriginAirport)
    flight_type = "Schengen" if is_schengen else "non-Schengen"
    
    # Buscar primera puerta libre en el área correcta
    for area in terminal.BoardingArea:
        if area.type == flight_type:
            for gate in area.gate:
                if not gate.occupancy:
                    # 4. Asignar puerta
                    gate.occupancy = True
                    gate.id = aircraft.id
                    return 0
    
    return -1

def AssignNightGates(bcn, aircrafts):
   
    # Check if input list is empty
    if len(aircrafts) == 0:
        return -1
    
    assigned_count = 0
    
    for aircraft in aircrafts:
        # Check if this is a night aircraft (departure only, no arrival)
        # Night aircraft have: DestinationAirport filled, OriginAirport empty
        has_arrival = aircraft.OriginAirport != "" or aircraft.TimeLanding != ""
        has_departure = aircraft.DestinationAirport != "" and aircraft.TimeDeparture != ""
        
        # Skip if not a night aircraft (has arrival data or no departure data)
        if has_arrival or not has_departure:
            continue
        
        # For night aircraft, we need to determine Schengen status from destination
        # Since there's no origin, we check the destination airport
        is_schengen = IsSchengenAirport(aircraft.DestinationAirport)
        
        # Temporarily set OriginAirport to destination for gate assignment
        # (AssignGate uses OriginAirport to determine Schengen status)
        original_origin = aircraft.OriginAirport
        aircraft.OriginAirport = aircraft.DestinationAirport
        
        # Try to assign gate
        result = AssignGate(bcn, aircraft)
        
        # Restore original OriginAirport value
        aircraft.OriginAirport = original_origin
        
        if result == 0:
            assigned_count += 1
    
    return assigned_count


def FreeGate(bcn, id):
    
    # Search all terminals
    for terminal in bcn.terms:
        # Search all boarding areas in the terminal
        for area in terminal.BoardingArea:
            # Search all gates in the boarding area
            for gate in area.gate:
                # Check if this gate is assigned to the aircraft
                if gate.id == id:
                    # Free the gate
                    gate.occupancy = False
                    gate.id = ""
                    return 0
    
    # Aircraft not found in any gate
    return -1

"""
Version 4 - Dynamic Gate Assignment Functions
Add these to your LEBL.py file
"""

def AssignGatesAtTime(bcn, aircrafts, time):
    
    # Validate time format
    if not time or ':' not in time:
        return -1
    
    # Parse the time
    parts = time.split(':')
    if len(parts) != 2:
        return -1
    
    if not parts[0].isdigit() or not parts[1].isdigit():
        return -1
    
    hour = int(parts[0])
    minute = int(parts[1])
    
    if hour < 0 or hour > 23 or minute != 0:
        return -1
    
    # Convert to minutes for comparison
    period_start = hour * 60  # Start of this hour
    period_end = (hour + 1) * 60  # Start of next hour
    
    # Step 1: Free gates of aircraft that have departed before this time period
    for aircraft in aircrafts:
        # Check if aircraft has departure time
        if aircraft.TimeDeparture != "":
            # Parse departure time
            dep_parts = aircraft.TimeDeparture.split(':')
            if len(dep_parts) == 2 and dep_parts[0].isdigit() and dep_parts[1].isdigit():
                dep_hour = int(dep_parts[0])
                dep_min = int(dep_parts[1])
                dep_time_minutes = dep_hour * 60 + dep_min
                
                # If aircraft departed before this period, free its gate
                if dep_time_minutes < period_start:
                    FreeGate(bcn, aircraft.id)
    
    # Step 2: Assign gates to aircraft landing during this period
    not_assigned_count = 0
    
    for aircraft in aircrafts:
        # Check if aircraft has arrival time
        if aircraft.TimeLanding != "":
            # Parse arrival time
            arr_parts = aircraft.TimeLanding.split(':')
            if len(arr_parts) == 2 and arr_parts[0].isdigit() and arr_parts[1].isdigit():
                arr_hour = int(arr_parts[0])
                arr_min = int(arr_parts[1])
                arr_time_minutes = arr_hour * 60 + arr_min
                
                # Check if arrival is in this period [period_start, period_end)
                if period_start <= arr_time_minutes < period_end:
                    # Try to assign gate
                    result = AssignGate(bcn, aircraft)
                    
                    if result == -1:
                        # Could not assign gate (terminal full or airline not found)
                        not_assigned_count += 1
    
    return not_assigned_count


def PlotDayOccupancy(bcn, aircrafts):
    
    import matplotlib.pyplot as plt
    
    # Store occupancy data for each terminal
    terminal_names = [t.Name for t in bcn.terms]
    terminal_occupancy = {name: [] for name in terminal_names}
    unassigned_per_hour = []
    hours = []
    
    # Simulate each hour of the day (00:00 to 23:00)
    for hour in range(24):
        time_str = f"{hour:02d}:00"
        hours.append(time_str)
        
        # Assign gates for this hour
        unassigned = AssignGatesAtTime(bcn, aircrafts, time_str)
        unassigned_per_hour.append(unassigned)
        
        # Count occupied gates per terminal
        for terminal in bcn.terms:
            occupied_count = 0
            for area in terminal.BoardingArea:
                for gate in area.gate:
                    if gate.occupancy:
                        occupied_count += 1
            terminal_occupancy[terminal.Name].append(occupied_count)
    
    # Create the plot
    num_terminals = len(terminal_names)
    fig, axes = plt.subplots(num_terminals + 1, 1, figsize=(12, 4 * (num_terminals + 1)))
    
    # If only one terminal, axes is not a list
    if num_terminals == 1:
        axes = [axes[0], axes[1]]
    
    # Plot occupancy for each terminal
    for idx, terminal_name in enumerate(terminal_names):
        ax = axes[idx]
        occupancy_data = terminal_occupancy[terminal_name]
        
        ax.plot(range(24), occupancy_data, marker='o', linewidth=2, markersize=6)
        ax.set_xlabel('Hour of Day', fontsize=11)
        ax.set_ylabel('Occupied Gates', fontsize=11)
        ax.set_title(f'Gate Occupancy - {terminal_name}', fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xticks(range(24))
        ax.set_xticklabels([f"{h:02d}:00" for h in range(24)], rotation=45, ha='right')
        
        # Find terminal's total gates
        total_gates = sum(len(area.gate) for area in bcn.terms[idx].BoardingArea)
        ax.axhline(y=total_gates, color='r', linestyle='--', alpha=0.5, label=f'Max Gates ({total_gates})')
        ax.legend()
    
    # Plot unassigned aircraft
    ax_unassigned = axes[num_terminals]
    ax_unassigned.bar(range(24), unassigned_per_hour, color='red', alpha=0.7)
    ax_unassigned.set_xlabel('Hour of Day', fontsize=11)
    ax_unassigned.set_ylabel('Unassigned Aircraft', fontsize=11)
    ax_unassigned.set_title('Aircraft Not Assigned Per Hour', fontsize=13, fontweight='bold')
    ax_unassigned.grid(True, alpha=0.3, axis='y')
    ax_unassigned.set_xticks(range(24))
    ax_unassigned.set_xticklabels([f"{h:02d}:00" for h in range(24)], rotation=45, ha='right')
    
    plt.tight_layout()
    plt.show()


def ResetToNightAircraftOnly(bcn, night_aircraft):
    # Free all gates
    for terminal in bcn.terms:
        for area in terminal.BoardingArea:
            for gate in area.gate:
                gate.occupancy = False
                gate.id = ""
    
    # Assign night aircraft
    AssignNightGates(bcn, night_aircraft)


