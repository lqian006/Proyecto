class NavPoint:
    def __init__(self, number, name, latitude, longitude):
        self.number = number
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

class NavAirport:
    def __init__(self, Name_airport, SIDs, STARs):
        self.Name_airport = Name_airport
        self.SIDs = SIDs
        self.STARs = STARs

class NavSegment:
    def __init__(self, OriginNumber, DestinationNumber, Distance):
        self.OriginNumber = OriginNumber
        self.DestinationNumber = DestinationNumber
        self.Distance = Distance

class AirSpace:
    def __init__(self, NavPoints, NavSegments, NavAirports):
        self.NavPoints = []
        self.NavSegments = []
        self.NavAirports = []

def LoadAirSpace (file_nav, file_seg, file_aer):
    airspace = AirSpace()
    with open(file_nav,"r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 4:
                number, name, lat, lon = parts
                airspace.NavSegments.append(NavSegment(number,name,lat, lon))

    with open (file_seg,"r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                origin, dest, cost = parts
                airspace.NavSegments.append(NavSegment(origin,dest,cost))

    with open (file_aer,"r") as f:
        current_airport = None
        for line in f:
            line = line.strip()
            if line.startswith("LE"):
                current_airport = NavAirport(line)
                airspace.NavAirports.append(current_airport)
            elif ".D" in line:
                current_airport.SIDs.append(line)
            elif ".A" in line:
                current_airport.STARs.append(line)
    return airspace



