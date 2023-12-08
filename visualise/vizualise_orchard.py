import json
import random
from visualise import *
from orchard_utils import *
import copy

def main():
  f = open('response_1701867391762.json')
  data = json.load(f)
  results = data['results']
  all_trees = [(float(s['latitude']), float(s['longitude'])) for s in results]
  
  # Visualisation
  lat_min, lat_max, lng_min, lng_max = get_boundary_coords(all_trees)
  init_viz()
  canvas_loc = [convert_gps_to_screen(-lat, lng, lat_min, lat_max, lng_min, lng_max) for (lat, lng) in all_trees]
  draw_dots(canvas_loc, 5, "black")

  input("Press enter to continue")

  ###########################
  ### GET FEATURES

  features = get_orchard_features_with_viz(all_trees, lat_min, lat_max, lng_min, lng_max)

  input("Press enter to continue")

  ###########################
  ### Visualise estimations
  turtle.clear()
  draw_dots(canvas_loc, 5, "black")
  for i in range(0,10): 
    start_tree = all_trees[random.randint(0, len(all_trees)-1)]
    start_tree_loc = [convert_gps_to_screen(-lat, lng, lat_min, lat_max, lng_min, lng_max) for (lat, lng) in [start_tree]]
    draw_dots(start_tree_loc, 15, "green")

    n1 = calculate_next_coordinate(start_tree, features[0]["slope"], features[0]["dist"])
    n2 = calculate_next_coordinate(start_tree, features[0]["slope"], -features[0]["dist"])
    n3 = calculate_next_coordinate(start_tree, features[1]["slope"], features[1]["dist"])
    n4 = calculate_next_coordinate(start_tree, features[1]["slope"], -features[1]["dist"])
    neighbour_trees_locs = [convert_gps_to_screen(-lat, lng, lat_min, lat_max, lng_min, lng_max) for (lat, lng) in [n1, n2, n3, n4]]
    draw_dots(neighbour_trees_locs, 10, "red")

  input("Press enter to continue")
  
  ###########################
  ### Find and visualise missing trees

  missing_trees = find_missing_trees(all_trees, features)

  # Visualise
  turtle.clear()
  draw_dots(canvas_loc, 5, "black")
  missing_tree_locs = [convert_gps_to_screen(-lat, lng, lat_min, lat_max, lng_min, lng_max) for (lat, lng) in missing_trees]
  draw_dots(missing_tree_locs, 4, "red")
  
  input("Press enter to continue")

  ###########################
  ### Reject missing trees that arent in groups of 3 or more times and visualise 
  m_trees = copy.deepcopy(missing_trees)
  missing_tree_groups = find_tree_groups(m_trees, min_group_size=3, precision=2.5)

  # Visualise
  turtle.clear()
  draw_dots(canvas_loc, 5, "black")
  flat_list = [item for sublist in missing_tree_groups for item in sublist]
  missing_tree_locs = [convert_gps_to_screen(-lat, lng, lat_min, lat_max, lng_min, lng_max) for (lat, lng) in flat_list]
  draw_dots(missing_tree_locs, 4, "red")

  input("Press enter to continue")  

  ###########################
  ### Find average loc of missing trees and visualise
  missing_tree_coords = [find_center_coord(missing_tree_group) for missing_tree_group in missing_tree_groups]
  
  # # Visualise
  turtle.clear()
  draw_dots(canvas_loc, 5, "black")
  missing_tree_locs = [convert_gps_to_screen(-lat, lng, lat_min, lat_max, lng_min, lng_max) for (lat, lng) in missing_tree_coords]
  draw_dots(missing_tree_locs, 10, "red")

  input("Press enter to continue") 

  ###########################
  ### Find potentially missing trees and visualise
  p_m_trees = copy.deepcopy(missing_trees)
  potentially_missing_tree_groups = find_tree_groups(p_m_trees, min_group_size=2, precision=2.5)

  # Visualise
  turtle.clear()
  draw_dots(canvas_loc, 5, "black")
  flat_list = [item for sublist in potentially_missing_tree_groups for item in sublist]
  potentially_missing_tree_locs = [convert_gps_to_screen(-lat, lng, lat_min, lat_max, lng_min, lng_max) for (lat, lng) in flat_list]
  draw_dots(potentially_missing_tree_locs, 4, "red")

  input("Press enter to continue")

  potentially_missing_tree_coords = [find_center_coord(potentially_missing_tree_group) for potentially_missing_tree_group in potentially_missing_tree_groups]
  potentially_missing_tree_coords = [coord for coord in potentially_missing_tree_coords if coord not in missing_tree_coords]
  
  # Visualise
  turtle.clear()
  draw_dots(canvas_loc, 5, "black")
  poten_missing_tree_locs = [convert_gps_to_screen(-lat, lng, lat_min, lat_max, lng_min, lng_max) for (lat, lng) in potentially_missing_tree_coords]
  draw_dots(missing_tree_locs, 10, "red")
  draw_dots(poten_missing_tree_locs, 8, "orange")

  response = {"missing_trees": [{"lat":lat,"lng":lng} for lat,lng in missing_tree_coords], 
              "potentially_missing_trees": [{"lat":lat,"lng":lng} for lat,lng in potentially_missing_tree_coords]}
  print(response)
  
  input("Press enter end")
  turtle.clear()
  turtle.bye()
  
if __name__ == "__main__":
  main()

