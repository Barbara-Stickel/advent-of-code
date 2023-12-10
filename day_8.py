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
