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

def haversine(lat1, lon1, lat2, lon2):

    R = 6378

    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dLon / 2) ** 2
    c = 2 * asin(sqrt(a))

    return R * c