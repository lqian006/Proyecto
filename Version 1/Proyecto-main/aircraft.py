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


def PlotArrivals(aircraft):
    if len(aircraft) == 0:
        print("No airports to plot.")
        return

    schengen_count = 0
    non_schengen_count = 0

    i = 0
    while i < len(airports):
        if airports[i].schengen:
            schengen_count += 1
        else:
            non_schengen_count += 1
        i += 1

    fig, ax = plt.subplots()

    ax.bar(['Airports'], [schengen_count], label='Schengen', color='steelblue')
    ax.bar(['Airports'], [non_schengen_count], bottom=[schengen_count], label='No Schengen', color='lightcoral')
    ax.set_ylabel('Count')
    ax.set_title('Schengen airports')
    ax.legend()

    plt.show()
