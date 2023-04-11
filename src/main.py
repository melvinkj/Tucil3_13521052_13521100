from reader import *
from algorithm import *
from utils import *
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from bonus import *

def main():

    print("======= Main Menu =======")
    print("1. Input through file")
    print("2. Input through map")
    menu = int(input("Choose the menu number : "))
    while(menu!=1 and menu!=2):
        print("Invalid input. Please enter a valid input!")
        menu = int(input("Choose the menu number : "))

    if (menu == 1) :
        places, matrix = ask_file()
    else :
        places, matrix, connection_list = bonus()

    
    # Ask for a valid input file
    
    print("Places: ")
    i=0
    for place in places:
        i+=1
        print(f"[{i}] {place[0]}")
    # Ask for a valid start and goal
    start_index, goal_index = ask_start_goal(places)

    print("Choose algorithm to calculate shortest route:")
    print("[1] UCS\n[2] A*")
    inp = int(input("Choice: "))
    while(inp!=1 and inp!=2):
        print("Invalid Input\nChoose algorithm to calculate shortest route:")
        print("[1] UCS\n[2] A*")
        inp = input("Choice: ")
    if (inp==1):
        cost, paths = UCS(matrix, start_index, goal_index)
        if paths:
            print(f"Shortest path from node {start_index} to node {goal_index}: {paths}")
            print(f"Cost: {cost}")
        else:
            print(f"No path found from node {start_index} to node {goal_index}")
    else:
        cost, paths = astar(start_index, goal_index, places, matrix)
        if paths:
            print(f"Shortest path from node {start_index} to node {goal_index}: {paths}")
            print(f"Cost: {cost}")
        else:
            print(f"No path found from node {start_index} to node {goal_index}")
    print()

    if (menu == 1):
        if paths:
            visualize(matrix,places,paths,start_index,goal_index)
    else :
        map_visualizer(places, connection_list, start_index, goal_index, paths)
while True:
    main()
    print("\nDo you want to find another route? (Y/N)")
    choice = input("Choice: ")
    while (choice!='y' and choice!='Y' and choice!='n' and choice!='N'):
        print("Invalid Input\nDo you want to find another route? (Y/N)")
        choice = input("Choice: ")
    if(choice=='N' or choice=='n'):
        print("Thanks for using our program!")
        break
    print("=========================================")