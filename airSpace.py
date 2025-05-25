from navPoint import *
from navSegment import *
from navAirport import *
import math
import matplotlib.pyplot as plt

class AirSpace:
    def __init__(self):
        self.NavPoints = []
        self.NavSegments = []
        self.NavAirports = []

    def get_navpoint_by_id(self, number):
        for p in self.NavPoints:
            if p.number == number:
                return p
        return None

#---Los vecinos---#

def PlotNode(airspace, name):
    # 1. Buscar el nodo seleccionado por nombre
    center = next((p for p in airspace.NavPoints if p.name.lower() == name.lower()), None)
    if center is None:
        print(f"NavPoint '{name}' no encontrado.")
        return

    center_id = center.number
    vecino_ids = set()
    segmentos_vecinos = []

    # 2. Buscar solo los segmentos que salen del nodo seleccionado
    for seg in airspace.NavSegments:
        if seg.OriginNumber == center_id:
            vecino_ids.add(seg.DestinationNumber)
            segmentos_vecinos.append(seg)

    plt.figure(figsize=(8, 6))

    # 3. Dibujar flechas de los segmentos salientes
    for seg in segmentos_vecinos:
        p1 = airspace.get_navpoint_by_id(seg.OriginNumber)
        p2 = airspace.get_navpoint_by_id(seg.DestinationNumber)
        if p1 and p2:
            dx = p2.longitude - p1.longitude
            dy = p2.latitude - p1.latitude

            # Dibujar flecha desde p1 hacia p2
            plt.arrow(p1.longitude, p1.latitude,
                      dx, dy,
                      head_width=0.05,
                      head_length=0.05,
                      fc='cyan', ec='cyan',
                      length_includes_head=True)

            # Distancia en el centro
            mx = (p1.longitude + p2.longitude) / 2
            my = (p1.latitude + p2.latitude) / 2
            plt.text(mx, my, f"{seg.Distance:.1f}", fontsize=6, color='gray', ha='center')

    # 4. Dibujar todos los nodos con colores según su rol
    for p in airspace.NavPoints:
        if p.number == center_id:
            plt.plot(p.longitude, p.latitude, 'ro', markersize=2)  # nodo seleccionado
            plt.text(p.longitude, p.latitude, p.name, fontsize=5, color='red', ha="right")
        elif p.number in vecino_ids:
            plt.plot(p.longitude, p.latitude, 'ko', markersize=2)  # vecinos
            plt.text(p.longitude, p.latitude, p.name, fontsize=5, color='black', ha="left")
        else:
            plt.plot(p.longitude, p.latitude, color='gray', marker='o', markersize=2)  # el resto
            plt.text(p.longitude, p.latitude, p.name, fontsize=5, color='gray', ha="left", va="bottom")

    # 5. Mostrar nombres de aeropuertos como en PlotAirSpace
    for airport in airspace.NavAirports:
        for p in airspace.NavPoints:
            if airport.Name_airport[:3] in p.name:
                plt.text(p.longitude, p.latitude, airport.Name_airport, fontsize=8,
                         color='darkred', ha="center", va="bottom")

    # 6. Estilo gráfico final
    plt.title(f"Vecinos salientes de '{center.name}'", fontsize=14)
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.grid(True, color='red', linestyle='--', linewidth=0.3)
    plt.axis("equal")
    plt.tight_layout()
    plt.show()


#---Reachables---#

def PlotReachable(airspace, name):
    # Buscar el nodo inicial
    start = next((p for p in airspace.NavPoints if p.name.lower() == name.lower()), None)
    if start is None:
        print(f"NavPoint '{name}' no encontrado.")
        return set()

    start_id = start.number

    # Encontrar nodos alcanzables con DFS/BFS (incluye el mismo nodo inicial)
    alcanzables = set()
    pendientes = [start_id]

    while pendientes:
        actual = pendientes.pop()
        if actual not in alcanzables:
            alcanzables.add(actual)
            # Añadir a la pila los destinos de segmentos salientes
            for seg in airspace.NavSegments:
                if seg.OriginNumber == actual and seg.DestinationNumber not in alcanzables:
                    pendientes.append(seg.DestinationNumber)

    # Filtrar segmentos que conectan nodos alcanzables
    segmentos_usados = [seg for seg in airspace.NavSegments
                       if seg.OriginNumber in alcanzables and seg.DestinationNumber in alcanzables]

    plt.figure(figsize=(8, 6))

    # Dibujar segmentos alcanzables con flechas
    for seg in segmentos_usados:
        p1 = airspace.get_navpoint_by_id(seg.OriginNumber)
        p2 = airspace.get_navpoint_by_id(seg.DestinationNumber)
        if p1 and p2:
            dx = p2.longitude - p1.longitude
            dy = p2.latitude - p1.latitude
            plt.arrow(p1.longitude, p1.latitude,
                      dx, dy,
                      head_width=0.05,
                      head_length=0.05,
                      fc='cyan', ec='cyan',
                      length_includes_head=True)
            mx = (p1.longitude + p2.longitude) / 2
            my = (p1.latitude + p2.latitude) / 2
            plt.text(mx, my, f"{seg.Distance:.1f}", fontsize=6, color='gray', ha='center')

    # Dibujar nodos
    for p in airspace.NavPoints:
        if p.number == start_id:
            plt.plot(p.longitude, p.latitude, 'ro', markersize=5)  # Nodo inicial en rojo
            plt.text(p.longitude, p.latitude, p.name, fontsize=6, color='red', ha="right")
        elif p.number in alcanzables:
            plt.plot(p.longitude, p.latitude, 'ko', markersize=4)  # Alcanzables en negro
            plt.text(p.longitude, p.latitude, p.name, fontsize=5, color='black', ha="left")
        else:
            # Opcional: nodos no alcanzables en gris (puedes comentar si no quieres mostrarlos)
            plt.plot(p.longitude, p.latitude, 'o', color='gray', markersize=2)
            plt.text(p.longitude, p.latitude, p.name, fontsize=5, color='gray', ha='left', va='bottom')

    # Mostrar aeropuertos como en otras funciones
    for airport in airspace.NavAirports:
        for p in airspace.NavPoints:
            if airport.Name_airport[:3] in p.name:
                plt.text(p.longitude, p.latitude, airport.Name_airport, fontsize=8,
                         color='darkred', ha="center", va="bottom")

    plt.title(f"Nodos alcanzables desde '{start.name}'", fontsize=14)
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.grid(True, color='red', linestyle='--', linewidth=0.3)
    plt.axis("equal")
    plt.tight_layout()
    plt.show()

    return alcanzables

#---Camino más corto---#

def PlotShortestPathSimple(airspace, start_name, end_name):
    # Buscar nodos
    start = next((p for p in airspace.NavPoints if p.name.lower() == start_name.lower()), None)
    end = next((p for p in airspace.NavPoints if p.name.lower() == end_name.lower()), None)

    if start is None:
        print(f"NavPoint '{start_name}' no encontrado.")
        return
    if end is None:
        print(f"NavPoint '{end_name}' no encontrado.")
        return

    # Inicialización
    dist = {p.number: math.inf for p in airspace.NavPoints}
    prev = {p.number: None for p in airspace.NavPoints}
    dist[start.number] = 0

    pendientes = list(dist.keys())  # lista de nodos pendientes

    while pendientes:
        # Buscar nodo con distancia mínima entre pendientes
        u = min(pendientes, key=lambda node: dist[node])
        pendientes.remove(u)

        if dist[u] == math.inf:
            break  # no quedan nodos alcanzables

        if u == end.number:
            break  # llegamos al destino

        # Revisar vecinos salientes
        for seg in airspace.NavSegments:
            if seg.OriginNumber == u:
                v = seg.DestinationNumber
                alt = dist[u] + seg.Distance
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u

    # Reconstruir camino
    if dist[end.number] == math.inf:
        print(f"No hay camino desde '{start.name}' hasta '{end.name}'.")
        return

    path = []
    u = end.number
    while u is not None:
        path.append(u)
        u = prev[u]
    path.reverse()

    # Extraer segmentos camino
    segmentos_camino = []
    for i in range(len(path) - 1):
        origen = path[i]
        destino = path[i+1]
        seg = next((s for s in airspace.NavSegments if s.OriginNumber == origen and s.DestinationNumber == destino), None)
        if seg:
            segmentos_camino.append(seg)

    # Dibujar (igual que antes)
    plt.figure(figsize=(8,6))

    for seg in airspace.NavSegments:
        p1 = airspace.get_navpoint_by_id(seg.OriginNumber)
        p2 = airspace.get_navpoint_by_id(seg.DestinationNumber)
        if p1 and p2:
            plt.plot([p1.longitude, p2.longitude], [p1.latitude, p2.latitude], color='lightgray', linewidth=0.5)

    for seg in segmentos_camino:
        p1 = airspace.get_navpoint_by_id(seg.OriginNumber)
        p2 = airspace.get_navpoint_by_id(seg.DestinationNumber)
        if p1 and p2:
            dx = p2.longitude - p1.longitude
            dy = p2.latitude - p1.latitude
            plt.arrow(p1.longitude, p1.latitude,
                      dx, dy,
                      head_width=0.07,
                      head_length=0.07,
                      fc='red', ec='red',
                      length_includes_head=True,
                      linewidth=1.5)
            mx = (p1.longitude + p2.longitude) / 2
            my = (p1.latitude + p2.latitude) / 2
            plt.text(mx, my, f"{seg.Distance:.1f}", fontsize=7, color='red', ha='center')

    for p in airspace.NavPoints:
        if p.number == start.number:
            plt.plot(p.longitude, p.latitude, 'go', markersize=6)
            plt.text(p.longitude, p.latitude, f"{p.name} (Start)", fontsize=6, color='green', ha='right')
        elif p.number == end.number:
            plt.plot(p.longitude, p.latitude, 'mo', markersize=6)
            plt.text(p.longitude, p.latitude, f"{p.name} (End)", fontsize=6, color='magenta', ha='left')
        elif p.number in path:
            plt.plot(p.longitude, p.latitude, 'ro', markersize=4)
            plt.text(p.longitude, p.latitude, p.name, fontsize=5, color='red', ha='left')
        else:
            plt.plot(p.longitude, p.latitude, 'ko', markersize=2)
            plt.text(p.longitude + 0.01, p.latitude + 0.01, p.name, fontsize=5, ha="left", va="bottom")

    for airport in airspace.NavAirports:
        for p in airspace.NavPoints:
            if airport.Name_airport[:3] in p.name:
                plt.plot(p.longitude, p.latitude, 'ro', markersize=5)
                plt.text(p.longitude, p.latitude, airport.Name_airport, fontsize=8, color='red', ha="right")

    plt.title(f"Camino más corto de '{start.name}' a '{end.name}' (Distancia: {dist[end.number]:.2f})", fontsize=14)
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.grid(True, color='red', linestyle='--', linewidth=0.3)
    plt.axis("equal")
    plt.tight_layout()
    plt.show()


#---Lee los ficheros---#

def LoadAirSpace(nav_file, seg_file, aer_file):
    space = AirSpace()

    with open(nav_file, "r", encoding="utf-8") as f:
        for line in f:
            datos = line.strip().split()
            if len(datos) == 4:
                space.NavPoints.append(NavPoint(int(datos[0]), datos[1], float(datos[2]), float(datos[3])))

    with open(seg_file, "r", encoding="utf-8") as f:
        for line in f:
            datos = line.strip().split()
            if len(datos) == 3:
                space.NavSegments.append(NavSegment(datos[0], datos[1], datos[2]))

    with open(aer_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
        for i in range(0, len(lines), 3):
            name = lines[i]
            sid = lines[i+1]
            star = lines[i+2]
            space.NavAirports.append(NavAirport(name, sid, star))

    return space


#---Hace el grafo--#

def PlotAirSpace(airspace):
    plt.figure(figsize=(8, 6))

    for seg in airspace.NavSegments:
        p1 = airspace.get_navpoint_by_id(seg.OriginNumber)
        p2 = airspace.get_navpoint_by_id(seg.DestinationNumber)
        if p1 and p2:
            plt.plot([p1.longitude, p2.longitude], [p1.latitude, p2.latitude], color='cyan', linewidth=0.5)
            mid_x = (p1.longitude + p2.longitude) / 2
            mid_y = (p1.latitude + p2.latitude) / 2
            plt.text(mid_x, mid_y, f"{seg.Distance:.1f}", fontsize=5, color='gray', ha='center')

    # Dibujar nodos (negro)
    for p in airspace.NavPoints:
        plt.plot(p.longitude, p.latitude, 'ko', markersize=2)
        plt.text(p.longitude + 0.01, p.latitude + 0.01, p.name, fontsize=5, ha="left", va="bottom")

    # Etiquetas especiales para aeropuertos
    for airport in airspace.NavAirports:
        for p in airspace.NavPoints:
            if airport.Name_airport[:3] in p.name:
                plt.plot(p.longitude, p.latitude, 'ro', markersize=5)
                plt.text(p.longitude, p.latitude, airport.Name_airport, fontsize=8, color='red', ha="right")

    # Ajustes de estilo visual
    plt.title("Gráfico del espacio aéreo de Cataluña", fontsize=12)
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.axis("equal")
    plt.grid(True, color='red', linestyle='--', linewidth=0.3)
    plt.tight_layout()
    plt.show()


