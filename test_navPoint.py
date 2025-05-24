from navPoint import*

x=input("Introduce un número de navpoint: ").strip()
encontrado=False

for punto in lista_navpoints:
    if x == str(punto.number) or x==str(punto.name) or x == str(punto.latitude) or x == str(punto.longitude):
        print("Navigation point:", punto.number)
        print("Nombre: ", punto.name)
        print("Latitud:", punto.latitude)
        print("Longitud:", punto.longitude)
        encontrado=True
        break
else:
    print("Ese navpoint no existe.")

