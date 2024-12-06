from pathlib import Path

import numpy as np
import pandas as pd
import math


def get_data(day):
    folder = Path("input")

    with open(folder / f"day_{day}.txt", "r") as f:
        data = f.read().splitlines()

    return data

def get_instruction(data):
    
    instruction = data[0]

    dict_map = {}
    for row in data[2:]:
        k, v = row.split(" = (")
        left, right = v.split(", ")
        right = right[:-1]

        dict_map[k] = {"L": left, "R": right}

    instruction = list(instruction)

    return instruction, dict_map


def d8_p1():
    
    data = get_data(8)
    instruction, dict_map = get_instruction(data)
    count_direction = 0
    next_value = "AAA"

    while next_value != "ZZZ":
        for direction in instruction:
            if count_direction % 1_000 == 0:
                print(count_direction, next_value)

            next_value = dict_map[next_value][direction]
            count_direction += 1

            if next_value == "ZZZ":
                break

    return count_direction

def d8_p2():

    data = get_data(8)
    instruction, dict_map = get_instruction(data)

    count_direction = 0

    starting_point = []
    for k in dict_map.keys():
        if k[-1] == "A":
            starting_point.append(k)

    dict_count = {}

    for next_value in starting_point:

        count_direction = 0
        initial_value = next_value

        dict_count[initial_value] = []

        number_z_found = 0
        while number_z_found < 5:
            for direction in instruction:

                next_value = dict_map[next_value][direction]
                count_direction += 1

                if next_value[-1] == "Z":
                    number_z_found += 1
                    dict_count[initial_value].append((count_direction, next_value))

                if number_z_found == 5:
                    break

    result = []
    for k, v in dict_count.items():
        result.append(v[0][0])

    return math.lcm(*result)


def get_extrapolated_number(row, extrapolation_end):

    if extrapolation_end:
        number_position = -1
    else:
        number_position = 0
    
    list_data = row.split(" ")

    array_data = np.array([int(x) for x in list_data if len(x) > 0], dtype=np.int64)
    last_data_point = np.array([], dtype=np.int64)

    all_zeros = False
    counter = 0
    while not all_zeros:
        new_np = np.array([array_data[x+1] - array_data[x] for x in range(len(array_data)-1)], dtype=np.int64)
        last_data_point = np.append(last_data_point, array_data[number_position])
        if set(new_np) != set([0]):
            array_data = new_np
            all_zeros = False
        else:
            all_zeros = True

        counter += 1
        if counter % 100 == 0:
            print(counter, array_data)

    last_data_point = last_data_point[::-1]

    extrapolated_number = 0
    for v in last_data_point:

        if extrapolation_end:
            extrapolated_number = v + extrapolated_number
        else:
            extrapolated_number = v - extrapolated_number

    return extrapolated_number


def d9_p1():
    data = get_data(9)
    result = 0 
    for row in data:
        result += get_extrapolated_number(row, extrapolation_end=True)

    return result

def d9_p2():
    data = get_data(9)
    result = 0 
    for row in data:
        result += get_extrapolated_number(row, extrapolation_end=False)

    return result


def get_directions():
    directions = {
        (-1, 0): ["|", "F", "7"],
        (0, 1): ["-", "7", "J"],
        (1, 0): ["|", "L", "J"],
        (0, -1): ["-", "F", "L"]
    }
    allowed_directions = {("|", -1, 0): (-1, 0),
                      ("|", 1, 0): (1, 0),
                      ("-", 0, -1): (0, -1),
                      ("-", 0, 1): (0, 1),

                      ("F", -1, 0): (0, 1),
                      ("F", 0, -1): (1, 0),

                      ("L", 1, 0): (0, 1),
                      ("L", 0, -1): (-1, 0),

                      ("J", 1, 0): (0, -1),
                      ("J", 0, 1): (-1, 0),

                      ("7", -1, 0): (0, -1),
                      ("7", 0, 1): (1, 0)
                      }
    return directions, allowed_directions


def d10_p1():

    data = get_data(10)

    data_array = np.array([list(row) for row in data])

    start_row, start_col = np.where(data_array == 'S')

    directions, allowed_directions = get_directions()

    potential_start = []
    symbols = []
    for (i, j), values in directions.items():
        if data_array[start_row + i, start_col + j] in values:
            potential_start.append((start_row + i, start_col + j))
            symbols.append(data_array[start_row + i, start_col + j])

    row, col = potential_start[0]
    end_row, end_col = potential_start[1]

    prev_i = (row - start_row)[0]
    prev_j = (col - start_col)[0]

    s = symbols[0][0]

    counter = 0
    end_of_loop = False

    while not end_of_loop:
        i, j = allowed_directions[(s, prev_i, prev_j)]

        row += i
        col += j
        s = data_array[row, col][0]
        counter += 1

        if row == end_row and col == end_col:
            end_of_loop = True
        else:
            prev_i, prev_j = i, j
    
    return counter / 2 + 1


def initialize_np_o_i(data):
    data_array = np.array([list(row) for row in data])
    np_o_i = np.zeros(shape=data_array.shape)
    

    directions, allowed_directions = get_directions()

    start_row, start_col = np.where(data_array == 'S')
    np_o_i[start_row, start_col] = 1

    potential_start = []
    symbols = []
    for (i, j), values in directions.items():
        if data_array[start_row + i, start_col + j] in values:
            potential_start.append((start_row + i, start_col + j))
            symbols.append(data_array[start_row + i, start_col + j])

            np_o_i[start_row + i, start_col + j] = 1

    row, col = potential_start[0]
    end_row, end_col = potential_start[1]

    prev_i = (row - start_row)[0]
    prev_j = (col - start_col)[0]

    s = symbols[0][0]

    counter = 0
    end_of_loop = False

    while not end_of_loop:
        i, j = allowed_directions[(s, prev_i, prev_j)]

        row += i
        col += j
        s = data_array[row, col][0]
        np_o_i[row, col] = 1
        counter += 1

        if row == end_row and col == end_col:
            end_of_loop = True
        else:
            prev_i, prev_j = i, j

    return data_array, np_o_i

def find_o_from_corners(np_o_i):
    stop_for_loop = False

    for direction in ["tl", "tr", "bl", "br"]:
        stop_for_loop = False
        for i in range(np_o_i.shape[0]):
            for j in range(np_o_i.shape[1]):

                if direction == "tl":
                    pass
                elif direction == "tr":
                    j = np_o_i.shape[1] - j - 1
                elif direction == "bl":
                    i = np_o_i.shape[0] - i - 1
                elif direction == "br":
                    i = np_o_i.shape[0] - i - 1
                    j = np_o_i.shape[1] - j - 1

                if np_o_i[i, j] == 0:
                    np_o_i[i, j] = 2
                elif np_o_i[i, j] == 1:
                    stop_for_loop = True

                if stop_for_loop:
                    break
            if stop_for_loop:
                break

    print(len(np.where(np_o_i == 0)[0]))

    for direction in ["tl", "tr", "bl", "br"]:
        stop_for_loop = False
        for j in range(np_o_i.shape[1]):
            for i in range(np_o_i.shape[0]):
            
                if direction == "tl":
                    pass
                elif direction == "tr":
                    j = np_o_i.shape[1] - j - 1
                elif direction == "bl":
                    i = np_o_i.shape[0] - i - 1
                elif direction == "br":
                    i = np_o_i.shape[0] - i - 1
                    j = np_o_i.shape[1] - j - 1

                if np_o_i[i, j] == 0:
                    np_o_i[i, j] = 2
                elif np_o_i[i, j] == 1:
                    stop_for_loop = True

                if stop_for_loop:
                    break
            if stop_for_loop:
                break
    print(len(np.where(np_o_i == 0)[0]))

    return np_o_i