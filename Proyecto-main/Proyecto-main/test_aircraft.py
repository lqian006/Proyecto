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


#test 5 PlotFlightsType
print("\nExecuting PlotFlightsType")
PlotFlightsType(arrives)

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

#---- TEST V4 ----

# Test 8 - LoadDepartures
print("\nTest 8 - LoadDepartures:")

departures_test = LoadDepartures("Departures.txt")

if len(departures_test) == 0:
    print("ERROR: LoadDepartures returned empty list or file not found")
else:
    print(f"PASS: Loaded {len(departures_test)} departures")
    
    # Check first departure
    first_dep = departures_test[0]
    if first_dep.id == "ECLZN" and first_dep.DestinationAirport == "LGMK" and first_dep.TimeDeparture == "00:19":
        print("  First departure correct: ECLZN → LGMK at 00:19")
    else:
        print(f"  ERROR: First departure incorrect")
    
    # Check that arrival fields are empty
    if first_dep.OriginAirport == "" and first_dep.TimeLanding == "":
        print("  Arrival fields are empty (correct)")
    else:
        print("  ERROR: Arrival fields should be empty")
    
    # Display sample
    print(f"  Sample departures:")
    for i in range(min(5, len(departures_test))):
        dep = departures_test[i]
        print(f"    {dep.id}: → {dep.DestinationAirport} at {dep.TimeDeparture} ({dep.AirlineCompany})")

# Test 9 - MergeMovements with sample data
print("\nTest 9 - MergeMovements:")

# Create sample arrivals
sample_arrivals = [
    Aircraft("EC001", "EGLL", "10:30", "VLG"),
    Aircraft("EC002", "LFPG", "12:00", "IBE"),
    Aircraft("EC003", "EHAM", "14:00", "KLM"),
]

# Create sample departures
sample_departures = [
    Aircraft("EC001", "", "", "VLG", "LESO", "16:30"),
    Aircraft("EC002", "", "", "IBE", "LEMD", "18:00"),
    Aircraft("NIGHT1", "", "", "RYR", "EGCC", "06:00"),  # Night aircraft
]

merged_result = MergeMovements(sample_arrivals, sample_departures)

if merged_result == -1:
    print("ERROR: MergeMovements returned error code")
else:
    # Check EC001 (should be merged)
    ec001 = None
    for aircraft in merged_result:
        if aircraft.id == "EC001":
            ec001 = aircraft
            break
    
    if ec001 and ec001.OriginAirport == "EGLL" and ec001.DestinationAirport == "LESO":
        print("PASS: EC001 merged correctly")
        print(f"  Route: {ec001.OriginAirport} ({ec001.TimeLanding}) → LEBL → {ec001.DestinationAirport} ({ec001.TimeDeparture})")
    else:
        print("ERROR: EC001 not merged correctly")
    
    # Check EC003 (arrival only - no matching departure)
    ec003 = None
    for aircraft in merged_result:
        if aircraft.id == "EC003":
            ec003 = aircraft
            break
    
    if ec003 and ec003.OriginAirport == "EHAM" and ec003.DestinationAirport == "":
        print("PASS: EC003 kept as arrival-only")
    else:
        print("ERROR: EC003 should be arrival-only")
    
    # Check total count
    print(f"  Total merged aircraft: {len(merged_result)}")


# Test 10 - MergeMovements Empty List Check:
print("\nTest 10 - MergeMovements Empty List Check:")

empty_arrivals = []
normal_departures = [Aircraft("EC001", "", "", "VLG", "LESO", "16:30")]

result1 = MergeMovements(empty_arrivals, normal_departures)
if result1 == -1:
    print("PASS: Returns -1 for empty arrivals")
else:
    print("ERROR: Should return -1 for empty arrivals")

normal_arrivals = [Aircraft("EC001", "EGLL", "10:30", "VLG")]
empty_departures = []

result2 = MergeMovements(normal_arrivals, empty_departures)
if result2 == -1:
    print("PASS: Returns -1 for empty departures")
else:
    print("ERROR: Should return -1 for empty departures")


# Test 11 - NightAircraft
print("\nTest 11 - NightAircraft:")

# Create mixed aircraft list
mixed_aircraft = [
    Aircraft("EC001", "EGLL", "10:30", "VLG", "LESO", "16:30"),  # Complete
    Aircraft("EC002", "LFPG", "12:00", "IBE"),                    # Arrival only
    Aircraft("NIGHT1", "", "", "RYR", "EGCC", "06:00"),          # Night aircraft
    Aircraft("NIGHT2", "", "", "VLG", "LFPO", "05:30"),          # Night aircraft
]

night_result = NightAircraft(mixed_aircraft)

if night_result == -1:
    print("ERROR: NightAircraft returned error code")
else:
    night_count = len(night_result)
    if night_count == 2:
        print(f"PASS: Found {night_count} night aircraft")
        
        # Check IDs
        night_ids = [aircraft.id for aircraft in night_result]
        if "NIGHT1" in night_ids and "NIGHT2" in night_ids:
            print("  Correct aircraft: NIGHT1, NIGHT2")
        else:
            print(f"  ERROR: Wrong aircraft identified: {night_ids}")
    else:
        print(f"ERROR: Expected 2 night aircraft, got {night_count}")


# Test 12 - NightAircraft with empty list
print("\nTest 12 - NightAircraft Empty List Check:")

empty_list = []
result = NightAircraft(empty_list)

if result == -1:
    print("PASS: Returns -1 for empty list")
else:
    print("ERROR: Should return -1 for empty list")


# Test 13 - MergeMovements with real data files
print("\nTest 13 - MergeMovements with Real Data:")

try:
    real_arrivals = LoadArrivals("arrivals.txt")
    real_departures = LoadDepartures("Departures.txt")
    
    if len(real_arrivals) > 0 and len(real_departures) > 0:
        print(f"  Loaded {len(real_arrivals)} arrivals")
        print(f"  Loaded {len(real_departures)} departures")
        
        real_merged = MergeMovements(real_arrivals, real_departures)
        
        if real_merged != -1:
            # Count categories
            complete = sum(1 for a in real_merged if a.OriginAirport != "" and a.DestinationAirport != "")
            arrival_only = sum(1 for a in real_merged if a.OriginAirport != "" and a.DestinationAirport == "")
            
            real_night = NightAircraft(real_merged)
            night_count = len(real_night) if real_night != -1 else 0
            
            print(f"\nPASS: Merge Statistics:")
            print(f"  Total aircraft: {len(real_merged)}")
            print(f"  Complete flights: {complete}")
            print(f"  Arrival only: {arrival_only}")
            print(f"  Night aircraft: {night_count}")
            print(f"  Merge rate: {complete / len(real_merged) * 100:.1f}%")
            
            # Show sample complete flight
            for aircraft in real_merged:
                if aircraft.OriginAirport != "" and aircraft.DestinationAirport != "":
                    print(f"\n  Sample complete flight:")
                    print(f"    {aircraft.id}: {aircraft.OriginAirport} ({aircraft.TimeLanding}) → LEBL → {aircraft.DestinationAirport} ({aircraft.TimeDeparture})")
                    break
        else:
            print("ERROR: MergeMovements failed")
    else:
        print("  SKIP: Real data files not available")
except:
    print("  SKIP: Real data files not available")


print("\n" + "="*60)
print("VERSION 4 TESTS COMPLETED")
print("="*60)


























































