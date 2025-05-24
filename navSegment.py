class NavSegment:
    def __init__(self, OriginNumber, DestinationNumber, Distance):
        self.OriginNumber = int(OriginNumber)
        self.DestinationNumber = int(DestinationNumber)
        self.Distance =float(Distance)

lista_segmentos=[]

with open("Cat_seg.txt", "r", encoding="utf-8") as f:
    for line in f:
        datos = line.strip().split()
        if len(datos) != 3:
            continue
        try:
            origin = int(datos[0])
            dest = int(datos[1])
            dist = float(datos[2])
            segmento = NavSegment(origin, dest, dist)
            lista_segmentos.append(segmento)
        except ValueError:
            continue


