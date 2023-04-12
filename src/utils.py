import math
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

def find_index(place_name, places):
    index = -999
    for i in range(len(places)):
        if (places[i][0] == place_name):
            index = i
            break

    return index

def find_name(index, places):
    return places[index][0]

def find_distance(element1, element2):
    earth_radius = 6317             #radius in kilometers
    delta_lat = abs(element1[1][0] - element2[1][0])
    if (delta_lat >= 180) :
        delta_lat = 360 - delta_lat
    delta_long = abs(element1[1][1] - element2[1][1])
    if (delta_long >= 180) :
        delta_long = 360 - delta_long
    angle = math.sqrt(pow(delta_lat, 2) + pow(delta_long, 2))
    distance = math.pi * (angle/180) * earth_radius

    return distance

def make_heuristic_distance_list(goal_index, places):
    heuristic_distance_list = []

    for place in places:
        distance = find_distance(place, places[goal_index])
        heuristic_distance_list.append(distance)
        
    return heuristic_distance_list

def ask_start_goal(places):
    # Ask for a valid start name
    start_index = int(input("Input starting point number: "))
    while (start_index<1 or start_index>len(places)):
        print("Input is invalid!")
        start_index = int(input("Input starting point number: "))

    # Ask for a valid goal name
    goal_index = int(input("Input destination number: "))
    while (goal_index<1 or goal_index>len(places) or goal_index==start_index):
        if(goal_index==start_index):
            print("Destination should be different from starting point. Input different destination!")
            goal_index = int(input("Input destination number: "))
        else:
            print("Input is invalid. Masukan nama tempat yang valid!")
            goal_index = int(input("Input destination number: "))

    return start_index-1, goal_index-1

def make_adjacency_weighted_matrix(places, matrix):
    for i in range(len(places)):
        for j in range(len(places)):
            if (matrix[i][j] == 1):
                distance = find_distance(places[i], places[j])
                matrix[i][j] = distance
                matrix[j][i] = distance
def visualize(matrix,places, paths, start_index, goal_index):
    graph =nx.Graph()
    edges = solutionEdges(paths)

    # write node places
    placeNames = []
    n=0
    for place in places:
        placeNames.append(str(place[0]))
        graph.add_node(placeNames[n], color='r')
        n+=1

    # coloring edges
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if(matrix[i][j]!=0):
                if(checkEdges(i,j,edges)):
                    graph.add_edge(placeNames[i], placeNames[j], color = 'blue', weight=round(matrix[i][j], 2))
                else:
                    graph.add_edge(placeNames[i], placeNames[j], color = 'black', weight=round(matrix[i][j], 2))
    
    # coloring nodes
    color_map = []
    for node in graph:
        if node == places[start_index][0]:
            color_map.append('red')
        elif node == places[goal_index][0]:
            color_map.append('green')
        else: 
            color_map.append('purple') 

    # Create a layout
    pos=nx.spring_layout(graph, scale=2)
    # Draw graph nodes
    edges,colors = zip(*nx.get_edge_attributes(graph, 'color').items())
    nx.draw(graph, pos, edgelist=edges, edge_color=colors, with_labels = True, font_weight = 'light', node_color = color_map, font_size= 10, verticalalignment = 'baseline')
    edge_weight = nx.get_edge_attributes(graph, 'weight') # Get graph edges weights
    # Draw graph edges
    nx.draw_networkx_edge_labels(graph, pos, edge_labels = edge_weight)
    print("Node's Colors:\nRed is starting point and green is goal")
    print("Successfully visualize the graph. Close the NetworkX Visualization to continue!")
    plt.show()

def solutionEdges(paths):
    solution =[]
    if(len(paths)>1):
        for i in range (len(paths)-1):
            solution.append([paths[i],paths[i+1]])
    return solution

def checkEdges(node1, node2, solEdges):
    # Check if two nodes are in the edges list
    for i in range(len(solEdges)):
        if((solEdges[i][0] == node1 and solEdges[i][1] == node2)or(solEdges[i][1] == node1 and solEdges[i][0] == node2)):
            return True
    return False