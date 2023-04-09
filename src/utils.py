import math

def find_index(place_name, places):
    index = -999
    for i in range(len(places)):
        if (places[i][0] == place_name):
            index = i
            break

    return index

def find_distance(element1, element2):
    delta_lat = abs(element1[1][0] - element2[1][0])
    if (delta_lat >= 180) :
        delta_lat = 360 - delta_lat
    delta_long = abs(element1[1][1] - element2[1][1])
    if (delta_long >= 180) :
        delta_long = 360 - delta_long
    distance = math.sqrt(pow(delta_lat, 2) + pow(delta_long, 2))

    return distance

def find_heuristic_distance(goal_index, places):
    heuristic_distance_list = []

    for place in places:
        distance = find_distance(place, places[goal_index])
        heuristic_distance_list.append(distance)
        
    return heuristic_distance_list

def ask_start_goal(places):
    # Ask for a valid start name
    start_name = input("Masukan nama tempat asal: ")
    start_index = find_index(start_name, places)
    while (find_index(start_name, places) == -999):
        print("Nama tempat asal tidak ada dalam peta. Masukan nama tempat yang valid!")
        start_name = input("Masukan nama tempat asal: ")
        start_index = find_index(start_name, places)

    # Ask for a valid goal name
    goal_name = input("Masukan nama tempat tujuan: ")
    goal_index = find_index(goal_name, places)
    while (find_index(goal_name, places) == -999):
        print("Nama tempat tujuan tidak ada dalam peta. Masukan nama tempat yang valid!")
        goal_name = input("Masukan nama tempat tujuan: ")
        goal_index = find_index(goal_name, places)


    return start_index, goal_index
