from geopy.geocoders import Nominatim
from utils import *
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def bonus():
    # Create a geolocator object
    geolocator = Nominatim(user_agent="my")


    done_place = False
    places = []

    while (not done_place):
        # Get the place name from the user
        place_name = input("Enter a place name: ")

        # Use the geolocator to find the location
        location = geolocator.geocode(place_name, addressdetails=True)

        # print(location)
        # Check if location is found, if not try to find closest match
        if location == None:
            print("Place not found in Open Street Map")
        else: 
            # Print the latitude and longitude coordinates
            print("Latitude: {0}, Longitude: {1}".format(location.latitude, location.longitude))
            temp = []
            temp.append(location.address)
            coordinate = [location.latitude, location.longitude]
            temp.append(coordinate)
            places.append(temp)
            i = 1
            for place in places:
                print(f"{i}. ", end ="")
                print(place)
                i += 1
            input_done_place = input("Do you want to add another location? (y/n): ")
            while(input_done_place!="y" and input_done_place!="Y" and input_done_place!="n" and input_done_place!="N"):
                print("Invalid input. Please enter a valid input!")
                input_done_place = input("Do you want to add another location? (y/n): ")

            if (input_done_place == "n" or input_done_place == "N"):
                done_place = True

    adjacency_matrix = [[0 for i in range(len(places))] for j in range(len(places))]
    done_connection = False
    connection_list = []

    while (not done_connection):
        input_done_connection = input("Do you want to add connection? (y/n): ")
        while(input_done_connection!="y" and input_done_connection!="Y" and input_done_connection!="n" and input_done_connection!="N"):
            print("Invalid input. Please enter a valid input!")
            input_done_connection = input("Do you want to add another location? (y/n): ")

        if (input_done_connection == "y" or input_done_connection == "Y"):
            temp = []
            valid = False
            while (not valid):
                connection1 = int(input("Input the number of the first place: "))
                if (connection1 <= len(places)):
                    valid = True
                    temp.append(connection1-1)
                else :
                    print("Invalid input. Please enter a valid input!")
                    
                
            valid = False
            while (not valid):
                connection2 = int(input("Input the number of the second place: "))
                if (connection2 <= len(places)):
                    valid = True
                    temp.append(connection2-1)
                else :
                    print("Invalid input. Please enter a valid input!")
            
            adjacency_matrix[connection1-1][connection2-1] = 1
            adjacency_matrix[connection2-1][connection1-1] = 1
            connection_list.append(temp)

    
        else :
            done_connection = True

    make_adjacency_weighted_matrix(places, adjacency_matrix)

    return places, adjacency_matrix, connection_list

def map_visualizer(places, connection_list, start_index, goal_index, path):
        data = []
        for i in range(len(places)):
                data.append([places[i][0], places[i][1][0], places[i][1][1], 1])

        df = pd.DataFrame(data, columns=['place', 'lat', 'lon', 'size'])

        fig = px.scatter_mapbox(df, 
                                lat='lat',
                                lon='lon',
                                color='place',
                                center={'lat':-6.891809,
                                        'lon':107.610363},
                                zoom=15,
                                size='size')
        
        # figure connection
        for i in range (len(connection_list)):
                connection = []
                connection.append([places[connection_list[i][0]][1][0], places[connection_list[i][0]][1][1]])
                connection.append([places[connection_list[i][1]][1][0], places[connection_list[i][1]][1][1]])
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
                connection.append([places[path[i]][1][0], places[path[i]][1][1]])

        df2 = pd.DataFrame(connection, columns=['lat', 'lon'])          
        fig.add_trace(go.Scattermapbox(
                mode = "lines",
                lat = df2.lat.tolist(),
                lon = df2.lon.tolist(),
                marker = {'color': "green", 
                        "size": 20},
                name = 'path'
                # title = 'Dilewati'   
        ))

        # figure start
        connection = []
        connection.append([places[start_index][1][0], places[start_index][1][1]])
        
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
        connection.append([places[goal_index][1][0], places[goal_index][1][1]])
        
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