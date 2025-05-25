from airSpace import *

# Cargar espacio aéreo
space = LoadAirSpace("Cat_nav.txt", "Cat_seg.txt", "Cat_aer.txt")
print("Airspace cargado correctamente.")
print(f"NavPoints: {len(space.NavPoints)}")
print(f"NavSegments: {len(space.NavSegments)}")
print(f"NavAirports: {len(space.NavAirports)}")

# Mostrar grafo
PlotAirSpace(space)

# Vecinos
id_input = int(input("Introduce el ID de un NavPoint para ver sus vecinos: "))
vecinos = space.get_neighbors(id_input)
print("Vecinos:", vecinos)

# Alcanzables
id_input = int(input("Introduce el ID de un NavPoint para ver alcanzables: "))
alcanzables = space.reachable_from(id_input)
print("Puntos alcanzables desde", id_input, ":", alcanzables)

# Camino más corto
origin = int(input("ID origen: "))
dest = int(input("ID destino: "))
path = space.find_shortest_path(origin, dest)
if path:
    print("Camino más corto:", path)


    # OPCIONAL: mostrar grafo con camino resaltado
    def PlotPath(space, path):
        PlotAirSpace(space)  # fondo
        for i in range(len(path) - 1):
            p1 = space.get_navpoint_by_id(path[i])
            p2 = space.get_navpoint_by_id(path[i + 1])
            if p1 and p2:
                plt.plot([p1.latitude, p2.latitude], [p1.longitude, p2.longitude], 'r-', linewidth=2)
        plt.title("Camino más corto resaltado")
        plt.show()


    PlotPath(space, path)
else:
    print("No hay camino posible.")


