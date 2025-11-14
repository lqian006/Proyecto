import matplotlib.pyplot as plt

class Aircraft:
    def __init__(self,id,Origin,Arrival,Airline):
        self.id = id
        self.OriginAirport = Origin
        self.TimeLanding =  Arrival
        self.AirlineCompany = Airline

# Son los arrives a LEBL en un cierto día
def LoadArrivals(filename):
    arrives = []
    file = open(filename, 'r')
    line = file.readline()
    line = file.readline()

    while line:
        parts = line.strip().split()
        if len(parts) == 4:
            id = parts[0]
            Origin = parts[1]
            Arrival = parts[2]
            Airline= parts[3]

            arrive = Aircraft(id, Origin, Arrival,Airline)
            arrives.append(arrive)

        line = file.readline()

    file.close()
    return arrives

def PlotArrivals(arrives):
    if len(arrives) == 0:
        print("No airports to plot.")
        return

    arrivals=[]
    for flight in arrives:
        arrivals.append(flight.TimeLanding.strip())

    i=0
    landing_frequency=[0]*24
    while i<len(arrivals):
        hour=int(arrivals[i][:2])
        landing_frequency[hour]+=1
        i+=1

    h=0
    hours=[]
    while h < 24:
        hours.append(f'{h:02d}:00')
        h+=1

    fig, ax = plt.subplots()

    ax.bar( hours,landing_frequency,label='vuelos',color='steelblue')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Number of flights')
    ax.set_title('Landing frequency per hour')
    ax.legend()
    plt.xticks(rotation=45)
    plt.show()

def SaveFlights(arrives,filename):
    if len(arrives)==0:
        print('no se ha podido crear el fichero')
        return

    file=open(filename, 'w')
    file.write(f'AIRCRAFT ORIGIN ARRIVAL ARILINE\n')
    for flight in arrives:
        id=flight.id
        origin=flight.OriginAirport
        arrival=flight.TimeLanding
        airline=flight.AirlineCompany
        if id.strip() == '':
            id = '0'
        if origin.strip() == '':
            origin = '0'
        if arrival.strip() == '':
            arrival = '0'
        if airline.strip() == '':
            airline = '0'
        file.write(f'{id} {origin} {arrival} {airline}\n')
    file.close()
