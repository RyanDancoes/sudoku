import numpy as np
import build
import copy


def calculate_options(board):
    filled_board = copy.deepcopy(board)

    for r in range(9):
        for c in range(9):
            options = []
            if not board[r][c]:
                options = write_notes(board, r, c)

            filled_board[r][c] = options

    combined = {(i, j): {board[i][j]: filled_board[i][j]} for i in range(9) for j in range(9)}
    return combined


def write_notes(board, r, c):
    house_num = build.get_house_number(r, c)
    options = []
    full = (
        build.get_row(board, r)
        + build.get_column(board, c)
        + build.get_house(board, house_num)
    )
    filled = []
    for i in full:
        if i != 0 and i not in filled:
            filled.append(i)

    for i in range(1, 10):
        if i not in filled:
            options.append(i)
    return options

def make_board(is_random):
    board = [[0] * 9 for _ in range(9)]
    is_empty = np.random.choice((True, False), 1)

    for i in range(9):
        for j in range(9):
            if not is_empty:
                if is_random:
                    board[i][j] = np.random.randint(1, 10)
                else:
                    board[i][j] = 0
            is_empty = np.random.choice((True, False), 1)

    return board


def translate(options):
    board = []
    row = []
    for cell in options:
        cell_value = list(options[cell].keys())[0]
        row.append(cell_value)
        if len(row) % 9 == 0:
            board.append(row)
            row = []
    return board


def print_board(options):
    count = 0
    for key, val in options.items():
        if count % 3 == 0 and count != 0 and count % 9 != 0:
            print(" || ", end='')
        if count % 9 == 0 and count % 27 != 0:
            print("\n"+"-"*113)
        if count % 27 == 0:
            print("\n"+"=" * 113)
        if 0 in val.keys():
            str_vals = [str(v) for v in list(val.values())[0]]
            print(f" {''.join(str_vals):^9s} ", end="")
        else:
            print(f" {list(val.keys())[0]:^9d} ", end="")
        if count % 3 != 2:
            print("|", end='')
        count += 1
    print('\n')


def game(board_load=None, is_random=False):
    first_go = True
    _options = {}
    while True:
        if not board_load:
            if first_go:
                _board = make_board(is_random)

            else:
                _board = translate(_options)
        else:
            _board = board_load

        _options = calculate_options(_board)
        print_board(_options)

        edit = input("Enter a cell to edit: [11] ")
        tup = (int(edit[0]) - 1, int(edit[1]) - 1)
        if len(list(_options[tup].values())[0]) > 1:
            str_vals = [str(v) for v in list(_options[tup].values())[0]]
            num_setting = input(f"Available numbers: {', '.join(str_vals)}. Pick one and whether to [i]nput or [c]ross out: [1i] ")
            num = int(num_setting[0])
            setting = num_setting[1]
            if setting == 'i':
                _options[tup] = {num: []}
            elif setting == 'c':
                _options[tup][0].remove(num)
        else:
            undo = input("There's a number here. Would you like to remove it? [y/n] ")
            if undo == 'y':

                _options[tup] = {0: [1, 2, 3, 4, 5, 6, 7, 8, 9]}

        input("Enter to continue.")
        first_go = False


def load():
    board = []
    for r in range(9):
        row_str = input(f"Input row {r+1} numbers (0 for blank) [030070009] ")
        row = [int(num) for num in row_str]
        board.append(row)
    print(board)

    input()
    game(board_load=board)

load()