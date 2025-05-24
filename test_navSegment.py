from navSegment import *

try:
    x = float(input("Introduce un número de navpoint o distancia: "))
except ValueError:
    print("Entrada no válida. Por favor, introduce un número.")

encontrado = False

for segmento in lista_segmentos:
    if segmento.OriginNumber == x or segmento.DestinationNumber == x or segmento.Distance == x:
        print("Origen (ID):", segmento.OriginNumber)
        print("Destino (ID):", segmento.DestinationNumber)
        print("Distancia:", segmento.Distance)
        encontrado = True

if not encontrado:
    print("Ese segmento no existe.")



