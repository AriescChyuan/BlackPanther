import math 

def get_coordinate(radius, center_lat, center_lon, angle_deg):
    angle_rad = math.radians(angle_deg)
    lat = center_lat + (radius/6371) * (180/math.pi) * math.cos(angle_rad)
    lon = center_lon + (radius/6371) * (180/math.pi) * math.sin(angle_rad) / math.cos(math.radians(center_lat))
    return lat, lon

radius = 10
center_lat = -35.36323458
center_lon = 149.16522392
coordinates = []

for i in range(10):
    angle = i * 36
    lat, lon = get_coordinate(radius, center_lat, center_lon, angle)
    coordinates.append((lat, lon))
print(coordinates)