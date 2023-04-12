from reader import *
from algorithm import *
from utils import *
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from bonus import *


def choose_input():
    print("======= Choose How to Input =======")
    print("[1] Input file")
    print("[2] Input places' name in OpenStreetMap")
    input_choice = int(input("Choose the menu number : "))
    while(input_choice!=1 and input_choice!=2):
        print("Invalid input. Please enter a valid input!")
        input_choice = int(input("Choose the menu number : "))

    return input_choice

def print_places(places):
    print("Places: ")
    i=0
    for place in places:
        i+=1
        print(f"[{i}] {place[0]}")

def choose_algorithm():
    print("Choose algorithm to calculate shortest route:")
    print("[1] UCS\n[2] A*")
    inp = int(input("Choice: "))
    while(inp!=1 and inp!=2):
        print("Invalid Input\nChoose algorithm to calculate shortest route:")
        print("[1] UCS\n[2] A*")
        inp = input("Choice: ")

    return inp

def algorithm_executor(inp, places, matrix, start_index, goal_index):
    # Execute
    if (inp==1):
        cost, paths = UCS(matrix, start_index, goal_index)
    else:
        cost, paths = astar(start_index, goal_index, places, matrix)

    # Print result    
    if paths:
        print(f"Shortest path from node {start_index+1} to node {goal_index+1}: {paths}")
        print(f"Cost: {cost}")
    else:
        print(f"No path found from node {start_index+1} to node {goal_index+1}")
    
    return cost, paths

def choose_visualizer():
    print("Choose how to visualize:")
    print("[1] Plot regular graph\n[2] Show on map\n[3] Do not visualize")
    visualizer_choice = int(input("Choice: "))
    while(visualizer_choice!=1 and visualizer_choice!=2 and visualizer_choice!= 3):
        print("Invalid input\nChoose how to visualize:")
        print("[1] Plot regular graph\n[2] Show on map\n[3] Do not visualize")
        visualizer_choice = input("Choice: ")

    return visualizer_choice

def choose_same_map():
    same_map = input("Do you want to find another route in this map again? (y/n): ")
    while(same_map!="y" and same_map!="Y" and same_map!="n" and same_map!="N"):
        print("Invalid input. Please enter a valid input!")
        same_map = input("Do you want to find another route in this map again? (y/n): ")
    
    if (same_map == "n" or same_map == "N"):
        return False
    else :
        return True

def main():

    input_choice = choose_input()

    if (input_choice == 1) :
        places, matrix = ask_file()
        connection_list = make_connection_list(matrix)
    else :
        places, matrix, connection_list = bonus()
    
    use_same_map = True
    
    while(use_same_map) :
        print_places(places)
        # Ask for a valid start and goal
        start_index, goal_index = ask_start_goal(places)

        # Ask user to choose the desired algorithm
        inp = choose_algorithm()

        # Execute desired algorithm
        cost, paths = algorithm_executor(inp, places, matrix, start_index, goal_index)
        print()

        # Ask how to visualize
        visualizer_choice = choose_visualizer()

        if (visualizer_choice == 1):
            if paths:
                visualize(matrix,places,paths,start_index,goal_index)
        elif (visualizer_choice == 2) :
            map_visualizer(places, connection_list, start_index, goal_index, paths)

        use_same_map = choose_same_map()

if __name__ == '__main__': 
    print("WELCOME!")
    while True:
        main()
        choice = input("\nDo you want to find another route on another map? (y/n): ")
        while (choice!='y' and choice!='Y' and choice!='n' and choice!='N'):
            choice = input("Invalid Input\nDo you want to find another route on another map? (y/n): ")
        if(choice=='N' or choice=='n'):
            print("\nThanks for using our program!")
            break
        print("=========================================")


