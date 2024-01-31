import numpy as np
import helpers
import copy
import techniques
import techniques2


def calculate_options(board):
    filled_board = copy.deepcopy(board)

    for r in range(9):
        for c in range(9):
            options = []
            if not board[r][c]:
                options = write_notes(board, r, c)

            filled_board[r][c] = options

    combined = {}
    for i in range(9):
        for j in range(9):
            combined[(i, j)] = {board[i][j]: filled_board[i][j]}

    return combined


def write_notes(board, r, c):
    house_num = helpers.get_house_number(r, c)
    options = []
    full = (
        helpers.get_row(board, r)
        + helpers.get_column(board, c)
        + helpers.get_house(board, house_num)
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
            print("|| ", end='')
        if count % 9 == 0 and count % 27 != 0:
            print("\n"+"-"*111)
        if count % 27 == 0:
            print("\n"+"=" * 111)
        if 0 in val.keys():
            str_vals = [str(v) for v in list(val.values())[0]]
            print(f" {''.join(str_vals):^9s} ", end="")
        else:

            print(f" {list(val.keys())[0]:^9d}*", end="")
        if count % 3 != 2:
            print("|", end='')
        count += 1
    print('\n')


def solver(options):

    while True:
        interest = techniques.naked_single(options)
        if interest:
            print(f"Naked single at {interest[0]+1}{interest[1]+1}.")
            break
        interest, value = techniques.check_everything(options, 'h_s')
        if interest:
            print(f"Hidden single of {value} at {interest[0]+1}{interest[1]+1}.")
            break
        interest1, interest2, value1, value2, remove = techniques.check_everything(options, 'n_p')
        if interest1 and interest2:
            print(f"Naked pair of {value1} and {value2} at {interest1[0] + 1}{interest1[1] + 1} and "
                  f"{interest2[0] + 1}{interest2[1] + 1}.")
            print('Cross off at: ', end='')
            for cell in remove:
                str_vals = [str(val) for val in remove[cell]]
                print(f"{cell[0]+1}{cell[1]+1}: {','.join(str_vals)}", end='     ')

            print()
            break
        else:
            input('No solutions.')
            break


def editor(options):
    edit = input("Enter a cell to edit: [11] ")
    tup = (int(edit[0]) - 1, int(edit[1]) - 1)
    setting = ''

    if len(list(options[tup].values())[0]) > 1 or list(options[tup].keys())[0] == 0:
        str_vals = [str(v) for v in list(options[tup].values())[0]]
        num_setting = input(f"Available numbers: {', '.join(str_vals)}. \n"
                            f"Pick one and whether to [i]nput or [c]ross out: [1i] ")
        num = int(num_setting[0])
        setting = num_setting[1]
        if setting == 'i':
            options[tup] = {num: []}
        elif setting == 'c':
            options[tup][0].pop(options[tup][0].index(num))

    else:
        undo = input("There's a number here. Would you like to remove it? [y/n] ")
        if undo == 'y':
            options[tup] = {0: [1, 2, 3, 4, 5, 6, 7, 8, 9]}

    return options, setting


def game(board_load=None, is_random=False):
    first_go = True
    _options = {}
    setting = ''
    while True:
        if not board_load:
            if first_go:
                _board = make_board(is_random)

            else:
                _board = translate(_options)
        else:
            if first_go:
                _board = board_load
            else:
                _board = translate(_options)

        if setting != 'c':
            _options = calculate_options(_board)

        if first_go:
            print_board(_options)

        choice = input("[E]dit or [S]olve? ").lower()

        if choice == 's':
            solver(_options)
        elif choice == 'e':
            _options, setting = editor(_options)
        elif choice == 'p':
            print_board(_options)
        elif choice == 'q':
            quit()

        first_go = False


def load():
    # board = []
    # for r in range(9):
    #     row_str = input(f"Input row {r+1} numbers (0 for blank) [030070009] ")
    #     row = [int(num) for num in row_str]
    #     board.append(row)
    # input(f'{board}')
    board = [[6, 0, 0, 0, 0, 0, 0, 1, 5], [0, 0, 0, 5, 0, 6, 0, 7, 4], [8, 7, 5, 0, 0, 3, 9, 2, 6], [1, 8, 3, 7, 5, 2, 6, 4, 9], [0, 9, 6, 8, 3, 4, 0, 5, 1], [0, 5, 0, 9, 6, 1, 0, 8, 3], [0, 0, 8, 3, 0, 0, 5, 6, 2], [3, 2, 0, 6, 0, 5, 0, 9, 8], [5, 6, 0, 0, 0, 0, 0, 3, 7]]

    game(board_load=board)


def main():
    load()

    # game()


main()

# 030000800
# 060740100
# 970358200
# 403076518
# 080090000
# 620103709
# 009024035
# 058901000
# 006007980
