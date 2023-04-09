import math

def find_index(nama_place, places):
    index = 0
    for object in places:
        if (object[0] == nama_place):
            break
        index += 1

    return index

def find_distance(element1, element2):
    delta_lat = element1[1][0] - element2[1][0]
    delta_long = element1[1][1] - element2[1][1]
    distance = math.sqrt(pow(delta_lat, 2) + pow(delta_long, 2))

    return distance

def find_heuristic_distance(goal_index, places):
    heuristic_distance_list = []

    for place in places:
        distance = find_distance(place, places[goal_index])
        heuristic_distance_list.append(distance)
        
    return heuristic_distance_list


