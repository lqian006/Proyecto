import matplotlib.pyplot as plt

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
    '''Converts decimal degrees to DMS format.
    '''
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
    
    plt.show()

def MapAirports (airports):
    if len(airports) == 0:
        print("No airports to map.")
        return
    
    # Create KML content
    kml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    kml_content += '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
    kml_content += '<Document>\n'
    
    # Add styles for Schengen (green) and non-Schengen (red)
    kml_content += '<Style id="schengen">\n'
    kml_content += '  <IconStyle>\n'
    kml_content += '    <color>ff00ff00</color>\n'
    kml_content += '  </IconStyle>\n'
    kml_content += '</Style>\n'
    
    kml_content += '<Style id="nonschengen">\n'
    kml_content += '  <IconStyle>\n'
    kml_content += '    <color>ff0000ff</color>\n'
    kml_content += '  </IconStyle>\n'
    kml_content += '</Style>\n'
    
    # Add each airport as a placemark
    i = 0
    while i < len(airports):
        airport = airports[i]
        style = 'schengen' if airport.schengen else 'nonschengen'
        schengen_text = 'Schengen' if airport.schengen else 'Non-Schengen'
        
        kml_content += '<Placemark>\n'
        kml_content += f'  <name>{airport.code}</name>\n'
        kml_content += f'  <description>{schengen_text} Airport</description>\n'
        kml_content += f'  <styleUrl>#{style}</styleUrl>\n'
        kml_content += '  <Point>\n'
        kml_content += '    <coordinates>\n'
        kml_content += f'      {airport.lon},{airport.lat}\n'
        kml_content += '    </coordinates>\n'
        kml_content += '  </Point>\n'
        kml_content += '</Placemark>\n'
        
        i += 1
    
    kml_content += '</Document>\n'
    kml_content += '</kml>\n'
    
    # Save to file
    filename = 'airports.kml'
    file = open(filename, 'w')
    file.write(kml_content)
    file.close()
    
    print(f"KML file '{filename}' created. Open it with Google Earth.")