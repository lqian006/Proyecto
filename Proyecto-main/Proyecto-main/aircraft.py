import math
import matplotlib.pyplot as plt

class Aircraft:
    def __init__(self,id,Origin,Arrival,Airline):
        self.id = id
        self.OriginAirport = Origin
        self.TimeLanding =  Arrival
        self.AirlineCompany = Airline

# Son los arrives a LEBL en un cierto día
def LoadArrivals(filename):
    arrives = []
    file = open(filename, 'r')
    line = file.readline()
    line = file.readline()

    while line:
        parts = line.strip().split()
        if len(parts) == 4:
            id = parts[0]
            Origin = parts[1]
            Arrival = parts[2]
            Airline= parts[3]

            arrive = Aircraft(id, Origin, Arrival,Airline)
            arrives.append(arrive)

        line = file.readline()

    file.close()
    return arrives

def PlotArrivals(arrives):
    if len(arrives) == 0:
        print("No airports to plot.")
        return

    arrivals=[]
    for flight in arrives:
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

def SaveFlights(arrives,filename):
    if len(arrives)==0:
        print('no se ha podido crear el fichero')
        return

    file=open(filename, 'w')
    file.write(f'AIRCRAFT ORIGIN ARRIVAL ARILINE\n')
    for flight in arrives:
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


def HaversineDistance(lat1, lon1, lat2, lon2):

    R = 6371.0

    # Convertir grados a radianes
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Diferencias
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Fórmula de Haversine
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    return distance


def FindAirportByCode(airports, code):
    """
    Busca un aeropuerto por su código en la lista de aeropuertos.

    Parámetros:
        airports: Lista de objetos Airport
        code: Código del aeropuerto a buscar

    Retorna:
        Objeto Airport si se encuentra, None si no existe
    """
    for airport in airports:
        if airport.code == code:
            return airport
    return None


def LongDistanceArrivals(aircrafts, airports):
    """
    Retorna una lista con los aviones que llegan a LEBL desde un aeropuerto
    a más de 2000 km de distancia (necesitan inspección especial).

    Parámetros:
        aircrafts: Lista de objetos Aircraft
        airports: Lista de objetos Airport

    Retorna:
        Lista de objetos Aircraft que cumplen el criterio
    """
    # Buscar el aeropuerto LEBL
    lebl = FindAirportByCode(airports, 'LEBL')

    if lebl is None:
        print("Error: Aeropuerto LEBL no encontrado en la lista.")
        return []

    long_distance_list = []

    for aircraft in aircrafts:
        # Buscar el aeropuerto de origen
        origin_airport = FindAirportByCode(airports, aircraft.OriginAirport)

        if origin_airport is None:
            continue  # Si no se encuentra el aeropuerto de origen, saltar

        # Calcular distancia usando Haversine
        distance = HaversineDistance(
            origin_airport.lat, origin_airport.lon,
            lebl.lat, lebl.lon
        )

        # Si la distancia es mayor a 2000 km, añadir a la lista
        if distance > 2000:
            long_distance_list.append(aircraft)

    return long_distance_list


def MapFlights(aircrafts, airports):
    """
    Muestra en Google Earth las trayectorias de todos los vuelos desde
    su aeropuerto de origen hasta LEBL.
    Muestra en diferentes colores las trayectorias con origen en un país Schengen.

    Parámetros:
        aircrafts: Lista de objetos Aircraft
        airports: Lista de objetos Airport
    """
    if len(aircrafts) == 0:
        print("No flights to map.")
        return

    # Buscar el aeropuerto LEBL
    lebl = FindAirportByCode(airports, 'LEBL')

    if lebl is None:
        print("Error: Aeropuerto LEBL no encontrado en la lista.")
        return

    # Crear contenido KML
    kml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    kml_content += '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
    kml_content += '<Document>\n'
    kml_content += '  <name>Flight Trajectories to LEBL</name>\n'
    kml_content += '  <description>Flight paths from origin airports to LEBL Barcelona</description>\n'

    # Estilos para líneas Schengen (verde) y Non-Schengen (rojo)
    kml_content += '  <Style id="schengen_line">\n'
    kml_content += '    <LineStyle>\n'
    kml_content += '      <color>ff00ff00</color>\n'  # Verde
    kml_content += '      <width>3</width>\n'
    kml_content += '    </LineStyle>\n'
    kml_content += '  </Style>\n'

    kml_content += '  <Style id="nonschengen_line">\n'
    kml_content += '    <LineStyle>\n'
    kml_content += '      <color>ff0000ff</color>\n'  # Rojo
    kml_content += '      <width>3</width>\n'
    kml_content += '    </LineStyle>\n'
    kml_content += '  </Style>\n'

    # Estilos para marcadores de aeropuertos
    kml_content += '  <Style id="origin_schengen">\n'
    kml_content += '    <IconStyle>\n'
    kml_content += '      <color>ff00ff00</color>\n'
    kml_content += '      <scale>1.0</scale>\n'
    kml_content += '    </IconStyle>\n'
    kml_content += '  </Style>\n'

    kml_content += '  <Style id="origin_nonschengen">\n'
    kml_content += '    <IconStyle>\n'
    kml_content += '      <color>ff0000ff</color>\n'
    kml_content += '      <scale>1.0</scale>\n'
    kml_content += '    </IconStyle>\n'
    kml_content += '  </Style>\n'

    kml_content += '  <Style id="destination">\n'
    kml_content += '    <IconStyle>\n'
    kml_content += '      <color>ff00ffff</color>\n'  # Amarillo
    kml_content += '      <scale>1.5</scale>\n'
    kml_content += '    </IconStyle>\n'
    kml_content += '  </Style>\n'

    # Añadir marcador para LEBL (destino)
    kml_content += '  <Placemark>\n'
    kml_content += f'    <name>LEBL (Destination)</name>\n'
    kml_content += f'    <description>Barcelona El Prat Airport - Arrival destination</description>\n'
    kml_content += '    <styleUrl>#destination</styleUrl>\n'
    kml_content += '    <Point>\n'
    kml_content += f'      <coordinates>{lebl.lon},{lebl.lat},0</coordinates>\n'
    kml_content += '    </Point>\n'
    kml_content += '  </Placemark>\n'

    # Añadir cada vuelo como una línea
    for aircraft in aircrafts:
        # Buscar aeropuerto de origen
        origin_airport = FindAirportByCode(airports, aircraft.origin)

        if origin_airport is None:
            continue  # Si no se encuentra, saltar este vuelo

        # Determinar estilo según si es Schengen o no
        line_style = 'schengen_line' if origin_airport.schengen else 'nonschengen_line'
        marker_style = 'origin_schengen' if origin_airport.schengen else 'origin_nonschengen'
        schengen_text = 'Schengen' if origin_airport.schengen else 'Non-Schengen'

        # Calcular distancia
        distance = HaversineDistance(
            origin_airport.lat, origin_airport.lon,
            lebl.lat, lebl.lon
        )

        # Añadir marcador para aeropuerto de origen
        kml_content += '  <Placemark>\n'
        kml_content += f'    <name>{origin_airport.code}</name>\n'
        kml_content += f'    <description>{schengen_text} Airport - Origin</description>\n'
        kml_content += f'    <styleUrl>#{marker_style}</styleUrl>\n'
        kml_content += '    <Point>\n'
        kml_content += f'      <coordinates>{origin_airport.lon},{origin_airport.lat},0</coordinates>\n'
        kml_content += '    </Point>\n'
        kml_content += '  </Placemark>\n'

        # Añadir línea de trayectoria
        kml_content += '  <Placemark>\n'
        kml_content += f'    <name>Flight: {origin_airport.code} → LEBL</name>\n'
        kml_content += f'    <description>'
        kml_content += f'Aircraft ID: {aircraft.id}<br/>'
        kml_content += f'Origin: {origin_airport.code} ({schengen_text})<br/>'
        kml_content += f'Destination: LEBL<br/>'
        kml_content += f'Distance: {distance:.2f} km'
        kml_content += f'</description>\n'
        kml_content += f'    <styleUrl>#{line_style}</styleUrl>\n'
        kml_content += '    <LineString>\n'
        kml_content += '      <tessellate>1</tessellate>\n'
        kml_content += '      <coordinates>\n'
        kml_content += f'        {origin_airport.lon},{origin_airport.lat},0\n'
        kml_content += f'        {lebl.lon},{lebl.lat},0\n'
        kml_content += '      </coordinates>\n'
        kml_content += '    </LineString>\n'
        kml_content += '  </Placemark>\n'

    kml_content += '</Document>\n'
    kml_content += '</kml>\n'

    # Guardar archivo KML
    filename = 'flights_to_lebl.kml'

    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(kml_content)

        print(f"KML file '{filename}' created successfully.")
        print(f"Total flights mapped: {len(aircrafts)}")

        # Intentar abrir en Google Earth Pro
        import os
        import platform
        import subprocess

        abs_path = os.path.abspath(filename)
        system = platform.system()

        if system == "Windows":
            possible_paths = [
                r"C:\Program Files\Google\Google Earth Pro\client\googleearth.exe",
                r"C:\Program Files (x86)\Google\Google Earth Pro\client\googleearth.exe",
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    subprocess.Popen([path, abs_path])
                    break
            else:
                os.startfile(abs_path)

        elif system == "Darwin":
            subprocess.Popen(["open", "-a", "Google Earth Pro", abs_path])

        else:  # Linux
            subprocess.Popen(["google-earth-pro", abs_path])

    except Exception as e:
        print(f"Error creating KML file: {str(e)}")