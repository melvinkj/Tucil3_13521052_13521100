from reader import *
from a_star import *
from algorithm import *
from utils import *

def main():
    # Ask for a valid input file
    places, matrix = ask_file()
    
    # Ask for a valid start and goal
    start_index, goal_index = ask_start_goal(places)

    path = UCS(matrix, start_index, goal_index)
    if path:
        print(f"Shortest path from node {start_index} to node {goal_index}: {path}")
    else:
        print(f"No path found from node {start_index} to node {goal_index}")
    astar(start_index, goal_index, places, matrix)

main()