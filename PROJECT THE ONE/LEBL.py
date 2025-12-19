import matplotlib.pyplot as plt
from aircraft import *
import os

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
        self.assignes_aircraft_id=None

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

#-----VERSIÓN 4-----#


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

    if not aircrafts:
        print("Error: lista de aircrafts vacía.")
        return None

    hours = list(range(24))
    terminal_names = [t.Name for t in bcn.terms]

    terminal_occupancy = {name: [] for name in terminal_names}
    unassigned_per_hour = []

    for hour in hours:
        time_str = f"{hour:02d}:00"
        unassigned = AssignGatesAtTime(bcn, aircrafts, time_str)
        unassigned_per_hour.append(unassigned)

        for terminal in bcn.terms:
            occupied = 0
            for area in terminal.BoardingArea:
                for gate in area.gate:
                    if gate.occupancy:
                        occupied += 1
            terminal_occupancy[terminal.Name].append(occupied)

    # -------- PLOT --------
    fig, ax1 = plt.subplots(figsize=(12, 5))

    for terminal_name in terminal_names:
        ax1.plot(
            hours,
            terminal_occupancy[terminal_name],
            marker='o',
            linewidth=2,
            label=f"Gates ocupadas - {terminal_name}"
        )

    ax1.set_xlabel("Hora del día")
    ax1.set_ylabel("Gates ocupadas")
    ax1.set_xticks(hours)
    ax1.set_xticklabels([f"{h:02d}:00" for h in hours], rotation=45)
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    ax2.bar(
        hours,
        unassigned_per_hour,
        alpha=0.3,
        color="red",
        label="Aircrafts no asignados"
    )
    ax2.set_ylabel("Aircrafts no asignados")

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper left")

    fig.suptitle("Ocupación de gates y aircrafts no asignados por hora")

    fig.tight_layout(rect=[0, 0, 1, 0.95])

    return fig





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
                    gate.assignes_aircraft_id=None
                    return 0

    # Aircraft not found in any gate
    return -1

def ResetToNightAircraftOnly(bcn, night_aircraft):
    # Free all gates
    for terminal in bcn.terms:
        for area in terminal.BoardingArea:
            for gate in area.gate:
                gate.occupancy = False
                gate.id = ""

    # Assign night aircraft
    AssignNightGates(bcn, night_aircraft)


