from math import*

class Waypoint:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon

def ShowWaypoint(waypoint):
    print('Nombre:{0}, lat:{1}, lon:{2}'
    .format (
        waypoint.name,
        waypoint.lat,
        waypoint.lon
    ))

def haversine(wp1, wp2):
    """Devuelve la distancia Haversine entre dos waypoints (en km)."""
    R = 6378.0
    lat1, lon1 = radians(wp1.lat), radians(wp1.lon)
    lat2, lon2 = radians(wp2.lat), radians(wp2.lon)
    dLat = lat2 - lat1
    dLon = lon2 - lon1
    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c