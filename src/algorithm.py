from utils import *
from queue import PriorityQueue as PQ
adj_matrix = [
    [0, 3, 0, 1, 0],
    [2, 0, 4, 0, 0],
    [0, 4, 0, 5, 1],
    [100, 0, 5, 0, 3],
    [0, 0, 1, 3, 0]
]

def visitedNode(node, path):
    for i in range(len(path)):
        if (node == path[i]):
            return False
    return True

def UCS (matrix, start, goal):
    q= PQ()
    path = []
    path.append(start)
    q.put((0, start, path))
    visited = []

    while not q.empty():
        cost, currNode, currPath = q.get()
        if (currNode not in visited):
            visited.append(currNode)

            if(currNode==goal):
                return cost, currPath
            
            # Generate neighbors of the current node from adjacency matrix
            neighbors=[]
            for i in range(len(matrix[currNode])):
                if(matrix[currNode][i]!=0):
                    neighbors.append(i)

            for neighbor in neighbors:
                if((neighbor not in currPath) and (neighbor not in visited)):
                    # If neighbor is not visited before, push it to the priority queue with its cost and path
                    new_cost = cost + matrix[currNode][neighbor]  
                    new_path = currPath + [neighbor]
                    # Calculate cost to reach neighbor from current node
                    q.put((new_cost, neighbor,new_path))

    return -999,None

def astar(start_index, goal_index, places, matrix):
    heuristic_distance_list = make_heuristic_distance_list(goal_index, places)

    # Initialize the first element of the queue
    prediction_distance = heuristic_distance_list[start_index]
    passed_distance = 0
    current_index = start_index
    path_index = [start_index]
    first_element = [prediction_distance, passed_distance, current_index, path_index]

    # Initialize queue
    queue = PQ()
    queue.put(first_element)

    # Initialize the state of solution
    path_found = False
    visited_node_index = set()

    while not path_found and not queue.empty():
        current_element = queue.get()
        if (current_element[2] not in visited_node_index):
            visited_node_index.add(current_element[2])
            # Check if current_element's last node is destination
            if (current_element[2] == goal_index):
                    solution_element = current_element
                    path_found = True
            else:
                for i in range(len(matrix)):
                    # if i hasn't been visited and has connection to the last node in the current_element 
                    if ((i not in visited_node_index) and (matrix[current_element[2]][i] != 0)):
                        new_passed_distance = current_element[1] + matrix[current_element[2]][i]
                        new_prediction_distance = new_passed_distance + heuristic_distance_list[i]
                        new_curent_index = i
                        new_path_index = current_element[3][:]
                        new_path_index.append(i)

                        new_element = [new_prediction_distance, new_passed_distance, new_curent_index, new_path_index]
                        queue.put(new_element)
                        
    if path_found:
        return solution_element[1], solution_element[3]
    else:
        return -999, None