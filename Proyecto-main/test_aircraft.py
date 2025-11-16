from aircraft import*
from airport import *

#Aquí cargamos todos los ficheros que vayamos a usar
arrives = LoadArrivals('arrivals.txt')
airports = LoadAirports("airports.txt")


#test 1 LoadArrivals
print("\nLoad arrives from File:")
print(f"Loaded {len(arrives)} arrives")


#test 2 PlotArrivals
print("\nWe are now plotting the arrivals per hour... ")
PlotArrivals(arrives)


#test 3 SaveFlights (hace falta retoque)
SaveFlights(arrives,'caca.txt')



#test 4 PlotAirlines
if __name__ == "__main__":
    print("\nPlotting the number of flights per airline")
    PlotAirlines(arrives)


#test 5 PlotFlightsType (vacío)



#test 6 MapFlights
print("\nShow trajectories in Google Earth...")
MapFlights(arrives, airports)

#test 7 LongDistanceArrivals
print("\n=== Test 7: Long Distance Arrivals ===")

long_distance = LongDistanceArrivals(arrives, airports)

print(f"Total arrivals: {len(arrives)}")
print(f"Long distance arrivals (>2000 km): {len(long_distance)}")
print("\nLong distance flights:")

for i, aircraft in enumerate(long_distance, 1):
    print(f"{i}. Flight ID: {aircraft.id}")
    print(f"   Origin: {aircraft.OriginAirport}")
    print(f"   Airline: {aircraft.AirlineCompany}")
    print(f"   Arrival Time: {aircraft.TimeLanding}")
    print()