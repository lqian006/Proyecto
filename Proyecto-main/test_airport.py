from airport import *

airport = Airport ("LEBL", 41.297445, 2.0832941)
SetSchengen(airport)
PrintAirport (airport)

airport = Airport ("LAX", 41.297445, 2.0832941)
SetSchengen(airport)
PrintAirport (airport)

# Test 3: Load airports from file
print("\n Load Airports from File:")
airports = LoadAirports('airports.txt')
print(f"Loaded {len(airports)} airports:")
i = 0
while i < len(airports):
    PrintAirport(airports[i])
    print()
    i += 1

# Test 4: Add airport
print("\nAdd Airport:")
new_airport = Airport("LFPG", 49.0097, 2.5479)
SetSchengen(new_airport)
result = AddAirport(airports, new_airport)
if result == 0:
    print(f"Successfully added airport {new_airport.code}")
else:
    print(f"Failed to add airport {new_airport.code}")
print(f"Total airports: {len(airports)}")


# Test 5: Remove airport
print("\nRemove Airport:")
result = RemoveAirport(airports, "KJFK")
if result == 0:
    print("Successfully removed KJFK")
else:
    print("Failed to remove KJFK")
print(f"Total airports: {len(airports)}")


# Test 6: Save Schengen airports
print("\nSave Schengen Airports:")
result = SaveSchengenAirports(airports, 'schengen_airports.txt')
if result == 0:
    print("Schengen airports saved successfully")
    file = open('schengen_airports.txt', 'r')
    content = file.read()
    file.close()
    print("\nContents of schengen_airports.txt:")
    print(content)
else:
    print("Failed to save Schengen airports")

# Test 7: Count Schengen vs Non-Schengen
print("\n Count Schengen vs Non-Schengen")
schengen_count = 0
non_schengen_count = 0
i = 0
while i < len(airports):
    if airports[i].schengen:
        schengen_count += 1
    else:
        non_schengen_count += 1
    i += 1

print(f"Total airports: {len(airports)}")
print(f"Schengen airports: {schengen_count}")
print(f"Non-Schengen airports: {non_schengen_count}")

#Test 8: Plot
print("\n Plot Airports:")
print("Creating plot... (close the plot window to continue)")
PlotAirports(airports)

# Test 9: Map airports in Google Earth
print("\n Map Airports to Google Earth:")
MapAirports(airports)

# Test 10
airports = LoadAirports("airports.txt")   # tu archivo de datos
ok, msg, filename = MapCloseAirport(airports, "AeropuertosCercanos", "EHAM", 100)

print(ok, msg, filename)
print("Cantidad:", len([a for a in airports if a.code != "EHAM"]))
