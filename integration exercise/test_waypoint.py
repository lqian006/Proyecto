from waypoint import *
wp = Waypoint ('A', 41.56, 1.889)
ShowWaypoint(wp)

lon1 = -8.739772189675971
lat1 = 42.211904178262195
lon2 = -5.971691936532935
lat2 = 37.38276157689335


print(haversine(lat1, lon1, lat2, lon2))

