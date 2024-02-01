import helpers


def naked_single(options):
    for key, val in options.items():
        if 0 in val.keys():
            if len(val[0]) == 1:
                return key
    return None


def hidden_single(house):
    total = {}
    value = 0
    for num in range(1,10):
        for key in house:
            if num in list(house[key].values())[0]:
                if num in total:
                    total[num] += 1
                else:
                    total[num] = 1

    for num in total:
        if total[num] == 1:
            value = num
            break
    for key in house:
        if value in list(house[key].values())[0]:
            return key, value

    return None, None


def naked_pair(house):
    doubles = {}
    for key, val in house.items():
        if 0 in val.keys():
            if len(val[0]) == 2:
                str_vals = [str(v) for v in val[0]]
                str_ops = ''.join(str_vals)
                if str_ops not in doubles:
                    doubles[str_ops] = 1
                else:
                    doubles[str_ops] += 1

    remove = {}
    for double in doubles:
        if doubles[double] == 2:
            key1, key2 = (), ()
            for key in house:
                if int(double[0]) in list(house[key].values())[0] and int(double[1]) in list(house[key].values())[0]:
                    if key1 != ():
                        key2 = key
                        break
                    key1 = key
            for key in house:
                if key != key1 and key != key2:
                    if int(double[0]) in list(house[key].values())[0]:
                        remove[key] = []
                        remove[key].append(int(double[0]))
                    if int(double[1]) in list(house[key].values())[0]:
                        if key in remove:
                            remove[key].append(int(double[1]))
                        else:
                            remove[key] = []
                            remove[key].append(double[1])
            if remove:
                return key1, key2, double[0], double[1], remove

    return None, None, None, None, None


def locked_candidate(row_col, house_num, house):
    freq = {}
    cell_house_num = 0
    for cell, options in row_col.items():
        if 0 in options.keys():
            for value in options[0]:
                if value in freq:
                    freq[value].append(cell)
                else:
                    freq[value] = [cell]

    cells_of_interest, value_of_interest, remove = [], 0, []
    for value in freq:
        if len(freq[value]) == 2 or len(freq[value]) == 3:
            houses = set()
            cells = freq[value]
            for cell in freq[value]:

                cell_house_num = helpers.get_house_number(cell[0], cell[1])
                houses.add(cell_house_num)

            if len(houses) == 1:
                for house_cell, val in house.items():
                    if cell_house_num == house_num:
                        if 0 in val.keys():

                            if value in list(val.values())[0]:
                                if house_cell not in cells:
                                    remove.append(house_cell)
                                    value_of_interest = value
                                    cells_of_interest = cells
    if cells_of_interest and value_of_interest and remove:
        return cells_of_interest, value_of_interest, remove

    return None, None, None


def check_everything(options, technique):
    prev_house_num = 0
    for key, val in options.items():
        house_num = helpers.get_house_number(key[0], key[1])
        row = helpers.get_row_options(options, key[0])
        col = helpers.get_col_options(options, key[1])

        if technique == 'h_s':
            key, value = hidden_single(row)
            if key:
                return key, value
            key, value = hidden_single(col)
            if key:
                return key, value

        if technique == 'n_p':
            key1, key2, value1, value2, remove = naked_pair(row)
            if key1 and key2:
                return key1, key2, value1, value2, remove
            key1, key2, value1, value2, remove = naked_pair(col)
            if key1 and key2:
                return key1, key2, value1, value2, remove

        if technique == 'l_c':
            house = helpers.get_house_options(options, house_num)
            cells, value, remove = locked_candidate(row, house_num, house)
            if cells and value and remove:
                return cells, value, remove
            cells, value, remove = locked_candidate(col, house_num, house)
            if cells and value and remove:
                return cells, value, remove

        if prev_house_num != house_num:
            house = helpers.get_house_options(options, house_num)
            prev_house_num = house_num

            if technique == 'h_s':
                key, value = hidden_single(house)
                if key:
                    return key, value

            if technique == 'n_p':
                key1, key2, value1, value2, remove = naked_pair(house)
                if key1 and key2:
                    return key1, key2, value1, value2, remove

    if technique == 'h_s':
        return None, None
    elif technique == 'n_p':
        return None, None, None, None, None
    elif technique == 'l_c':
        return None, None, None
