from waypoint import*
class FlightPlan:
    def __init__(self, name, Waypoints):
        self.name=name
        self.Waypoints=[]


def AddWaypoint(self,waypoint):
    self.Waypoints.append(waypoint)


def ShowFlightPlan(fp):
    print(f"Flight plan: {fp.name}")
    if len(fp.waypoints) == 0:
        print(" (No waypoints)")
    else:
        for wp in fp.waypoints:
            ShowWaypoint(wp)




# 🆕 STEP 4

def FindWaypoint(fp, name):
    """Busca un waypoint por nombre en el flight plan"""
    for wp in fp.waypoints:
        if wp.name == name:
            return wp
    return None

def RemoveWaypoint(fp, name):
    """Elimina el waypoint con el nombre dado si existe"""
    wp = FindWaypoint(fp, name)
    if wp:
        fp.waypoints.remove(wp)
        return True
    return False

def FlightPlanLength(fp):
    """Calcula la longitud total del plan de vuelo (suma de distancias consecutivas)"""
    total = 0.0
    for i in range(len(fp.waypoints) - 1):
        wp1 = fp.waypoints[i]
        wp2 = fp.waypoints[i+1]
        total += haversine(wp1, wp2)
    return total

