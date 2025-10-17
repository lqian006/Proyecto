from waypoint import *
from flightplan import *

myPlan = FlightPlan("My Flight Plan")

wp1 = Waypoint('Nou Camp', 41.381623923229995, 2.122853541678448)
wp2 = Waypoint('Santiago Bernabeu', 40.453030507454244, -3.6883551609249308)
wp3 = Waypoint('Balaidos', 42.211904178262195, -8.739772189675971)
wp4 = Waypoint('Sanchez Pizjuan', 37.38276157689335, -5.971691936532935)

AddWaypoint(myPlan, wp1)
AddWaypoint(myPlan, wp2)
AddWaypoint(myPlan, wp3)
AddWaypoint(myPlan, wp4)

print("== Mostrar plan ==")
ShowFlightPlan(myPlan)

print("\n== Test FindWaypoint ==")
found = FindWaypoint(myPlan, 'Balaidos')
print("Found:", found.name if found else "None")

print("\n== Test RemoveWaypoint ==")
RemoveWaypoint(myPlan, 'Balaidos')
ShowFlightPlan(myPlan)

print("\n== Test FlightPlanLength ==")
print("Longitud total:", FlightPlanLength(myPlan), "km")

#paso 6
LoadFlightPlan(myPlan)
