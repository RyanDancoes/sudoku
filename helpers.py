
def get_house_number(row, col):
    return (row // 3) * 3 + (col // 3) + 1


def get_row(board, row_index):
    return board[row_index]


def get_row_options(options, row_index):
    sub_options = {}
    for key, value in options.items():
        if row_index == key[0]:
            sub_options[key] = value

    return sub_options


def get_column(board, col_index):
    col_array = [0]*9
    for i in range(9):
        col_array[i] = board[i][col_index]
    return col_array


def get_col_options(options, col_index):
    sub_options = {}
    for key, value in options.items():
        if col_index == key[1]:
            sub_options[key] = value
    return sub_options


def get_house(board, house_number):
    house_array = []
    house_number -= 1  # Adjust house number to be 0-based

    row_start, row_end = (house_number // 3) * 3, (house_number // 3 + 1) * 3
    col_start, col_end = (house_number % 3) * 3, (house_number % 3 + 1) * 3

    for i in range(row_start, row_end):
        for j in range(col_start, col_end):
            house_array.append(board[i][j])

    return house_array


def get_house_options(options, house_number):
    sub_options = {}
    row_start, row_end = (house_number // 3) * 3, (house_number // 3 + 1) * 3
    col_start, col_end = (house_number % 3) * 3, (house_number % 3 + 1) * 3

    for key, value in options.items():
        if row_start <= key[0] < row_end and col_start <= key[1] < col_end:
            sub_options[key] = value

    return sub_options
