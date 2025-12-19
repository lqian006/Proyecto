import matplotlib.pyplot as plt
import os
import platform
import subprocess
import math

from matplotlib.textpath import text_to_path


class Airport:
    def __init__(self,code,lat,lon):
        self.code = code
        self.lat = lat
        self.lon = lon
        self.schengen = False

def IsSchengenAirport(code):
    if not code or len(code) < 2:
        return False
    schengen_codes = {'LO', 'EB', 'LK', 'LC', 'EK', 'FO', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH', 'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'GC', 'LE', 'ES', 'LS'}
    return code[:2] in schengen_codes
    
def SetSchengen(airport):
    if IsSchengenAirport(airport.code):
        airport.schengen = True
    else:
        airport.schengen = False
   
def PrintAirport(airport):
    schengen = "Yes" if airport.schengen else "No"
     
    print(f"Airport: {airport.code}")
    print(f"  Latitude: {airport.lat}")
    print(f"  Longitude: {airport.lon}")
    print(f"  Schengen: {schengen}")

def LoadAirports(filename): 
    airports = []
    file = open(filename, 'r')

    line = file.readline()
    
    while line:
        parts = line.strip().split()
        if len(parts) == 3:
            code = parts[0]
            lat = ConvertCoordinate(parts[1])
            lon = ConvertCoordinate(parts[2])
            
            airport = Airport(code, lat, lon)
            SetSchengen(airport)
            airports.append(airport)
        
        line = file.readline()
    
    file.close()
    return airports

def ConvertCoordinate(coord_str):
    '''Converts coordinate from DMS format to decimal degrees.'''
    if not coord_str or len(coord_str) < 7:
        return 0.0
    
    direction = coord_str[0]
    
    # Check if we have 7 or 8 digits after direction
    if len(coord_str) == 8:  # Format: EDDDMMSS (longitude)
        degrees = int(coord_str[1:4])
        minutes = int(coord_str[4:6])
        seconds = int(coord_str[6:8])
    else:  # Format: NDDMMSS (latitude) 
        degrees = int(coord_str[1:3])
        minutes = int(coord_str[3:5])
        seconds = int(coord_str[5:7])
    
    # Convert to decimal degrees
    decimal = degrees + minutes / 60.0 + seconds / 3600.0
    
    # Make negative for South and West
    if direction in ['S', 'W']:
        decimal = -decimal
    
    return decimal

def SaveSchengenAirports (airports,filename):
    if len(airports) == 0:
        return -1
    
    # Filter Schengen airports
    schengen_airports = []
    i = 0
    while i < len(airports):
        if airports[i].schengen:
            schengen_airports.append(airports[i])
        i += 1
    
    if len(schengen_airports) == 0:
        return -1
    
    # Write to file
    file = open(filename, 'w')
    file.write("CODE LAT LON\n")
    
    # Write each Schengen airport
    i = 0
    while i < len(schengen_airports):
        airport = schengen_airports[i]
        lat_str = DecimalToDMS(airport.lat, True)
        lon_str = DecimalToDMS(airport.lon, False)
        file.write(f"{airport.code} {lat_str} {lon_str}\n")
        i += 1
    
    file.close()
    return 0

def DecimalToDMS(decimal, is_latitude):
    '''Converts decimal degrees to DMS format.'''
    if decimal < 0:
        direction = 'S' if is_latitude else 'W'
        decimal = -decimal
    else:
        direction = 'N' if is_latitude else 'E'
    
    degrees = int(decimal)
    minutes = int((decimal - degrees) * 60)
    seconds = int(((decimal - degrees) * 60 - minutes) * 60)
    
    return f"{direction}{degrees:02d}{minutes:02d}{seconds:02d}"

def AddAirport(airports,airport):
    i = 0
    while i < len(airports):
        if airports[i].code == airport.code:
            return -1
        i += 1
    
    airports.append(airport)
    return 0

def RemoveAirport (airports,code):
    i = 0
    while i < len(airports):
        if airports[i].code == code:
            airports.pop(i)
            return 0
        i += 1
    
    return -1

def PlotAirports(airports):
    if len(airports) == 0:
        print("No airports to plot.")
        return
    
    schengen_count = 0
    non_schengen_count = 0
    
    i = 0
    while i < len(airports):
        if airports[i].schengen:
            schengen_count += 1
        else:
            non_schengen_count += 1
        i += 1
    
    fig, ax = plt.subplots()
    
    ax.bar(['Airports'], [schengen_count], label='Schengen', color='steelblue')
    ax.bar(['Airports'], [non_schengen_count], bottom=[schengen_count], label='No Schengen', color='lightcoral')
    ax.set_ylabel('Count')
    ax.set_title('Schengen airports')
    ax.legend()

    return fig


def MapAirports(airports, base_filename="airports"):

    if not airports or len(airports) == 0:
        return (False, "No hay aeropuertos para mapear.", "")

    filename = f"{base_filename}.kml"

    # Crear contenido KML
    kml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    kml_content += '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
    kml_content += '<Document>\n'
    kml_content += '  <name>Airports Map</name>\n'
    kml_content += '  <description>Schengen and Non-Schengen Airports</description>\n'

    # Estilos para Schengen (verde) y Non-Schengen (rojo)
    kml_content += '  <Style id="schengen">\n'
    kml_content += '    <IconStyle>\n'
    kml_content += '      <color>ff00ff00</color>\n'
    kml_content += '      <scale>1.3</scale>\n'
    kml_content += '    </IconStyle>\n'
    kml_content += '    <LabelStyle>\n'
    kml_content += '      <scale>0.9</scale>\n'
    kml_content += '    </LabelStyle>\n'
    kml_content += '  </Style>\n'

    kml_content += '  <Style id="nonschengen">\n'
    kml_content += '    <IconStyle>\n'
    kml_content += '      <color>ff0000ff</color>\n'
    kml_content += '      <scale>1.3</scale>\n'
    kml_content += '    </IconStyle>\n'
    kml_content += '    <LabelStyle>\n'
    kml_content += '      <scale>0.9</scale>\n'
    kml_content += '    </LabelStyle>\n'
    kml_content += '  </Style>\n'

    # Agregar cada aeropuerto como placemark
    for airport in airports:
        style = 'schengen' if airport.schengen else 'nonschengen'
        schengen_text = 'Schengen' if airport.schengen else 'Non-Schengen'

        kml_content += '  <Placemark>\n'
        kml_content += f'    <name>{airport.code}</name>\n'
        kml_content += f'    <description>{schengen_text} Airport<br/>Lat: {airport.lat:.4f}<br/>Lon: {airport.lon:.4f}</description>\n'
        kml_content += f'    <styleUrl>#{style}</styleUrl>\n'
        kml_content += '    <Point>\n'
        kml_content += f'      <coordinates>{airport.lon},{airport.lat},0</coordinates>\n'
        kml_content += '    </Point>\n'
        kml_content += '  </Placemark>\n'

    kml_content += '</Document>\n'
    kml_content += '</kml>\n'

    # Guardar archivo KML
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(kml_content)

        # Obtener ruta absoluta
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

        if google_earth_opened:
            return (True, f"Archivo KML '{filename}' creado y abierto correctamente.", filename)
        else:
            message = (f"Archivo KML '{filename}' creado.\n\n"
                       f"No se pudo abrir Google Earth Pro automáticamente.\n\n"
                       f"Por favor:\n"
                       f"1. Abre Google Earth Pro manualmente\n"
                       f"2. Archivo → Abrir → Selecciona '{filename}'\n\n"
                       f"O haz doble clic en '{filename}' si Google Earth está instalado.")
            return (True, message, filename)

    except Exception as e:
        return (False, f"No se pudo crear el KML: {str(e)}", "")


def HaversineDistance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radio de la Tierra en km

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def MapCloseAirport(airports, base_filename="AeropuertosCercanos", reference="", max_distance_km=100):

    reference_airport = None # Buscar aeropuerto
    for a in airports:
        if a.code == reference:
            reference_airport = a
            break

    if reference_airport is None: # si no existe no hay, avisar
        return (False, f"Aeropuerto no encontrado.", "")

    close_airports = [] # Filtrar aeropuertos cercanos
    for a in airports:
        if a.code == reference:
            continue  # no contar la referencia
        dist = HaversineDistance(reference_airport.lat, reference_airport.lon, a.lat, a.lon)
        if dist <= max_distance_km:
            close_airports.append(a)

    if len(close_airports) == 0:
        return (False, "No hay aeropuertos dentro de la distancia indicada.", "")
        #por si no hay nada cerca

    filename = f"{base_filename}.kml" #name del archivo

    kml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    kml_content += '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
    kml_content += '<Document>\n'
    kml_content += f'  <name>Airports near {reference}</name>\n'
    kml_content += f'  <description>Aeropuertos a menos de {max_distance_km} km de {reference}</description>\n'

    # colorines para chengen
    kml_content += '  <Style id="schengen">\n'
    kml_content += '    <IconStyle>\n'
    kml_content += '      <color>ff00ff00</color>\n'
    kml_content += '      <scale>1.3</scale>\n'
    kml_content += '    </IconStyle>\n'
    kml_content += '  </Style>\n'

    #colorines para no schengen
    kml_content += '  <Style id="nonschengen">\n'
    kml_content += '    <IconStyle>\n'
    kml_content += '      <color>ff0000ff</color>\n'
    kml_content += '      <scale>1.3</scale>\n'
    kml_content += '    </IconStyle>\n'
    kml_content += '  </Style>\n'

    # colorin para la referencia
    kml_content += '  <Style id="reference">\n'
    kml_content += '    <IconStyle>\n'
    kml_content += '      <color>ffffaa00</color>\n'
    kml_content += '      <scale>1.5</scale>\n'
    kml_content += '    </IconStyle>\n'
    kml_content += '  </Style>\n'

    # ponerle un (referencia) al lado del nombre
    kml_content += '  <Placemark>\n'
    kml_content += f'    <name>{reference_airport.code} (Referencia)</name>\n'
    kml_content += '    <styleUrl>#reference</styleUrl>\n'
    kml_content += '    <Point>\n'
    kml_content += f'      <coordinates>{reference_airport.lon},{reference_airport.lat},0</coordinates>\n'
    kml_content += '    </Point>\n'
    kml_content += '  </Placemark>\n'

    #crear marcadores para los otros eroppuertos
    for airport in close_airports:
        style = 'schengen' if airport.schengen else 'nonschengen'
        schengen_text = "Schengen" if airport.schengen else "Non-Schengen"

        kml_content += '  <Placemark>\n'
        kml_content += f'    <name>{airport.code}</name>\n'
        kml_content += f'    <description>{schengen_text}</description>\n'
        kml_content += f'    <styleUrl>#{style}</styleUrl>\n'
        kml_content += '    <Point>\n'
        kml_content += f'      <coordinates>{airport.lon},{airport.lat},0</coordinates>\n'
        kml_content += '    </Point>\n'
        kml_content += '  </Placemark>\n'

    kml_content += '</Document>\n'
    kml_content += '</kml>\n'

    #guarar el archivo
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(kml_content)

        abs_path = os.path.abspath(filename)

        return (True, f"KML '{filename}' creado correctamente.", filename)

    except Exception as e:
        return (False, f"No se pudo crear el archivo: {str(e)}", "")