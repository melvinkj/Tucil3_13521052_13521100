import os
from flask import Flask, render_template
import numpy as np

def input_places_file():
    places = False
    while (not places):
        file_name = input("Input file name (with .txt): ")
        places = read_file(file_name)

    return places

def read_file(file_name):
    try:
        path = os.path.realpath(__file__)
        dir = os.path.dirname(path)
        dir = dir.replace('src', 'test')
        os.chdir(dir)
        with open(dir + "\\" + file_name) as file:
            # lines = file.readlines()
            line_ctr = 0
            places_count = 0
            places = []

            line = file.readline().rstrip()
            places_count = int(line)
            for i in range(places_count):
                line = file.readline().rstrip()
                temp = []
                temp.append(line)
                line = file.readline().rstrip()
                coordinate = [float(num) for num in line.split(' ')]
                temp.append(coordinate)
                places.append(temp)
            
            matrix = []
            for i in range(places_count):
                line = file.readline().rstrip()
                temp = [int(num) for num in line.split(' ')]
                matrix.append(temp)


    except FileNotFoundError:
        print(f"No such file with '{file_name}'. Please input valid filename!")
        places = False
        matrix = False

    return places, matrix

def ask_file():
    places, matrix = input_places_file()
    while (not places):
        places, matrix = input_places_file()

    return places, matrix

def read_file_gui(file_name):
    try:
        path = os.path.realpath(__file__)
        dir = os.path.dirname(path)
        dir = dir.replace('src', 'test')
        os.chdir(dir)
        with open(file_name) as file:
            # lines = file.readlines()
            line_ctr = 0
            places_count = 0
            places = []

            line = file.readline().rstrip()
            places_count = int(line)
            for i in range(places_count):
                line = file.readline().rstrip()
                temp = []
                temp.append(line)
                line = file.readline().rstrip()
                coordinate = [float(num) for num in line.split(' ')]
                temp.append(coordinate)
                places.append(temp)
            
            matrix = []
            for i in range(places_count):
                line = file.readline().rstrip()
                temp = [int(num) for num in line.split(' ')]
                matrix.append(temp)


    except FileNotFoundError:
        print(f"No such file with '{file_name}'. Please input valid filename!")
        places = False
        matrix = False

    return places, matrix