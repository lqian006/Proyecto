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
            OriginNumber = int(datos[0])
            DestinationNumber = int(datos[1])
            Distance = float(datos[2])
            segmento = NavSegment(OriginNumber, DestinationNumber, Distance)
            lista_segmentos.append(segmento)
        except ValueError:
            continue
