from navAirport import*
try:
    x = input("Introduce el nombre: ").strip()
except ValueError:
    print("Entrada no válida.")

encontrado = False

for aeropuerto in aeropuerto.SIDs:
    if aeropuerto.Name_airport == x or aeropuerto.SIDs == x or aeropuerto.STARs == x:
        print("Nombre del aeropuerto:", aeropuerto.Name_airport)
        print("SID: ", aeropuerto.SIDs)
        print("STAR:", aeropuerto.STARs)
        encontrado = True

if not encontrado:
    print("No existe.")
