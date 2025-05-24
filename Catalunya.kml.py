from export_kml import *

elementos = []

for np in airSpace.NavPoints:
    elementos.append(generar_kml_punto(np.name,np.lat,np.lon))

guardar_kml("Catalunya.kml", elementos)