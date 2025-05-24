from navPoint import*

x=int(input("Introduce un número de navpoint: "))

for punto in lista_navpoints:
    if punto.number == x:
        print("Nombre:", punto.name)
        print("Latitud:", punto.latitude)
        print("Longitud:", punto.longitude)
        break
else:
    print("Ese navpoint no existe.")
