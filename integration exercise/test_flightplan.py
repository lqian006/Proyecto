from waypoint import *
from flightplan import *

myPlan = FlightPlan("My Flight Plan")

wp1=Waypoint('Nou Camp',41.381623923229995,2.122853541678448)
wp2=Waypoint('Santiago Bernabeu',40.453030507454244,-3.6883551609249308)
wp3=Waypoint('Balaidos',42.211904178262195,-8.739772189675971)
wp4=Waypoint('Sanchez Pizjuan',37.38276157689335,-5.971691936532935)

myPlan.AddWaypoint(wp1)
myPlan.AddWaypoint(wp2)
myPlan.AddWaypoint(wp3)
myPlan.AddWaypoint(wp4)

# --- Test FindWaypoint ---
print("Testing FindWaypoint...")
wp = FindWaypoint(fp, name)
print("Found:", wp)

wp_not_found = FindWaypoint(fp, name)
print("Not found:", wp_not_found)


# --- Test RemoveWaypoint ---
print("\nTesting RemoveWaypoint...")
RemoveWaypoint(fp, name)
print("After removing BBB:", fp)

RemoveWaypoint(fp, name)
print("After trying to remove XYZ:", fp)


# --- Test FlightPlanLength ---
print("\nTesting FlightPlanLength...")
length = FlightPlanLength(fp)
print("Total length:", length)