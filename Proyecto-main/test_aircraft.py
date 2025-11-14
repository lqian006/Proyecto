from aircraft import*

print("\nLoad arrives from File:")
arrives = LoadArrivals('arrivals.txt')
print(f"Loaded {len(arrives)} arrives")

if __name__ == "__main__":
  PlotAirlines(aircrafts)

print("\nLoad arrives from File:")
arrives = LoadArrivals('arrivals.txt')
print(f"Loaded {len(arrives)} arrives")

#test PlotArrivals
PlotArrivals(arrives)

#test SaveFlights
arrives=LoadArrivals('arrivals.txt')
SaveFlights(arrives,'saved_flights.txt')