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
    start_index = int(input("Masukan angka pilihan tempat asal: "))
    while (start_index<1 or start_index>len(places)):
        print("Pilihan tidak ada dalam peta. Masukan nama tempat yang valid!")
        start_index = int(input("Masukan angka pilihan tempat asal: "))

    # Ask for a valid goal name
    goal_index = int(input("Masukan angka pilihan tempat tujuan: "))
    while (goal_index<1 or goal_index>len(places) or goal_index==start_index):
        if(goal_index==start_index):
            print("Pilihan tujuan harus berbeda dari tempat asal. Masukan nama tempat yang berbeda!")
            goal_index = int(input("Masukan angka pilihan tempat tujuan: "))
        else:
            print("Pilihan tidak ada dalam peta. Masukan nama tempat yang valid!")
            goal_index = int(input("Masukan angka pilihan tempat tujuan: "))

    return start_index-1, goal_index-1
