import matplotlib.pyplot as plt
from airport import *
import webbrowser
import os
from math import radians, sin, cos, sqrt, atan2
import platform
import subprocess

class Aircraft:
    def __init__(self,id,Origin,Arrival,Airline):
        self.id = id
        self.OriginAirport = Origin
        self.TimeLanding =  Arrival
        self.AirlineCompany = Airline

# Son los arrives a LEBL en un cierto día
def LoadArrivals(filename):
    arrives = []

    try:
        with open(filename, 'r') as file:
            file.readline()

            for line in file:
                parts = line.strip().split()

                if len(parts) != 4:
                    continue

                id = parts[0]
                Origin = parts[1]
                Arrival = parts[2]
                Airline = parts[3]

                # Validar formato de tiempo
                if ':' not in Arrival:
                    continue

                try:
                    time_parts = Arrival.split(':')
                    hour = int(time_parts[0])
                    minute = int(time_parts[1])
                    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                        continue
                except (ValueError, IndexError):
                    continue

                arrive = Aircraft(id, Origin, Arrival, Airline)
                arrives.append(arrive)

    except FileNotFoundError:
        return []

    return arrives

def PlotArrivals(aircrafts):
    if len(aircrafts) == 0:
        print("No airports to plot.")
        return

    arrivals=[]
    for flight in aircrafts:
        arrivals.append(flight.TimeLanding.strip())

    i=0
    landing_frequency=[0]*24
    while i<len(arrivals):
        hour=int(arrivals[i][:2])
        landing_frequency[hour]+=1
        i+=1

    h=0
    hours=[]
    while h < 24:
        hours.append(f'{h:02d}:00')
        h+=1

    fig, ax = plt.subplots()

    ax.bar( hours,landing_frequency,label='vuelos',color='steelblue')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Number of flights')
    ax.set_title('Landing frequency per hour')
    ax.legend()
    plt.xticks(rotation=45)
    plt.show()

def SaveFlights(aircrafts,filename):
    if len(aircrafts)==0:
        print('no se ha podido crear el fichero')
        return

    file=open(filename, 'w')
    file.write(f'AIRCRAFT ORIGIN ARRIVAL ARILINE\n')
    for flight in aircrafts:
        id=flight.id
        origin=flight.OriginAirport
        arrival=flight.TimeLanding
        airline=flight.AirlineCompany
        if id.strip() == '':
            id = '0'
        if origin.strip() == '':
            origin = '0'
        if arrival.strip() == '':
            arrival = '0'
        if airline.strip() == '':
            airline = '0'
        file.write(f'{id} {origin} {arrival} {airline}\n')
    file.close()

def PlotAirlines(aircrafts):
    if len(aircrafts) == 0:
        print("Error: No aircraft data to plot.")
        return

    # Count flights per airline
    airline_counts = {}
    for aircraft in aircrafts:
        airline = aircraft.AirlineCompany
        if airline in airline_counts:
            airline_counts[airline] += 1
        else:
            airline_counts[airline] = 1

    # Sort by number of flights (most to least)
    sorted_items = sorted(airline_counts.items(), key=lambda x: x[1], reverse=True)
    airlines = [item[0] for item in sorted_items]
    counts = [item[1] for item in sorted_items]

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.bar(airlines, counts, color='green')
    ax.set_xlabel('Airline')
    ax.set_ylabel('Number of Flights')
    ax.set_title('Flights per Airline')
    plt.xticks(rotation=90)
    plt.tight_layout()
    ax.grid(axis='y', alpha=0.3)
    plt.show()


def MapFlights(aircrafts, airports):

    if len(aircrafts) == 0:
        print("Error: No flights to map.")
        return

    if len(airports) == 0:
        print("Error: No airports loaded. Cannot map flights without airport coordinates.")
        return

    airport_dict = {}
    for airport in airports:
        airport_dict[airport.code] = airport

    LEBL_LAT = 41.297445
    LEBL_LON = 2.0832941

    filename = "flights.kml"

    # Crear contenido KML
    kml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    kml_content += '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
    kml_content += '<Document>\n'
    kml_content += '  <n>Flight Trajectories to LEBL</n>\n'
    kml_content += '  <description>Schengen and Non-Schengen Flight Trajectories</description>\n'

    # Estilos para Schengen (verde) y Non-Schengen (rojo)
    kml_content += '  <Style id="schengen_line">\n'
    kml_content += '    <LineStyle>\n'
    kml_content += '      <color>ff00ff00</color>\n'
    kml_content += '      <width>2</width>\n'
    kml_content += '    </LineStyle>\n'
    kml_content += '  </Style>\n'

    kml_content += '  <Style id="nonschengen_line">\n'
    kml_content += '    <LineStyle>\n'
    kml_content += '      <color>ff0000ff</color>\n'
    kml_content += '      <width>2</width>\n'
    kml_content += '    </LineStyle>\n'
    kml_content += '  </Style>\n'

    mapped_count = 0

    for aircraft in aircrafts:
        origin_code = aircraft.OriginAirport

        # Buscar aeropuerto de origen
        if origin_code not in airport_dict:
            continue

        origin_airport = airport_dict[origin_code]

        # Determinar si es Schengen
        is_schengen = IsSchengenAirport(origin_code)
        style = 'schengen_line' if is_schengen else 'nonschengen_line'
        schengen_text = 'Schengen' if is_schengen else 'Non-Schengen'

        # Crear placemark para la trayectoria
        kml_content += '  <Placemark>\n'
        kml_content += f'    <n>{aircraft.id} ({origin_code} → LEBL)</n>\n'
        kml_content += f'    <description>'
        kml_content += f'Flight: {aircraft.id}<br/>'
        kml_content += f'Airline: {aircraft.AirlineCompany}<br/>'
        kml_content += f'Origin: {origin_code}<br/>'
        kml_content += f'Arrival: {aircraft.TimeLanding}<br/>'
        kml_content += f'Type: {schengen_text}'
        kml_content += f'</description>\n'
        kml_content += f'    <styleUrl>#{style}</styleUrl>\n'
        kml_content += '    <LineString>\n'
        kml_content += '      <tessellate>1</tessellate>\n'
        kml_content += '      <coordinates>\n'
        kml_content += f'        {origin_airport.lon},{origin_airport.lat},0\n'
        kml_content += f'        {LEBL_LON},{LEBL_LAT},0\n'
        kml_content += '      </coordinates>\n'
        kml_content += '    </LineString>\n'
        kml_content += '  </Placemark>\n'

        mapped_count += 1

    kml_content += '</Document>\n'
    kml_content += '</kml>\n'

    if mapped_count == 0:
        print("Error: No flights could be mapped. Check that origin airports are loaded.")
        return

    # Guardar archivo KML
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(kml_content)

        abs_path = os.path.abspath(filename)

        # Detectar sistema operativo y abrir Google Earth Pro
        system = platform.system()
        google_earth_opened = False

        if system == "Windows":
            # Rutas comunes de Google Earth Pro en Windows
            possible_paths = [
                r"C:\Program Files\Google\Google Earth Pro\client\googleearth.exe",
                r"C:\Program Files (x86)\Google\Google Earth Pro\client\googleearth.exe",
                os.path.expanduser(r"~\AppData\Local\Google\Google Earth Pro\client\googleearth.exe")
            ]

            for path in possible_paths:
                if os.path.exists(path):
                    try:
                        subprocess.Popen([path, abs_path])
                        google_earth_opened = True
                        break
                    except:
                        continue

        elif system == "Darwin":  # macOS
            try:
                subprocess.Popen(["open", "-a", "Google Earth Pro", abs_path])
                google_earth_opened = True
            except:
                pass

        elif system == "Linux":
            try:
                subprocess.Popen(["google-earth-pro", abs_path])
                google_earth_opened = True
            except:
                pass

        if not google_earth_opened:
            try:
                if system == "Windows":
                    os.startfile(abs_path)
                elif system == "Darwin":
                    subprocess.Popen(["open", abs_path])
                else:
                    subprocess.Popen(["xdg-open", abs_path])
                google_earth_opened = True
            except:
                pass

        if not google_earth_opened:
            print(f"KML file '{filename}' created with {mapped_count} trajectories.")
            print("Could not open Google Earth Pro automatically.")
            print(f"Please open Google Earth Pro and load the file '{filename}'")

    except Exception as e:
        print(f"Error creating KML file: {str(e)}")


def HaversineDistance(lat1, lon1, lat2, lon2):

    R = 6371.0

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance


def LongDistanceArrivals(aircrafts, airports):

    if len(aircrafts) == 0:
        print("Error: No aircrafts to process.")
        return []

    if len(airports) == 0:
        print("Error: No airports loaded. Cannot calculate distances.")
        return []

    airport_dict = {}
    for airport in airports:
        airport_dict[airport.code] = airport

    LEBL_LAT = 41.297445
    LEBL_LON = 2.0832941

    long_distance = []

    for aircraft in aircrafts:
        origin_code = aircraft.OriginAirport

        if origin_code not in airport_dict:
            continue

        origin_airport = airport_dict[origin_code]

        distance = HaversineDistance(
            origin_airport.lat, origin_airport.lon,
            LEBL_LAT, LEBL_LON)

        if distance > 2000:
            long_distance.append(aircraft)

    return long_distance