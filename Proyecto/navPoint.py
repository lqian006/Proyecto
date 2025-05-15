with open ("Cat_nav.txt", "r", encoding="utf") as f:
    lines=f.readlines()
for i in range(len(lines)):
    datos=lines[i].strip().split()

    number=



class NavPoint:
    def __init__(self, number, name, latitude,longitude):
        self.number = number
        self.name = name
        self.latitude = latitude
        self.longitude = longitude