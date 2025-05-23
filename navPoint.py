class NavPoint:
    def __init__(self, number, name, latitude, longitude):
        self.number = number
        self.name = name
        self.latitude = latitude
        self.longitude = longitude


lista_navpoints = []

with open("Cat_nav.txt", "r", encoding="utf-8") as f:
    for line in f:
        datos = line.strip().split()
        number = int(datos[0])
        name = datos[1]
        latitude = float(datos[2])
        longitude = float(datos[3])
        punto = NavPoint(number, name, latitude, longitude)
        lista_navpoints.append(punto)


x=int(input("Introduce un número de navpoint: "))

for punto in lista_navpoints:
    if punto.number == x:
        print("Nombre:", punto.name)
        print("Latitud:", punto.latitude)
        print("Longitud:", punto.longitude)
        break
else:
    print("Ese navpoint no existe.")
