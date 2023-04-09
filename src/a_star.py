from queue import PriorityQueue as PQ
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


def astar(start_name, goal_name, places, matrix):
    start_index = find_index(start_name, places)
    goal_index = find_index(goal_name, places)

    heuristic_distance_list = find_heuristic_distance(goal_index, places)

    # Initialize the first element of the queue
    prediction_distance = heuristic_distance_list[start_index]
    passed_distance = 0
    current_index = start_index
    visited_nodes_index = [start_index]
    first_element = [prediction_distance, passed_distance, current_index, visited_nodes_index]

    # Initialize queue
    queue = PQ()
    queue.put(first_element)

    # Initialize the state of solution
    path_found = False

    while not queue.empty():
        current_element = queue.get()

        # Check if current_element's last node is destination
        if (current_element[2] == goal_index):
            if (not path_found):
                best_element = current_element
                path_found = True
            else:
                # Check if the solution is the best solution so far
                if (current_element[1] < best_element[1]):
                    best_element = current_element

        else :
            for i in range(len(matrix)):
                # if i hasn't been visited and has connection to the last node in the current_element
                if ((i not in current_element[3]) and (matrix[current_element[2]][i] != -999)):
                    new_prediction_distance = current_element[1] + heuristic_distance_list[i]
                    new_passed_distance = current_element[1] + matrix[current_element[2]][i]
                    new_curent_index = i
                    new_visited_nodes_index = current_element[3][:]
                    new_visited_nodes_index.append(i)

                    new_element = [new_prediction_distance, new_passed_distance, new_curent_index, new_visited_nodes_index]
                    queue.put(new_element)
                        
    if path_found:
        print(f"Shortest path from node {start_name} to node {goal_name}: {best_element[3]}")
        print(f"Cost: {best_element[1]}")
    else:
        print(f"No path found from node {start_name} to node {goal_name}")