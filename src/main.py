from reader import *
from algorithm import *
from utils import *
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

def main():
    # Ask for a valid input file
    places, matrix = ask_file()
    
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
        astar(start_index, goal_index, places, matrix)

    visualize(matrix,places,paths,start_index,goal_index)

while True:
    main()
    print("\nDo you want to find another route? (Y/N)")
    choice = input("Choice: ")
    while (choice!='y' and choice!='Y' and choice!='n' and choice!='N'):
        print("Invalid Input\nDo you want to find another route? (Y/N)")
        choice = input("Choice: ")
    if(choice=='N' or choice=='n'):
        break