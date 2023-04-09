import os

def input_places_file():
    places = False
    while (not places):
        file_name = input("Masukkan nama file (dengan .txt): ")
        places = read_file(file_name)

    return places
def read_file(file_name):
    try:
        path = os.path.realpath(__file__)
        dir = os.path.dirname(path)
        dir = dir.replace('src', 'input')
        os.chdir(dir)
        with open(dir + "\\" + file_name) as file:
            # lines = file.readlines()
            line_ctr = 0
            places_count = 0
            places = []

            line = file.readline().rstrip()
            places_count = int(line[0])
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
        print(f"Tidak terdapat file dengan nama {file_name}. Harap masukan nama file yang valid!")
        places = False

    return places, matrix


# places, matrix = input_places_file()
# print(places)
# print(matrix)