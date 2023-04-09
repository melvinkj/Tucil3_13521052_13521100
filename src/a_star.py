from utils import *
from queue import PriorityQueue as PQ

def astar(start_index, goal_index, places, matrix):
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

        elif ((not path_found) or (path_found and current_element[0] < best_element[0])):
            for i in range(len(matrix)):
                # if i hasn't been visited and has connection to the last node in the current_element
                if ((i not in current_element[3]) and (matrix[current_element[2]][i] != 0)):
                    new_prediction_distance = current_element[1] + heuristic_distance_list[i]
                    new_passed_distance = current_element[1] + matrix[current_element[2]][i]
                    new_curent_index = i
                    new_visited_nodes_index = current_element[3][:]
                    new_visited_nodes_index.append(i)

                    new_element = [new_prediction_distance, new_passed_distance, new_curent_index, new_visited_nodes_index]
                    queue.put(new_element)
                        
    if path_found:
        print(f"Shortest path from node {places[start_index][0]} to node {places[goal_index][0]}: {best_element[3]}")
        print(f"Cost: {best_element[1]}")
    else:
        print(f"No path found from node {places[start_index][0]} to node {places[goal_index][0]}")