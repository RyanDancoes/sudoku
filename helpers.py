
def get_house_number(row, col):
    return (row // 3) * 3 + (col // 3) + 1


def get_row(board, row_index):
    return board[row_index]


def get_column(board, col_index):
    col_array = [0]*9
    for i in range(9):
        col_array[i] = board[i][col_index]
    return col_array


def get_house(board, house_number):
    house_array = []
    house_number -= 1  # Adjust house number to be 0-based

    row_start, row_end = (house_number // 3) * 3, (house_number // 3 + 1) * 3
    col_start, col_end = (house_number % 3) * 3, (house_number % 3 + 1) * 3

    for i in range(row_start, row_end):
        for j in range(col_start, col_end):
            house_array.append(board[i][j])

    return house_array
