from waypoint import*
class FlightPlan:
    def __init__(self, name):
        self.name = name
        self.waypoints = []

def AddWaypoint (fp , waypoint):
    fp.waypoints.append(waypoint)

def ShowFlightPlan(fp):
    print(f"Flight plan: {fp.name}")
    if len(fp.waypoints) == 0:
        print(" No waypoints")
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

# step 5
import matplotlib.pyplot as plt
from waypoint import haversine  # o la función que tengas

def PlotFlightPlan(fp):
    # Calcular límites automáticamente según waypoints
    lons = [wp.lon for wp in fp.waypoints]
    lats = [wp.lat for wp in fp.waypoints]
    margin = 0.5  # para que los puntos no queden pegados al borde
    min_lon, max_lon = min(lons) - margin, max(lons) + margin
    min_lat, max_lat = min(lats) - margin, max(lats) + margin

    # Plot waypoints
    for wp in fp.waypoints:
        plt.plot(wp.lon, wp.lat, 'o', color='red', markersize=5)
        plt.text(wp.lon + 0.05, wp.lat + 0.05, wp.name, color='green', weight='bold', fontsize=6)

    # Draw lines and distance labels
    for i in range(len(fp.waypoints) - 1):
        wp1 = fp.waypoints[i]
        wp2 = fp.waypoints[i + 1]
        plt.plot([wp1.lon, wp2.lon], [wp1.lat, wp2.lat], color='blue', linewidth=0.5)
        distance = haversine(wp1, wp2)
        mid_lon = (wp1.lon + wp2.lon) / 2
        mid_lat = (wp1.lat + wp2.lat) / 2
        plt.text(mid_lon, mid_lat, f'{distance:.2f} km', color='black', fontsize=8)

    plt.grid(color='red', linestyle='dashed', linewidth=0.5)
    plt.title('Tu plan de vuelo: ' + fp.name)
    plt.axis([min_lon, max_lon, min_lat, max_lat])
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()



#step 6

def LoadFlightPlan (fileName):
    file=open("Datos.txt","w")

    file.write(fileName)