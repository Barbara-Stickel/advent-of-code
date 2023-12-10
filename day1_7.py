from pathlib import Path
import numpy as np
import pandas as pd

def get_data(day):
    folder = Path("input")

    with open(folder / f"day_{day}.txt", "r") as f:
        data = f.read().splitlines()

    return data


def _d1_p1_get_digit(value):
    for letter in value:
        try:
            digit = int(letter)
            break
        except ValueError:
            pass

    return digit


def d1_p1():
    data = get_data(1)

    all_numbers = []
    for value in data:
        value = list(value)
        
        first_digit = _d1_p1_get_digit(value)

        value.reverse()
        second_digit = _d1_p1_get_digit(value)
        
        all_numbers.append(int(f"{first_digit}{second_digit}"))
    
    return sum(all_numbers)


def _d1_p2_get_digit(value, is_reverse=False):

    list_numbers = [
        "one", "two", "three", "four", "five",
        "six", "seven", "eight", "nine"]

    if is_reverse:
        list_numbers = [x[::-1] for x in list_numbers]
        value = value[::-1]

    list_value = list(value)

    for i, letter in enumerate(list_value):
        try:
            digit = int(letter)

            print("aa")
            break
        except ValueError:
            break_loop = False
            for number in list_numbers:
                if number == value[i:i+len(number)]:
                    digit = number
                    break_loop = True

                    print(break_loop)
                
                if break_loop:
                    break
            if break_loop:
                break
    
    dict_numbers = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9}
    
    if is_reverse:
        dict_numbers = {k[::-1]: v for k, v in dict_numbers.items()}
    
    if digit in dict_numbers.keys():
        digit = dict_numbers[digit]
    return digit


def d1_p2():
    data = get_data(1)

    all_numbers = []
    for value in data:
         
        first_digit = _d1_p2_get_digit(value, is_reverse=False)
        second_digit = _d1_p2_get_digit(value, is_reverse=True)
        
        all_numbers.append(int(f"{first_digit}{second_digit}"))
    
    return sum(all_numbers)


def d2_p1():
    data = get_data(2)

    list_possible_games = []

    for game_string in data:
        game_number, games = game_string.split(":")
        game_number = int(game_number.split(" ")[1])

        list_game = games[1:].split("; ")

        is_possible_game = True
        for sets in list_game:
            list_set = sets.split(", ")
            for set in list_set:
                value, color = set.split(" ")
                if (color == "red") and int(value) > 12:
                    is_possible_game = False
                    break
                elif (color == "green") and int(value) > 13:
                    is_possible_game = False
                    break
                elif (color == "blue") and int(value) > 14:
                    is_possible_game = False
                    break

        if is_possible_game:
            list_possible_games.append(game_number)

    return sum(list_possible_games)

def d2_p2():
    data = get_data(2)
    list_power_games = []

    for game_string in data:
        dict_max_color = {"red": 1, "green": 1, "blue": 1}
        game_number, games = game_string.split(":")
        game_number = int(game_number.split(" ")[1])

        list_game = games[1:].split("; ")

        is_possible_game = True
        for sets in list_game:
            list_set = sets.split(", ")
            for set in list_set:
                value, color = set.split(" ")
                dict_max_color[color] = max(dict_max_color[color], int(value))

        power = dict_max_color["red"] * dict_max_color["green"] * dict_max_color["blue"]
        list_power_games.append(power)

    return sum(list_power_games)

def d3_p1():
    data = get_data(3)

    array = np.array([list(row) for row in data])

    width = array.shape[0]

    list_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    list_numbers = [str(i) for i in list_numbers]

    array_done = np.zeros(array.shape, dtype=int)
    list_final_numbers = []
    for i, row in enumerate(array):
        for j, char in enumerate(row):
            if array_done[i, j] == 0:
                if char == ".":
                    array_done[i, j] = -1
                
                elif char in list_numbers:
                    # print(char)
                    # Getting the number and the length
                    array_done[i, j] = 1
                    number = str(char)
                    for k in range(1, width - j):

                        if array[i, j + k] in list_numbers:
                            array_done[i, j + k] = 1
                            number += str(array[i, j + k])
                        else:
                            break
                    number_length = len(number)

                    has_a_special_character = False
                    # Checking the row before:
                    if i > 0:
                        for k in range(0, number_length):
                            if array[i-1, j+k] != ".":
                                has_a_special_character = True

                    # print(1, has_a_special_character)

                    # Checking the row after:
                    if i < width - 1:
                        for k in range(0, number_length):
                            if array[i+1, j+k] != ".":
                                has_a_special_character = True

                    # print(2, has_a_special_character)

                    # Checking the column before:
                    if j > 0:
                        if array[i, j-1] != ".":
                            has_a_special_character = True
                        
                        if i > 0:
                            if array[i-1, j-1] != ".":
                                has_a_special_character = True
                        if i < width - 1:
                            if array[i+1, j-1] != ".":
                                has_a_special_character = True
                    
                    # Checking the column after:
                    if j + number_length < width - 1:
                        if array[i, j+number_length] != ".":
                            has_a_special_character = True

                        if i > 0:
                            if array[i-1, j+number_length] != ".":
                                has_a_special_character = True
                        if i < width - 1:
                            if array[i+1, j+number_length] != ".":
                                has_a_special_character = True

                    # print(3, has_a_special_character)
                
                    if has_a_special_character:
                        list_final_numbers.append(int(number))         
                else:
                    array_done[i, j] = 2       
    return sum(list_final_numbers)

def _add_gear(row, col, number, dict_gear, array):

    if array[row, col] == "*":
        if (row, col) in dict_gear.keys():
            dict_gear[(row, col)].append(number)
        else:
            dict_gear[(row, col)]= [number]
    
    return dict_gear


def d3_p2():
    data = get_data(3)

    array = np.array([list(row) for row in data])
    width = array.shape[0]

    list_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    list_numbers = [str(i) for i in list_numbers]

    dict_gear = {}

    array_done = np.zeros(array.shape, dtype=int)
    list_final_numbers = []
    for i, row in enumerate(array):
        for j, char in enumerate(row):
            if array_done[i, j] == 0:
                if char == ".":
                    array_done[i, j] = -1
                
                elif char in list_numbers:
                    # print(char)
                    # Getting the number and the length
                    array_done[i, j] = 1
                    number = str(char)
                    for k in range(1, width - j):

                        if array[i, j + k] in list_numbers:
                            array_done[i, j + k] = 1
                            number += str(array[i, j + k])
                        else:
                            break
                    
                    number_length = len(number)

                    has_a_special_character = False
                    # Checking the row before:
                    if i > 0:
                        for k in range(0, number_length):
                            row = i - 1
                            col = j + k
                            dict_gear = _add_gear(row, col, number, dict_gear, array)

                    # print(1, has_a_special_character)

                    # Checking the row after:
                    if i < width - 1:
                        for k in range(0, number_length):
                            row = i + 1
                            col = j + k
                            dict_gear = _add_gear(row, col, number, dict_gear, array)

                    # Checking the column before:
                    if j > 0:

                        col = j - 1
                        
                        row = i
                        dict_gear = _add_gear(row, col, number, dict_gear, array)
                        
                        if i > 0:
                            row = i - 1
                            dict_gear = _add_gear(row, col, number, dict_gear, array)

                        if i < width - 1:
                            row = i + 1
                            dict_gear = _add_gear(row, col, number, dict_gear, array)
                    
                    # Checking the column after:
                    if j + number_length < width - 1:
                        col = j + number_length

                        row = i
                        dict_gear = _add_gear(row, col, number, dict_gear, array)

                        if i > 0:
                            row = i-1
                            dict_gear = _add_gear(row, col, number, dict_gear, array)

                        if i < width - 1:                        
                            row = i+1
                            dict_gear = _add_gear(row, col, number, dict_gear, array)
        
                else:
                    array_done[i, j] = 2
    
    list_gear = [int(dict_gear[key][0]) * int(dict_gear[key][1])
                 for key in dict_gear.keys() if len(dict_gear[key]) == 2]
    
    return sum(list_gear)


def _get_score(numbers):
    w_number, my_number = numbers.split(" | ")

    w_number = [int(x) for x in w_number.split(" ") if len(x) > 0]
    my_number = [int(x) for x in my_number.split(" ") if len(x) > 0]

    count_winning_number = 0

    for n in my_number:
        if n in w_number:
            count_winning_number += 1
    if count_winning_number in [0, 1]:
        score = count_winning_number
    elif count_winning_number > 1:
        score = 2 ** (count_winning_number - 1)
    else:
        print("error")

    return count_winning_number, score


def d4_p1():
    data = get_data(4)
    final_score = 0

    for row in data:    
        _, numbers = row.split(":")
        _, score = _get_score(numbers)

        final_score += score

    return final_score


def d4_p2():
    data = get_data(4)

    dict_cards = {}
    for row in data:
        card, numbers = row.split(":")
        card_number = int(card.split(" ")[-1])

        if card_number not in dict_cards:
            dict_cards[card_number] = 0

        # The card initial card
        dict_cards[card_number] += 1
        count_winning_number, _ = _get_score(numbers)

        if count_winning_number > 0:
            for j in range(1, count_winning_number + 1):
                if card_number + j not in dict_cards:
                    dict_cards[card_number + j] = 0
                
                dict_cards[card_number + j] += 1 * dict_cards[card_number]

    return sum(dict_cards.values())


# -----------------
# Day 5

def _get_next_destination(seed_number, source_name):

    for k in dict_data.keys():
        if k[0] == source_name:
            desti_name = k[1]
            list_range = dict_data[k]
            break

    has_found_destination = False
    for d, s, r in list_range:
        if s <= seed_number <= s + r - 1:
            new_seed_number = d + seed_number - s
            has_found_destination = True

        if has_found_destination:
            break

    if not has_found_destination:
        new_seed_number = seed_number

    return new_seed_number, desti_name

def create_dict_data_map_1(data):
    dict_data = {}

    for row in data[2:]:
        if len(row) == 0:  
            pass
        elif row[-1] == ":":
            source_name, destination_name = row.split(" ")[0].split("-to-")
            dict_data[(source_name, destination_name)] = []
        elif len(row) > 0:
            dict_data[(source_name, destination_name)].append(
                list(map(int, row.split(" "))))

    return dict_data

def create_dict_data_map_2(dict_data_temp):
    dict_data = {}

    for key, value in dict_data_temp.items():
        print(key)
        df = pd.DataFrame(value, columns=["d", "s", "r"])

        df.sort_values("s", inplace=True)
        df.reset_index(inplace=True, drop=True)

        len_df = len(df)

        for i in range(len_df - 1):
            row = df.iloc[i]
            if row["s"] + row["r"] < df.iloc[i + 1]["s"]:
                s = row["s"] + row["r"]
                r = df.iloc[i + 1]["s"] - s
                df = pd.concat([df, pd.DataFrame([[s, s, r]], columns=["d", "s", "r"])])

        df.sort_values("s", inplace=True)
        df.reset_index(inplace=True, drop=True)


        for i in range(1, len(df) - 1):
            row = df.iloc[i]
            # print(row["s"] + row["r"] == df.iloc[i + 1]["s"])

        list_range = []
        for i, row in df.iterrows():
            list_range.append(row.to_list())

        dict_data[key] = list_range

    return dict_data

def get_next_destination1(seed_number, source_name, dict_data):

    for k in dict_data.keys():
        if k[0] == source_name:
            desti_name = k[1]
            list_range = dict_data[k]
            break
    
    minimum_number_above = None
    has_found_destination = False
    for d, s, r in list_range:
        if s <= seed_number <= s + r - 1:
            new_seed_number = d + seed_number - s
            range_number = r
            has_found_destination = True

        elif s > seed_number:
            if minimum_number_above is None:
                minimum_number_above = s
            else:
                minimum_number_above = min(s, minimum_number_above)
    
        if has_found_destination:
            break

    if not has_found_destination:
        new_seed_number = seed_number
        if minimum_number_above is None:
            range_number = minimum_number_above
        else:
            range_number = max(minimum_number_above - seed_number - 1, 1)

    return new_seed_number, desti_name, range_number

def get_next_destination(seed_number, source_name, dict_data):

    for k in dict_data.keys():
        if k[0] == source_name:
            desti_name = k[1]
            list_range = dict_data[k]
            break
    
    has_found_destination = False
    for d, s, r in list_range:
        if s <= seed_number <= s + r - 1:
            new_seed_number = d + seed_number - s
            range_number = s + r - seed_number
            has_found_destination = True
    
        if has_found_destination:
            break

    if not has_found_destination:
        new_seed_number = seed_number
        range_number = None

    return new_seed_number, desti_name, range_number


def d5_p1(data, dict_data):
    seed_list = data[0].split(": ")[1].split(" ")
    seed_list = [int(x) for x in seed_list]

    # Initialization
    minimum_location = None
    dict_path = {}

    locations_done = []


    for i, seed_number in enumerate(seed_list):
        
        print(i, locations_done)
        is_done = False
        for sn, rn in locations_done:
            if sn <= seed_number <= sn + rn - 1:
                is_done = True

        if is_done:
            continue
        
        source_name = "seed"
        min_range_number = None
        original_number = seed_number

        dict_path[original_number] = []
        while source_name != "location":
            seed_number, source_name, range_number = get_next_destination(seed_number, source_name, dict_data)
            dict_path[original_number].append(range_number)

            if range_number is not None:
                min_range_number = min(min_range_number, range_number) if min_range_number is not None else range_number


        if minimum_location is None:
            minimum_location = seed_number
        else:
            minimum_location = min(minimum_location, seed_number)

        locations_done.append((seed_number, min_range_number))

    return minimum_location


def get_seed_part_2(data):
    seed_list = data[0].split(": ")[1].split(" ")
    seed_list = [int(x) for x in seed_list]

    all_seeds = []
    for i, seed_number in enumerate(seed_list):
        if i%2 == 0:
            all_seeds.append((seed_number, seed_list[i + 1]))

    return all_seeds


def get_one_seed(seed_number, dict_data):
    source_name = "seed"
    min_range_number = None

    while source_name != "location":
        seed_number, source_name, range_number = get_next_destination(seed_number, source_name, dict_data)
        # print(source_name, range_number)

        if range_number is not None:
            min_range_number = min(min_range_number, range_number) if min_range_number is not None else range_number

    return seed_number, min_range_number


def d5_p2(data):

    dict_data_temp = create_dict_data_map_1(data)
    dict_data = create_dict_data_map_2(dict_data_temp)

    all_seeds = get_seed_part_2(data)

    # Initialization
    minimum_location = None
    count = 0

    for i, tuple_seed_number in enumerate(all_seeds):
        seed_number, range_seed = tuple_seed_number

        final_seed = seed_number + range_seed

        while seed_number <= final_seed:
            count += 1
            
            location, range_done = get_one_seed(seed_number, dict_data)

            seed_number += range_done
            minimum_location = min(minimum_location, location) if minimum_location is not None else location

# -----------------
# Day 6

def d6_p1():
    list_data = [(48, 261), (93, 1192), (84, 1019), (66, 1063)]

    all_result = 1

    for total_time, total_distance in list_data:

        result = 0

        for time_button in range(1, total_time):

            speed = time_button

            remaining_time = total_time - time_button
            distance = remaining_time * speed

            if distance > total_distance:
                result += 1
        
        all_result *= result

    return all_result


def d6_p2():
    total_time = 48_938_466
    total_distance = 261_119_210_191_063

    result = []

    for time_button in range(1, total_time, 1000):

        speed = time_button

        remaining_time = total_time - time_button
        distance = remaining_time * speed

        if distance > total_distance:
            result.append((time_button, distance))


    df = pd.DataFrame(result).set_index(0)
    df.sort_index(inplace=True)

    low_number = df.index[0]

    for time_button in range(low_number - 2000, low_number + 10, 1):
        speed = time_button

        remaining_time = total_time - time_button
        distance = remaining_time * speed

        if distance > total_distance:
            result.append((time_button, distance))

    df = pd.DataFrame(result).set_index(0)
    df.sort_index(inplace=True)

    high_number = df.index[-1]

    for time_button in range(high_number, high_number + 2000, 1):
        speed = time_button

        remaining_time = total_time - time_button
        distance = remaining_time * speed

        if distance > total_distance:
            result.append((time_button, distance))

    df = pd.DataFrame(result).set_index(0)
    df.sort_index(inplace=True)

    return df.index[-1] - df.index[0] + 1

# -----------------
# Day 7

def replace_letter(letter):
    if letter == "A":
        return 14
    elif letter == "K":
        return 13
    elif letter == "Q":
        return 12
    elif letter == "J":
        return 11
    elif letter == "T":
        return 10
    else:
        return int(letter)
    
def d7_p1():
    data = get_data(7)
    dict_cards = {}
    for row in data:
        card, bid = row.split(" ")
        card = tuple(card)
        card = tuple(map(replace_letter, card))
        dict_cards[card] = bid

    list_cards = list(dict_cards.keys())

    dict_kind = {
        "5": [],
        "4": [],
        "3 + 2": [],
        "3 + 1 + 1": [],
        "2 + 2 + 1": [],
        "2 + 1 + 1 + 1": [],
        "1 + 1 + 1 + 1 + 1": [],
    }

    for card in list_cards:
        s = pd.Series(list(card)).value_counts()

        if s.max() == 5:
            dict_kind["5"].append(card)
        elif s.max() == 4:
            dict_kind["4"].append(card)
        elif s.max() == 3:
            if s.min() == 2:
                dict_kind["3 + 2"].append(card)
            elif s.min() == 1:
                dict_kind["3 + 1 + 1"].append(card)
            else:
                print("error", card)
        elif s.max() == 2:
            if len(s) == 3:
                dict_kind["2 + 2 + 1"].append(card)
            elif len(s) == 4:
                dict_kind["2 + 1 + 1 + 1"].append(card)
            else:
                print("error", card)
        elif s.max() == 1:
            dict_kind["1 + 1 + 1 + 1 + 1"].append(card)

    for k, v in dict_kind.items():
        v = sorted(v)
        dict_kind[k] = v

    order_hand = list(dict_kind.keys())[::-1]

    rank = 0
    result = 0
    for hand in order_hand:
        for card in dict_kind[hand]:
            rank += 1
            result += rank * int(dict_cards[card])

    return result

def replace_letter_v2(letter):
    if letter == "A":
        return 14
    elif letter == "K":
        return 13
    elif letter == "Q":
        return 12
    elif letter == "J":
        return 1
    elif letter == "T":
        return 10
    else:
        return int(letter)
    
def d7_p2():
    data = get_data(7)
    dict_cards = {}
    for row in data:
        card, bid = row.split(" ")
        card = tuple(card)
        card = tuple(map(replace_letter_v2, card))
        dict_cards[card] = bid

    list_cards = list(dict_cards.keys())

    dict_kind = {
        "5": [],
        "4": [],
        "3 + 2": [],
        "3 + 1 + 1": [],
        "2 + 2 + 1": [],
        "2 + 1 + 1 + 1": [],
        "1 + 1 + 1 + 1 + 1": [],
    }

    for card in list_cards:
        s = pd.Series(list(card)).value_counts()

        
        if (1 in s.index) and (s.max() < 5):
            nb_jocker = s[1]
            s.drop(1, inplace=True)
            s.iloc[0] += nb_jocker

        if s.max() == 5:
            dict_kind["5"].append(card)
        elif s.max() == 4:
            dict_kind["4"].append(card)
        elif s.max() == 3:
            if s.min() == 2:
                dict_kind["3 + 2"].append(card)
            elif s.min() == 1:
                dict_kind["3 + 1 + 1"].append(card)
            else:
                print("error", card)
        elif s.max() == 2:
            if len(s) == 3:
                dict_kind["2 + 2 + 1"].append(card)
            elif len(s) == 4:
                dict_kind["2 + 1 + 1 + 1"].append(card)
            else:
                print("error", card)
                print(s)
        elif s.max() == 1:
            dict_kind["1 + 1 + 1 + 1 + 1"].append(card)

    for k, v in dict_kind.items():
        v = sorted(v)
        dict_kind[k] = v

    order_hand = list(dict_kind.keys())[::-1]

    rank = 0
    result = 0
    for hand in order_hand:
        for card in dict_kind[hand]:
            rank += 1
            result += rank * int(dict_cards[card])

    return result