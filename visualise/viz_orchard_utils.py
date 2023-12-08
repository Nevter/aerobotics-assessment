from coord_utils import *
from visualise import * 

def find_neighbour_trees(tree, all_trees, num_neighbours=4):
  """
  Find the closest coordinates to a target coordinate in a list.

  Parameters:
  - coordinates: List of tuples representing GPS coordinates.
  - target_coordinate: Tuple (latitude, longitude) for the target coordinate.
  - num_closest: Number of closest coordinates to find (default is 4).

  Returns:
  - closest: List of the closest coordinates to the target coordinate.
  """
  distances = [(coord, haversine_distance(coord, tree)) for coord in all_trees if haversine_distance(coord, tree) > 0]
  distances.sort(key=lambda x: x[1])  # Sort by distance

  closest = [coord for coord, _ in distances[:num_neighbours]]
  return closest

def get_orchard_features_with_viz(all_trees, lat_min, lat_max, lng_min, lng_max):
  features = []

  viz_count = 0
  for tree in all_trees:
    
    neighbours = find_neighbour_trees(tree, all_trees, 4)

    p, f = get_local_orchard_features(tree, neighbours)
    features += f

    if (viz_count < 20):
      canvas_loc = convert_gps_to_screen(-tree[0], tree[1], lat_min, lat_max, lng_min, lng_max)
      draw_dot(canvas_loc[0], canvas_loc[1], 12, "green")

      canvas_locs = [convert_gps_to_screen(-lat, lng, lat_min, lat_max, lng_min, lng_max) for (lat, lng) in neighbours]
      draw_dots(canvas_locs, 10, "red")

      for pair in p:
        p_locs = [convert_gps_to_screen(-lat, lng, lat_min, lat_max, lng_min, lng_max) for (lat, lng) in pair]
        draw_line(p_locs[0], p_locs[1], 3, "blue")
      viz_count +=1





  axis1 = [(slope, dist) for slope, dist in features if slope > 0]
  axis2 = [(slope, dist) for slope, dist in features if slope < 0]
  axis1Slopes, axis1Dists = zip(*axis1)
  axis2Slopes, axis2Dists = zip(*axis2)

  return [
    {
      "slope": sum(list(axis1Slopes)) / len(list(axis1Slopes)),
      "dist" : sum(list(axis1Dists)) / len(list(axis1Dists))
    },
    {
      "slope": sum(list(axis2Slopes)) / len(list(axis2Slopes)),
      "dist" : sum(list(axis2Dists)) / len(list(axis2Dists))
    },
  ]

def get_local_orchard_features(tree, neighbours):
  num_neighbours = len(neighbours)
  possible_pairs = [(i, j) for i in range(num_neighbours) for j in range(i, num_neighbours) if i != j]
  pairs = []
  features = []
  for t1, t2 in possible_pairs:
    t1_loc = neighbours[t1]
    t2_loc = neighbours[t2]

    onLine, slope, dist = is_point_on_line(t1_loc, t2_loc, tree, precision=0.5)
    if onLine:
      pairs.append([t1_loc, t2_loc])
      features.append((slope, dist))
      if len(pairs) >= 2: 
        break

  return (pairs, features)


def is_tree_at_location(check_tree, coords, precision):
  for tree in coords: 
    distance = haversine_distance(tree, check_tree)
    if distance <= precision: 
      return True
  return False


def find_tree_groups(trees, min_group_size, precision):
  groups = []
  for check_tree in trees: 
    temp = [check_tree]
    for tree in trees:
      if check_tree != tree:
        distance = haversine_distance(tree, check_tree)
        if distance <= precision: 
          temp.append(tree)

    if len(temp) >= min_group_size:
      groups.append(temp)
    
    # Remove these trees so we dont look at them again
    for t in temp: 
        trees.remove(t)
  return groups

def find_missing_trees(trees, orchard_features):
  missing_trees = []
  for tree in trees: 

    n1 = calculate_next_coordinate(tree, orchard_features[0]["slope"], orchard_features[0]["dist"])
    n2 = calculate_next_coordinate(tree, orchard_features[0]["slope"], -orchard_features[0]["dist"])
    n3 = calculate_next_coordinate(tree, orchard_features[1]["slope"], orchard_features[1]["dist"])
    n4 = calculate_next_coordinate(tree, orchard_features[1]["slope"], -orchard_features[1]["dist"])

    for neighbour in [n1,n2,n3,n4]:
      tree_exists = is_tree_at_location(neighbour, trees, precision=2.5)
      if (not tree_exists):
        missing_trees.append(neighbour)
  
  return missing_trees
