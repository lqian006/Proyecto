class NavAirport:
    def __init__(self, Name_airport, SIDs, STARs):
        self.Name_airport = Name_airport
        self.SIDs = SIDs
        self.STARs = STARs

lista_aeropuertos=[]

with open("Cat_aer.txt", "r", encoding="utf-8") as f:
    lines=[line.strip() for line in f if line.strip()]
    for i in range(0,len(lines),3):
        Name_airport=lines[i]
        SIDs=lines[i+1]
        STARs=lines[i+2]
        aeropuerto = NavAirport(Name_airport, SIDs, STARs)
        lista_aeropuertos.append(aeropuerto)
