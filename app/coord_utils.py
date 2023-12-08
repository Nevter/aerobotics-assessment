import math

def calculate_next_coordinate(start_coordinate, gradient, distance_meters):
    """
    Calculate the next GPS coordinate based on a starting coordinate, gradient, and distance.

    Parameters:
    - start_coordinate: Tuple representing the starting GPS coordinate (latitude, longitude).
    - gradient: Gradient (slope) of the line.
    - distance_meters: Distance to move in meters.

    Returns:
    - Tuple representing the next GPS coordinate (latitude, longitude).
    """
    # Earth radius in meters
    earth_radius = 6371000.0

    # Convert latitude and longitude to radians
    lat1, lon1 = math.radians(start_coordinate[0]), math.radians(start_coordinate[1])

    # Calculate change in latitude and longitude
    delta_lat = (distance_meters / earth_radius) * math.cos(gradient)
    delta_lon = (distance_meters / earth_radius) * math.sin(gradient)

    # Calculate new latitude
    lat2 = lat1 + delta_lat

    # Calculate new longitude
    lon2 = lon1 + delta_lon

    # Convert latitude and longitude back to degrees
    lat2, lon2 = math.degrees(lat2), math.degrees(lon2)

    return lat2, lon2

def is_point_on_line(A, B, X, precision=1e-10):
  """
  Check if point X lies on the line segment defined by points A and B.

  Parameters:
  - A, B, X: Tuple or list representing (x, y) coordinates of points A, B, and X.
  - precision: Optional parameter to specify the precision for the check.

  Returns:
  - Tuple of the following values: 
     - True if X lies on the line segment AB within the specified precision, False otherwise.
     - If X lies on the line segment, the slope of the line.
     - If X lies on the line segment, the average distance between the trees on that line segment.
  """
  # Calculate slopes
  slope_AB = (B[1] - A[1]) / (B[0] - A[0]) if (B[0] - A[0]) != 0 else float('inf')
  slope_AX = (X[1] - A[1]) / (X[0] - A[0]) if (X[0] - A[0]) != 0 else float('inf')

  # Check if slopes are equal within the specified precision
  if abs(slope_AB - slope_AX) < precision:
      # Check if X lies within the bounding box of AB
      if (
          min(A[0], B[0]) <= X[0] <= max(A[0], B[0]) and
          min(A[1], B[1]) <= X[1] <= max(A[1], B[1])
        ):
          avg_dist = ((haversine_distance(A,X)) + haversine_distance(B, X) ) / 2
          return (True, slope_AB, avg_dist)

  return (False, 0, 0)

def get_boundary_coords(coords):
  """
  Calculate the boundary coordinates of a set of coords.

  Parameters:
  - coords: A list of tuples representing GPS coordinates (latitude, longitude).

  Returns:
  - Tuple representing the the min and max latitude, and the min and max longitude.
  """
      
  lat = [-x[0] for x in coords]
  lng = [x[1] for x in coords]
  return min(lat), max(lat), min(lng), max(lng)

def haversine_distance(coord1, coord2):
  """
  Calculate the distance on a sphere between two GPS coordinates using the Haversine formula.
  https://en.wikipedia.org/wiki/Haversine_formula
  
  Parameters:
  - coord1: Tuple (latitude, longitude) for the first coordinate.
  - coord2: Tuple (latitude, longitude) for the second coordinate.

  Returns:
  - distance: Distance between the two coordinates in meters.
  """
  R = 6371000  # Radius of the Earth in meters

  lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
  lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

  dlat = lat2 - lat1
  dlon = lon2 - lon1

  a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

  distance = R * c
  return distance


def find_center_coord(coords):
  """
  Calculate the center point of a set of coordinates.
  
  Parameters:
  - coords: A list of tuples representing the coordiantes of a point (latitude, longitude).

  Returns:
  - coordinate: A tuple representing the center coordinate (latitude, longitude).
  """

  avg_x = sum(x for x, _ in coords) / len(coords)
  avg_y = sum(y for _, y in coords) / len(coords)
  return (avg_x, avg_y)