import random
from timeit import default_timer as timer

import customtkinter
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pathlib import Path 

import algorithm as algo
import reader
import utils
import bonus
import os
import networkx as nx

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


class SpecsWindow(customtkinter.CTkToplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Window config
        self.resizable(False, False)

        # Create a frame to contain label
        self.specs_frame = customtkinter.CTkFrame(master=self)
        self.specs_frame.pack(padx=20, pady=20)

        # Create label
        self.specs_label = customtkinter.CTkLabel(master=self.specs_frame,
                                                  text="non",
                                                  font=('Arial', -12),
                                                  justify="left")
        self.specs_label.pack(padx=20, pady=20)


class App(customtkinter.CTk):
    # initialize inputs
    start_index = -999
    goal_index = -999
    choice = "UCS"
    places = None
    adjMatrix = None

    # Output variables 
    distance = "0 m"
    final_path = None
    cost = "0"    

    def __init__(self):
        super().__init__()

        # Font variables
        title_font = customtkinter.CTkFont(family="Arial Bold", size=-18)
        input_heading_font = customtkinter.CTkFont(family="Arial", size=-14)
        output_heading_font = customtkinter.CTkFont(family="Arial Bold", size=-14)
        placeholder_font = customtkinter.CTkFont(family="Arial", size=-12)
        select_theme_font = customtkinter.CTkFont(family="Arial", size=-12)
        button_font = customtkinter.CTkFont(family="Arial Bold", size=-12)
        status_font = customtkinter.CTkFont(family="Arial", size=-12)
        validation_label_font = customtkinter.CTkFont(family="Arial", size=-12)
        output_font = customtkinter.CTkFont(family="Arial", size=-14)

        # Initialize specs window to None
        self.specs_window = None

        # Main window configurations
        self.title("Path Finder")
        self.minsize(910, 625)

        # ============ create two frames ============

        # configure grid layout (1 x 2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.left_frame = customtkinter.CTkFrame(master=self, width=180)
        self.left_frame.grid(row=0, column=0, sticky="nswe", padx=(20, 0), pady=20)

        self.right_frame = customtkinter.CTkFrame(master=self)
        self.right_frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ left_frame ============

        # Configure grid layout (20 x 1)
        self.left_frame.grid_columnconfigure(1, weight=1)
        self.left_frame.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
        self.left_frame.grid_rowconfigure(2, minsize=20)  # space between input fields and app title
        self.left_frame.grid_rowconfigure(13, weight=1)  # empty row as spacing
        self.left_frame.grid_rowconfigure(16, minsize=20)  # empty row as spacing
        self.left_frame.grid_rowconfigure(19, minsize=20)  # empty row with minsize as spacing

        # App title
        self.app_title = customtkinter.CTkLabel(master=self.left_frame,
                                                text="Path Finder",
                                                font=title_font)
        self.app_title.grid(row=1, column=0, pady=10, padx=20)

        # input file
        self.insert_button = customtkinter.CTkButton(master=self.left_frame, text = 'Choose file',width=20,command=self.insertFile)
        self.insert_button.grid(row=3,column = 0,pady=0, padx=20)
        self.file_label = customtkinter.CTkLabel(master=self.left_frame,
                                                             text="No File Selected",
                                                             font=input_heading_font)
        self.file_label.grid(row=4, column=0, pady=0, padx=20)
        # Points
        self.starting_point_label = customtkinter.CTkLabel(master=self.left_frame,
                                                             text="Choose Starting Points:",
                                                             font=input_heading_font)
        self.starting_point_label.grid(row=5, column=0, pady=0, padx=20)

        self.comboboxStart = customtkinter.CTkOptionMenu(master=self.left_frame,
                                            font=placeholder_font,
                                            values=["Start"],
                                            command=self.optionmenu_start)
        
        self.comboboxStart.grid(row=6, column=0, pady=5, padx=20, sticky="ew")

        self.number_of_points_validation_label = customtkinter.CTkLabel(master=self.left_frame,
                                                                        text="",
                                                                        text_color="red",
                                                                        font=validation_label_font)
        self.number_of_points_validation_label.grid(row=7, column=0, pady=(0, 10), padx=20)

        # goal
        self.number_of_dimensions_label = customtkinter.CTkLabel(master=self.left_frame,
                                                                 text="Choose Goal Points:",
                                                                 font=input_heading_font)
        self.number_of_dimensions_label.grid(row=8, column=0, pady=0, padx=20)

        self.comboboxGoal = customtkinter.CTkOptionMenu(master=self.left_frame,
                                            font=placeholder_font,
                                            values=["Goal"],
                                            command=self.optionmenu_goal)
        
        self.comboboxGoal.grid(row=9, column=0, pady=5, padx=20, sticky="ew")

        self.validation_label = customtkinter.CTkLabel(master=self.left_frame,
                                                                            text="-",
                                                                            text_color="red",
                                                                            font=validation_label_font)
        self.validation_label.grid(row=10, column=0, pady=(0, 10), padx=20)

        # algorithm option
        self.comboboxAlgo = customtkinter.CTkOptionMenu(master=self.left_frame,
                                            font=placeholder_font,
                                            values=["UCS","A*"],
                                            command=self.optionmenu_algo)
        
        self.comboboxAlgo.grid(row=11, column=0, pady=5, padx=20, sticky="ew")

        # Randomize input button
        self.visualize_button = customtkinter.CTkButton(master=self.left_frame,
                                                              text="Visualize",
                                                              font=button_font,

                                                              command=self.visualize)
        self.visualize_button.grid(row=12, column=0, pady=5, padx=20)

        # Start button
        self.start_button = customtkinter.CTkButton(master=self.left_frame,
                                                    text="Bonus",
                                                    font=button_font,
                                                    command = self.map_bonus)
        self.start_button.grid(row=13, column=0, pady=5, padx=20)


        # Select GUI theme
        self.theme_label = customtkinter.CTkLabel(master=self.left_frame,
                                                  text="Select theme:",
                                                  font=select_theme_font)
        self.theme_label.grid(row=17, column=0, pady=0, padx=20, sticky="s")

        self.theme_options = customtkinter.CTkOptionMenu(master=self.left_frame,
                                                         values=["Dark", "Light", "System"],
                                                         font=select_theme_font,
                                                         command=change_appearance_mode)
        self.theme_options.grid(row=18, column=0, pady=5, padx=20, sticky="")

        # ============ right_frame ============

        # Configure grid layout (3x3) and its weights
        # weight=0 means it will not expand
        self.right_frame.rowconfigure((0, 1, 2, 3), weight=1)
        self.right_frame.columnconfigure((0, 1, 2), weight=1)
        self.right_frame.rowconfigure(1, weight=0)
        self.right_frame.columnconfigure(1, weight=0)
        self.right_frame.rowconfigure(3, weight=0)


        # Frame containing matplotlib 
        self.visualization_frame = customtkinter.CTkFrame(master=self.right_frame, fg_color="transparent")
        self.visualization_frame.grid(row=1, column=1, pady=(20, 20), padx=(20, 20), sticky="nswe")

        # Initialize a canvas for
        # This initialization is useful to avoid displaying multiple plots
        # by destroying the canvas before creating a new one every time a plot is want to be drawn
        self.visualization_canvas = FigureCanvasTkAgg(None, master=self.visualization_frame)

        # Initialize label for output when number of dimensions != 3
        self.points_output_label = customtkinter.CTkLabel(master=self.visualization_frame)

        # Output frame: contains output comparison between divide-and-conquer and brute-force
        self.output_frame = customtkinter.CTkFrame(master=self.right_frame)
        self.output_frame.grid(row=3, column=1, pady=(0, 20), padx=(20, 20), sticky="nswe")
        self.output_frame.rowconfigure((0, 1,2), weight=0)
        self.output_frame.columnconfigure((0, 1,2,3), weight=1)
        self.output_frame.grid_columnconfigure(0, weight=1)  # empty column as spacing
        self.output_frame.grid_columnconfigure(3, weight=1)  # empty column as spacing

        # output labels for divide-and-conquer algorithm
        self.path_label = customtkinter.CTkLabel(master=self.output_frame,
                                                                       text="Path",
                                                                       font=output_heading_font,
                                                                       anchor="n")
        self.path_label.grid(row=0, column=1, padx=(20, 10), pady=(20, 0))

        self.path_output_label = customtkinter.CTkLabel(master=self.output_frame,
                                                                      text="\n-------------------",
                                                                      font=output_font,
                                                                      text_color="green",
                                                                      anchor="w",
                                                                      justify="left")
        self.path_output_label.grid(row=0, column=2, padx=(0, 10), pady=(0, 20))

        self.cost_label = customtkinter.CTkLabel(master=self.output_frame,
                                                               text="Cost:",
                                                               font=output_font,
                                                               anchor="w",
                                                               justify="left")
        self.cost_label.grid(row=1, column=1, padx=(20, 10), pady=(0, 20))

        self.cost_output_label = customtkinter.CTkLabel(master=self.output_frame,
                                                                      text=f'{App.cost}',
                                                                      font=output_font,
                                                                      text_color="green",
                                                                      anchor="w",
                                                                      justify="left")
        self.cost_output_label.grid(row=1, column=2, padx=(0, 10), pady=(0, 20))
        
        # self.distance_label = customtkinter.CTkLabel(master=self.output_frame,
        #                                                        text="Distance: ",
        #                                                        font=output_font,
        #                                                        anchor="w",
        #                                                        justify="left")
        # self.distance_label.grid(row=2, column=1, padx=(20, 10), pady=(0, 20))

        # self.distance_output_label = customtkinter.CTkLabel(master=self.output_frame,
        #                                                               text=f'{App.distance}',
        #                                                               font=output_font,
        #                                                               text_color="green",
        #                                                               anchor="w",
        #                                                               justify="left")
        # self.distance_output_label.grid(row=2, column=2, padx=(0, 10), pady=(0, 20))


    
    def insertFile(self):        
        # open file
        self.filename = fd.askopenfilename(filetypes=[("Text files", "*.txt")])
        self.file_label.configure(text = Path(self.filename).name)
        self.dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.filename)
        App.places, App.adjMatrix = reader.read_file_gui(self.filename)

        place = []
        for i in range (len(App.places)):
            if(i<9):
                place.append(str(i+1)+". "+str(App.places[i][0]))
            elif(i<99):
                place.append(str(i+1)+"."+str(App.places[i][0]))
        self.comboboxStart.configure(values = (place))
        self.comboboxGoal.configure(values = place)


    def visualize(self):
        """
        Start algorithm
        """
        if (App.start_index == App.goal_index and (App.start_index!=-999 or App.goal_index!=-999)):
            self.validation_label.configure(text="Start and Goal point must be different!",
                                            text_color="red")
        elif ((App.start_index==-999 or App.goal_index==-999)):
            self.validation_label.configure(text="Please input valid place",
                                            text_color="red")
        elif(App.places and App.adjMatrix):
            if(App.choice =="UCS"):
                App.cost, App.final_path = algo.UCS(App.adjMatrix, App.start_index, App.goal_index)
            else:
                App.cost, App.final_path = algo.astar(App.start_index, App.goal_index, App.places, App.adjMatrix)

            self.validation_label.configure(text="",
                                            text_color="red")
            if App.final_path:
                fig = plt.figure(figsize=(8,5))
                ax = fig.add_subplot(111)
                ax.set_title("Shortest Path")
                graph =nx.Graph()
                edges = utils.solutionEdges(App.final_path)

                # write node places
                placeNames = []
                n=0
                for place in App.places:
                    placeNames.append(str(place[0]))
                    graph.add_node(placeNames[n], color='r')
                    n+=1

                # coloring edges
                for i in range(len(App.adjMatrix)):
                    for j in range(len(App.adjMatrix[0])):
                        if(App.adjMatrix[i][j]!=0):
                            if(utils.checkEdges(i,j,edges)):
                                graph.add_edge(placeNames[i], placeNames[j], color = 'blue', weight=round(App.adjMatrix[i][j],2))
                            else:
                                graph.add_edge(placeNames[i], placeNames[j], color = 'black', weight=round(App.adjMatrix[i][j],2))
                
                # coloring nodes
                color_map = []
                for node in graph:
                    if node == App.places[App.start_index][0]:
                        color_map.append('red')
                    elif node == App.places[App.goal_index][0]:
                        color_map.append('green')
                    else: 
                        color_map.append('purple') 

                # Create a layout
                pos=nx.spring_layout(graph, scale=2)
                # Draw graph nodes
                edges,colors = zip(*nx.get_edge_attributes(graph, 'color').items())
                nx.draw(graph, pos, edgelist=edges, edge_color=colors, with_labels = True, font_weight = 'light', node_color = color_map, font_size= 10, verticalalignment = 'baseline',ax=ax)
                edge_weight = nx.get_edge_attributes(graph, 'weight') # Get graph edges weights
                # Draw graph edges
                nx.draw_networkx_edge_labels(graph, pos, edge_labels = edge_weight)
                print("Node's Colors:\nRed is starting point and green is goal")
                print("Successfully visualize the graph. Close the NetworkX Visualization to continue!")
                # Destroy visualization canvas (if a plot is present this destroys it)
                self.visualization_canvas.get_tk_widget().destroy()

                # Destroy text output
                if self.points_output_label.cget("text") != "CTkLabel" or "":
                    self.points_output_label.pack_forget()

                # Then, draw a new plot to a Tkinter canvas
                self.visualization_canvas = FigureCanvasTkAgg(fig, master=self.visualization_frame)
                self.visualization_canvas.draw()
                self.visualization_canvas.get_tk_widget().pack()
                
                paths = ""
                count = 0
                for i in (App.final_path):
                    paths+= str(i+1)
                    count+=1
                    if(count!=len(App.final_path)):
                        paths+= " -> "
                
                self.path_output_label.configure(text =f'\n{paths}')
                self.cost_output_label.configure(text =f'{App.cost} km')

            else:
                self.path_output_label.configure(text= "\n-------------------")
                self.cost_output_label.configure(text ="0")
                self.validation_label.configure(text="No Path was Found!",
                                                text_color="red")
        else:
            self.validation_label.configure(text="Input valid file first!",
                                            text_color="red")
        self.validation_label.grid(row=10, column=0, pady=(0, 10), padx=20)

    def map_bonus(self):
        """
        Start bonus
        """
        if ((App.places and App.adjMatrix) and ((App.start_index!=-999 and App.goal_index!=-999))):
            if(App.final_path):
                connection_list = utils.make_connection_list(App.adjMatrix)
                bonus.map_visualizer(App.places, connection_list, App.start_index, App.goal_index, App.final_path)
                self.validation_label.configure(text="Open Your Local Host website!",
                                                text_color="green")
            else:
                self.validation_label.configure(text="No Path was Found!",
                                                text_color="red")
        else:
            self.validation_label.configure(text="Input valid location first!",
                                            text_color="red")
            

    def optionmenu_start(self, start):
        if(App.places):
            App.start_index = utils.find_index(start[3:],App.places)

    def optionmenu_goal(self,goal):
        if(App.places):
            App.goal_index = utils.find_index(goal[3:], App.places)

    def optionmenu_algo(self, choice):
        App.choice = choice

def change_appearance_mode(new_appearance_mode: str):
    """
    Changes the GUI theme
    :param new_appearance_mode: string: "dark", "light", or "system"
    """
    customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
