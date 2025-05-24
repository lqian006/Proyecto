from test_navPoint import*
from test_navSegment import*
from test_navAirpoint import*




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