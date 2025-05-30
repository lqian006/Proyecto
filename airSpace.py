from navPoint import *
from navSegment import *
from navAirport import *
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

    def get_navpoint_by_name(self, name):
        """Busca un NavPoint por su nombre (insensible a mayúsculas/minúsculas)."""
        for p in self.NavPoints:
            if p.name.lower() == name.lower():
                return p
        return None

#---Los vecinos---#

def PlotNode(airspace, name):
    original_input_name = name # Store the original input name

    # 1. Buscar el nodo seleccionado por nombre
    center = next((p for p in airspace.NavPoints if p.name.lower() == name.lower()), None)

    # If not found as a NavPoint name, check if it's an Airport name
    if center is None:
        airport_found = next((a for a in airspace.NavAirports if a.Name_airport.lower() == name.lower()), None)
        if airport_found and airport_found.associated_navpoint_name:
            # If it's an airport, use its associated NavPoint for plotting
            center = next(
                (p for p in airspace.NavPoints if p.name.lower() == airport_found.associated_navpoint_name.lower()),
                None)
            if center: # If a center NavPoint was found for the airport
                original_input_name = name # Keep the original input name for the title

    if center is None:
        print(f"'{name}' (NavPoint or Airport) no encontrado o no tiene SID asociado.")
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
    plt.title(f"Vecinos salientes de '{original_input_name}'", fontsize=14) # Use original_input_name here
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.grid(True, color='red', linestyle='--', linewidth=0.3)
    plt.axis("equal")
    plt.tight_layout()



#---Reachables---#

def PlotReachable(airspace, start_node_name, ax=None):
    # Ensure ax is provided when called from Tkinter
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
        created_fig = True
    else:
        created_fig = False

    start_node = next((p for p in airspace.NavPoints if p.name.lower() == start_node_name.lower()), None)
    if not start_node:
        airport_found = next((a for a in airspace.NavAirports if a.Name_airport.lower() == start_node_name.lower()), None)
        if airport_found and airport_found.associated_navpoint_name:
            start_node = next((p for p in airspace.NavPoints if p.name.lower() == airport_found.associated_navpoint_name.lower()), None)

    if not start_node:
        raise ValueError(f"Nodo o aeropuerto '{start_node_name}' no encontrado o no tiene NavPoint asociado.")

    visited = set()
    queue = [start_node]

    while queue:
        current = queue.pop(0)
        # Check if current node's number (ID) has already been visited
        if current.number in {p.number for p in visited}:
            continue
        visited.add(current)

        for seg in airspace.NavSegments:
            if seg.OriginNumber == current.number:
                next_node = airspace.get_navpoint_by_id(seg.DestinationNumber)
                if next_node and next_node.number not in {p.number for p in visited}:
                    queue.append(next_node)
            # If segments are bidirectional, uncomment the following block:
            # elif seg.DestinationNumber == current.number:
            #     next_node = airspace.get_navpoint_by_id(seg.OriginNumber)
            #     if next_node and next_node.number not in {p.number for p in visited}:
            #         queue.append(next_node)

    ax.clear()

    # Draw all segments (light gray)
    for s in airspace.NavSegments:
        p1 = airspace.get_navpoint_by_id(s.OriginNumber)
        p2 = airspace.get_navpoint_by_id(s.DestinationNumber)
        if p1 and p2:
            ax.plot([p1.longitude, p2.longitude], [p1.latitude, p2.latitude], color='lightgray', linewidth=0.8, zorder=1)

    # Draw all NavPoints (black)
    for p in airspace.NavPoints:
        ax.plot(p.longitude, p.latitude, 'ko', markersize=2, zorder=2)
        ax.text(p.longitude + 0.01, p.latitude + 0.01, p.name, fontsize=5, ha="left", va="bottom", zorder=2)

    # Highlight reachable nodes (red)
    for p in visited:
        ax.plot(p.longitude, p.latitude, 'ro', markersize=4, zorder=3)

    # Highlight the start node (blue)
    ax.plot(start_node.longitude, start_node.latitude, 'bo', markersize=6, zorder=4)
    ax.text(start_node.longitude + 0.01, start_node.latitude + 0.01, start_node.name, fontsize=6, color='blue', ha="left", va="bottom", zorder=4)

    # Add airports (gray, as per your desired style)
    for airport in airspace.NavAirports:
        if airport.associated_navpoint_name:
            p = next((np for np in airspace.NavPoints if np.name.lower() == airport.associated_navpoint_name.lower()), None)
            if p:
                ax.plot(p.longitude, p.latitude, 'o', color='gray', markersize=3, zorder=5) # Changed to gray
                ax.text(p.longitude, p.latitude, airport.Name_airport, fontsize=7, color='gray', ha="center", va="bottom", zorder=5) # Changed to gray

    ax.set_title(f"Nodos alcanzables desde '{start_node_name}'")
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.set_aspect('equal')
    ax.grid(True, color='red', linestyle='--', linewidth=0.3)
    ax.autoscale_view()

    if created_fig:
        plt.tight_layout()
        plt.show()
#---Camino más corto---#

def PlotShortestPathSimple(airspace, start_name, end_name, ax=None):
    import math
    created_fig = False
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
        created_fig = True
    else:
        created_fig = False

    # Find start and end NavPoints (handling airport names)
    start = next((p for p in airspace.NavPoints if p.name.lower() == start_name.lower()), None)
    if not start:
        airport_start = next((a for a in airspace.NavAirports if a.Name_airport.lower() == start_name.lower()), None)
        if airport_start and airport_start.associated_navpoint_name:
            start = next((p for p in airspace.NavPoints
                          if p.name.lower() == airport_start.associated_navpoint_name.lower()), None)

    end = next((p for p in airspace.NavPoints if p.name.lower() == end_name.lower()), None)
    if not end:
        airport_end = next((a for a in airspace.NavAirports if a.Name_airport.lower() == end_name.lower()), None)
        if airport_end and airport_end.associated_navpoint_name:
            end = next((p for p in airspace.NavPoints
                        if p.name.lower() == airport_end.associated_navpoint_name.lower()), None)

    if start is None:
        raise ValueError(f"Nodo o aeropuerto '{start_name}' no encontrado o no tiene NavPoint asociado.")
    if end is None:
        raise ValueError(f"Nodo o aeropuerto '{end_name}' no encontrado o no tiene NavPoint asociado.")

    # Dijkstra's Algorithm
    dist = {p.number: math.inf for p in airspace.NavPoints}
    prev = {p.number: None for p in airspace.NavPoints}
    dist[start.number] = 0

    unvisited = {p.number for p in airspace.NavPoints}

    while unvisited:
        u_number = None
        min_dist = math.inf
        for node_num in unvisited:
            if dist[node_num] < min_dist:
                min_dist = dist[node_num]
                u_number = node_num

        if u_number is None or dist[u_number] == math.inf:
            break

        unvisited.remove(u_number)

        if u_number == end.number:
            break

        for seg in airspace.NavSegments:
            if seg.OriginNumber == u_number:
                v_number = seg.DestinationNumber
                if v_number in unvisited:
                    alt = dist[u_number] + seg.Distance
                    if alt < dist[v_number]:
                        dist[v_number] = alt
                        prev[v_number] = u_number

    if dist[end.number] == math.inf:
        ax.clear()
        ax.text(0.5, 0.5, f"No hay camino desde '{start.name}' hasta '{end.name}'.",
                horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        ax.set_title(f"Camino más corto de '{start_name}' a '{end_name}'")
        ax.set_xticks([])
        ax.set_yticks([])
        if created_fig:
            plt.tight_layout()
            plt.show()
        return

    # Reconstruct path
    path_numbers = []
    current_node_number = end.number
    while current_node_number is not None:
        path_numbers.append(current_node_number)
        current_node_number = prev[current_node_number]
    path_numbers.reverse()

    # Get segment objects for the path
    segmentos_camino = []
    for i in range(len(path_numbers) - 1):
        origen_num = path_numbers[i]
        destino_num = path_numbers[i + 1]
        seg = next((s for s in airspace.NavSegments if s.OriginNumber == origen_num and s.DestinationNumber == destino_num), None)
        if seg:
            segmentos_camino.append(seg)

    # Plotting
    ax.clear()

    # Draw all segments (light gray)
    for seg in airspace.NavSegments:
        p1 = airspace.get_navpoint_by_id(seg.OriginNumber)
        p2 = airspace.get_navpoint_by_id(seg.DestinationNumber)
        if p1 and p2:
            ax.plot([p1.longitude, p2.longitude], [p1.latitude, p2.latitude], color='lightgray', linewidth=0.5, zorder=1)

    # Draw path segments (red arrows)
    for seg in segmentos_camino:
        p1 = airspace.get_navpoint_by_id(seg.OriginNumber)
        p2 = airspace.get_navpoint_by_id(seg.DestinationNumber)
        if p1 and p2:
            dx = p2.longitude - p1.longitude
            dy = p2.latitude - p1.latitude
            ax.arrow(p1.longitude, p1.latitude, dx, dy,
                     head_width=0.07, head_length=0.07,
                     fc='red', ec='red', linewidth=1.5,
                     length_includes_head=True, zorder=3)
            mx = (p1.longitude + p2.longitude) / 2
            my = (p1.latitude + p2.latitude) / 2
            ax.text(mx, my, f"{seg.Distance:.1f}", fontsize=7, color='red', ha='center', zorder=3)

    # Draw all NavPoints
    for p in airspace.NavPoints:
        if p.number == start.number:
            ax.plot(p.longitude, p.latitude, 'go', markersize=6, zorder=4)
            ax.text(p.longitude, p.latitude, f"{start.name} (Start)", fontsize=6, color='green', ha='right', zorder=4)
        elif p.number == end.number:
            ax.plot(p.longitude, p.latitude, 'mo', markersize=6, zorder=4)
            ax.text(p.longitude, p.latitude, f"{end.name} (End)", fontsize=6, color='magenta', ha='left', zorder=4)
        elif p.number in path_numbers:
            ax.plot(p.longitude, p.latitude, 'ro', markersize=4, zorder=3)
            ax.text(p.longitude + 0.01, p.latitude + 0.01, p.name, fontsize=5, color='red', ha='left', zorder=3)
        else:
            ax.plot(p.longitude, p.latitude, 'ko', markersize=2, zorder=2)
            ax.text(p.longitude + 0.01, p.latitude + 0.01, p.name, fontsize=5, ha="left", va="bottom", zorder=2)

    # Add airports (gray, as per your desired style)
    for airport in airspace.NavAirports:
        if airport.associated_navpoint_name:
            p = next((np for np in airspace.NavPoints if np.name.lower() == airport.associated_navpoint_name.lower()), None)
            if p:
                ax.plot(p.longitude, p.latitude, 'o', color='gray', markersize=3, zorder=5) # Changed to gray
                ax.text(p.longitude, p.latitude, airport.Name_airport, fontsize=7, color='gray', ha="center", va="bottom", zorder=5) # Changed to gray


    ax.set_title(f"Camino más corto de '{start_name}' a '{end_name}' (Distancia: {dist[end.number]:.2f})",
                 fontsize=14)
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.grid(True, color='red', linestyle='--', linewidth=0.3)
    ax.set_aspect("equal")
    ax.autoscale_view()

    if created_fig:
        plt.tight_layout()
        plt.show()

#---Lee los ficheros---#

# In your main script where LoadAirSpace is defined
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
                try:
                    space.NavSegments.append(NavSegment(datos[0], datos[1], datos[2]))
                except ValueError as e:
                    print(f"Error parsing segment data for segment {datos}: {e}")


    with open(aer_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
        for i in range(0, len(lines), 3):
            name = lines[i]
            sid_raw = lines[i+1] # Keep as raw string for splitting in NavAirport init
            star_raw = lines[i+2] # Keep as raw string for splitting in NavAirport init
            airport = NavAirport(name, sid_raw, star_raw) # Pass raw strings

            # Find the NavPoint for the first SID and associate it with the airport
            if airport.SID: # Check if there's at least one SID name
                first_sid_name = airport.SID[0] # This is now a string (e.g., 'ALT.D')
                found_sid_navpoint = False
                for p in space.NavPoints:
                    # **IMPORTANT: Search by NavPoint name (p.name) here**
                    if p.name.lower() == first_sid_name.lower():
                        airport.associated_navpoint_number = p.number
                        airport.associated_navpoint_name = p.name
                        found_sid_navpoint = True
                        break
                if not found_sid_navpoint:
                    print(f"Advertencia: El NavPoint con nombre '{first_sid_name}' (primer SID de {airport.Name_airport}) no fue encontrado en Cat_nav.txt. No se podrá usar este aeropuerto para rutas.")
            else:
                print(f"Advertencia: El aeropuerto {airport.Name_airport} no tiene SIDs definidos.")

            space.NavAirports.append(airport)
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
        plt.plot(p.longitude, p.latitude, 'ko', markersize=2) # 'k' para negro, 'o' para círculo
        plt.text(p.longitude + 0.01, p.latitude + 0.01, p.name, fontsize=5, ha="left", va="bottom")

    # Etiquetas especiales para aeropuertos
    for airport in airspace.NavAirports:
        for p in airspace.NavPoints:
            # Esta es la lógica clave: si el nombre del NavPoint contiene las 3 primeras letras
            # del nombre del aeropuerto, se dibuja en rojo.
            if airport.Name_airport[:3] in p.name:
                plt.plot(p.longitude, p.latitude, 'ko', markersize=2) # 'r' para rojo, 'o' para círculo
                plt.text(p.longitude, p.latitude, airport.Name_airport, fontsize=5, ha="left", va="bottom")

    # Ajustes de estilo visual
    plt.title("Gráfico del espacio aéreo de Cataluña", fontsize=12) # ¡Nota: el título aquí es estático!
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.axis("equal")
    plt.grid(True, color='red', linestyle='--', linewidth=0.3)
    plt.tight_layout()



