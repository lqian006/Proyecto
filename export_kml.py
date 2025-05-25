def generar_kml_punto(nombre, lat, lon):
   return f"""
<Placemark>
   <name>{nombre}</name>
   <Point>
       <coordinates>{lon},{lat},0</coordinates>
   </Point>
</Placemark>
"""


def generar_kml_ruta(nombre,coordenadas):
   coord_str = "".join([f"{lon},{lat},0" for lat, lon in coordenadas])
   return f"""
<Placemark>
   <name>{nombre}</name>
   <LineString>
       <coordinates>{coord_str}</coordinates>
   </LineString>
</Placemark>
"""


def guardar_kml(nombre_archivo, elementos_kml):
    with open(nombre_archivo, "w") as f:
        f.write("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
""")
        for elemento in elementos_kml:
            f.write(elemento)
        f.write("</Document></kml>")

def exportar_airspace_kml(nombre_archivo, airspace):
    elementos = []

    for np in airspace.NavPoints:
        elementos.append(generar_kml_punto(np.name,np.lat,np.lon))

    for ap in airspace.NavAirports:
        if ap.SIDs:
            sid_name = ap.SIDs[0]
            sid_point = next((p for p in airspace.NavPoints if p.name == sid_name), None)
            if sid_point:
                elementos.append(generar_kml_punto(ap.name + "(AP)", sid_point.lat, sid_point.lon))

    guardar_kml(nombre_archivo, elementos)