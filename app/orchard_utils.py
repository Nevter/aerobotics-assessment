from app.coord_utils import *


def find_neighbour_trees(tree, all_trees, num_neighbours=4):
  """
  Find the closest tree to a target tree in a list.

  Parameters:
  - tree: Tuple (latitude, longitude) for the target tree.
  - all_trees: List of tuples representing GPS coordinates of all trees.
  - num_neighbours: Number of closest trees to find (default is 4).

  Returns:
  - closest: List of the closest tree coordinates to the target tree.
  """
  distances = [(coord, haversine_distance(coord, tree)) for coord in all_trees if haversine_distance(coord, tree) > 0]
  distances.sort(key=lambda x: x[1])  # Sort by distance

  closest = [coord for coord, _ in distances[:num_neighbours]]
  return closest

def get_orchard_features(all_trees):
  """
  Find the slope and distance between trees on each major axis of an orchard.

  Parameters:
  - all_trees: List of tuples representing GPS coordinates of all trees.

  Returns:
  - features: A list of the major axes of the orchard, each containing a dictionary of the slope
              and average distance between trees on that axis. 
  """

  features = []
  pairs = []
  for tree in all_trees:
    neighbours = find_neighbour_trees(tree, all_trees, 4)
    p, f = get_local_orchard_features(tree, neighbours)
    features += f
    pairs += p
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
  """
  Find the slope and distance between a tree and its neighbours.

  Parameters:
  - tree: A tuple (lat, lng) of a tree
  - neighbours: List of tuples representing GPS coordinates of neighbour trees.

  Returns:
  - features: A list of tuples representing the slope and average distance between trees on the found
              major axis. 
  - pairs: The trees that form a pair of trees on a major axis
  """
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


def is_tree_at_location(check_tree, all_trees, precision):
  """
  Check if there is a tree at a given location.

  Parameters:
  - check_tree: A GPS coordinate of a potential tree.
  - all_trees: List of tuples representing GPS coordinates of all trees.
  - precision: How close the check_tree should be to an actual tree to confirm that the tree exists.

  Returns:
  - boolean: True if there is a tree at the check_tree location, false otherwise. 
  """
  for tree in all_trees: 
    distance = haversine_distance(tree, check_tree)
    if distance <= precision: 
      return True
  return False


def find_tree_groups(trees, min_group_size, precision):
  """
  Group sets of trees

  Parameters:
  - all_trees: List of tuples representing GPS coordinates of the trees to group.
  - min_group_size: How many trees should be located together to count as a group.
  - precision: How close the trees should be to each other to form a group.

  Returns:
  - groups: A list of lists of groups of trees (a tuple (lat, lng))
  """
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
  """
  Finds locations where there could be a tree in the orchard, but there isnt.

  Parameters:
  - trees: List of tuples representing GPS coordinates of the trees in the orchard.
  - orchard_features: A list of the major axes of the orchard, each containing a dictionary of the slope
                      and average distance between trees on that axis. 

  Returns:
  - missing_trees: A list of the locations where there could be trees in the orchard (lat, lng)
  """

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
