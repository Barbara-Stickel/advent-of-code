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