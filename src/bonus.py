from geopy.geocoders import Nominatim
from utils import *
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def ask_locations():
        print("===== ADD LOCATION =====")
        # Create a geolocator object
        geolocator = Nominatim(user_agent="my")

        # Ask the location name from the user
        location_name = input("Enter a location name: ")

        done_location = False
        locations = []
        while (not done_location):
                # Use the geolocator to find the location
                location = geolocator.geocode(location_name, addressdetails=True)

                # Check if location is found, if not try to find closest match
                if location == None:
                        print("Location not found in Open Street Map")
                else: 
                        temp = []
                        temp.append(location.address)
                        coordinate = [location.latitude, location.longitude]
                        temp.append(coordinate)
                        locations.append(temp)
                        i = 1
                        print("\n===== LOCATIONS =====")
                        for location in locations:
                                print(f"{i}. {location[0]}")
                                i += 1
                        print("\n")

                print("Type \"done\" to stop adding locations")
                location_name = input("Enter a Location name: ")
                if (location_name == "done" or location_name == "DONE"):
                        done_location = True

        return locations

def ask_connection(locations_length):
        print("===== ADD CONNECTION =====")
        adjacency_matrix = [[0 for i in range(locations_length)] for j in range(locations_length)]
        done_connection = False
        connection_list = []

        while (not done_connection):
                continue_add_connection = input("Do you want to add connection? (y/n): ")
                while(continue_add_connection!="y" and continue_add_connection!="Y" and continue_add_connection!="n" and continue_add_connection!="N"):
                        print("Invalid input. Please enter a valid input!")
                        continue_add_connection = input("Do you want to add another connection? (y/n): ")

                if (continue_add_connection == "y" or continue_add_connection == "Y"):
                        temp = []
                        valid = False
                        while (not valid):
                                connection1 = int(input("Input the number of the first place: "))
                                if (connection1 >= 1 and connection1 <= locations_length):
                                        valid = True
                                        temp.append(connection1-1)
                                else :
                                        print("Invalid input. Please enter a valid input!")
                                
                                
                        valid = False
                        while (not valid):
                                connection2 = int(input("Input the number of the second place: "))
                                if (connection2 >= 1 and connection2 <= locations_length):
                                        valid = True
                                        temp.append(connection2-1)
                                else :
                                        print("Invalid input. Please enter a valid input!")
                    
                        adjacency_matrix[connection1-1][connection2-1] = 1
                        adjacency_matrix[connection2-1][connection1-1] = 1
                        connection_list.append(temp)

                else :
                        done_connection = True
        return connection_list, adjacency_matrix
     

def bonus():

    locations = ask_locations()

    connection_list, adjacency_matrix = ask_connection(len(locations))        

    make_adjacency_weighted_matrix(locations, adjacency_matrix)

    return locations, adjacency_matrix, connection_list

def map_visualizer(locations, connection_list, start_index, goal_index, path):
        data = []
        for i in range(len(locations)):
                data.append([locations[i][0], locations[i][1][0], locations[i][1][1], 1])

        df = pd.DataFrame(data, columns=['place', 'lat', 'lon', 'size'])

        fig = px.scatter_mapbox(df, 
                                lat='lat',
                                lon='lon',
                                color='place',
                                center={'lat':locations[start_index][1][0],
                                        'lon':locations[start_index][1][1]},
                                zoom=15,
                                size='size')
        
        # figure connection
        for i in range (len(connection_list)):
                connection = []
                connection.append([locations[connection_list[i][0]][1][0], locations[connection_list[i][0]][1][1]])
                connection.append([locations[connection_list[i][1]][1][0], locations[connection_list[i][1]][1][1]])
                df1 = pd.DataFrame(connection, columns=['lat', 'lon']) 
                if (i == 0):
                        fig.add_trace(go.Scattermapbox(
                                mode = "lines",
                                lat = df1.lat.tolist(),
                                lon = df1.lon.tolist(),
                                marker = {'color': "red", 
                                        "size": 10},
                                name = 'connection'
                        ))
                else:
                        fig.add_trace(go.Scattermapbox(
                                mode = "lines",
                                lat = df1.lat.tolist(),
                                lon = df1.lon.tolist(),
                                marker = {'color': "red", 
                                        "size": 10},
                                showlegend=False,
                                name = 'connection'
                        ))

        # figure path
        connection = []
        for i in range (len(path)):
                connection.append([locations[path[i]][1][0], locations[path[i]][1][1]])

        df2 = pd.DataFrame(connection, columns=['lat', 'lon'])          
        fig.add_trace(go.Scattermapbox(
                mode = "lines",
                lat = df2.lat.tolist(),
                lon = df2.lon.tolist(),
                marker = {'color': "green", 
                        "size": 20},
                name = 'path from start to goal'
                # title = 'Dilewati'   
        ))

        # figure start
        connection = []
        connection.append([locations[start_index][1][0], locations[start_index][1][1]])
        
        df3 = pd.DataFrame(connection, columns=['lat', 'lon'])          
        fig.add_trace(go.Scattermapbox(
                mode = "markers",
                lat = df3.lat.tolist(),
                lon = df3.lon.tolist(),
                marker = {'color': "red", 
                        "size": 40},
                name='start' 
        ))
        fig.add_trace(go.Scattermapbox(
                mode = "markers",
                lat = df3.lat.tolist(),
                lon = df3.lon.tolist(),
                marker = {'color': "white", 
                        "size": 20},
                name='start',
                showlegend=False
        ))

        # figure goal
        connection = []
        connection.append([locations[goal_index][1][0], locations[goal_index][1][1]])
        
        df3 = pd.DataFrame(connection, columns=['lat', 'lon'])          
        fig.add_trace(go.Scattermapbox(
                mode = "markers",
                lat = df3.lat.tolist(),
                lon = df3.lon.tolist(),
                marker = {'color': "blue", 
                        "size": 40},
                name='goal' 
        ))
        fig.add_trace(go.Scattermapbox(
                mode = "markers",
                lat = df3.lat.tolist(),
                lon = df3.lon.tolist(),
                marker = {'color': "white", 
                        "size": 20},
                name='goal',
                showlegend=False
        ))
        fig.update_layout(mapbox_style='open-street-map')

        fig.show()