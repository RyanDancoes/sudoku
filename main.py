import pygame
import numpy as np
import helpers
import copy

class Board:
    def __init__(self):
        self.board = [[0] * 9 for _ in range(9)]
        self.isEmpty = np.random.choice((True, False), 1)
        self.row, self.col = 0, 0
        self.house_num = build.get_house_number(self.row, self.col)

    def make_board(self):
        for i in range(9):
            for j in range(9):
                if not self.isEmpty:
                    self.board[i][j] = 0  # np.random.randint(1, 10)
                self.isEmpty = np.random.choice((True, False), 1)
        self.board[0][0] = 0
        self.house_num = build.get_house_number(self.row, self.col)

    def write_notes(self):
        options = []
        full = (
            build.get_row(self.board, self.row)
            + build.get_column(self.board, self.col)
            + build.get_house(self.board, self.house_num)
        )
        filled = []
        for i in full:
            if i != 0 and i not in filled:
                filled.append(i)

        for i in range(1, 10):
            if i not in filled:
                options.append(i)
        return options

class Grid:
    def __init__(self, display_surf, width, height):
        self._display_surf = display_surf
        self.width = width
        self.height = height

    def draw(self):
        padding = 20
        cell_size = (self.width - 2 * padding) // 9

        for i in range(padding, self.width - padding + 1, cell_size):
            pygame.draw.line(
                self._display_surf, (0, 0, 255), (i, padding), (i, self.height - padding)
            )
            pygame.draw.line(
                self._display_surf, (0, 0, 255), (padding, i), (self.width - padding, i)
            )

        pygame.display.update()

class Solver:
    def __init__(self, board):
        self.board = board

    def calculate_options(self):
        filled_board = copy.deepcopy(self.board.board)

        for i in range(9):
            for j in range(9):
                options = []
                if not self.board.board[i][j]:
                    options = self.board.write_notes()

                filled_board[i][j] = options

        combined = {(i, j): {self.board.board[i][j]: filled_board[i][j]} for i in range(9) for j in range(9)}
        print(combined)


class App:
    def __init__(self):
        self._running = True
        self.size = self.width, self.height = 697, 697
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.board = Board()
        self.grid = Grid(self._display_surf, self.width, self.height)
        self.solver = Solver(self.board)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        self.grid.draw()
        self.solver.calculate_options()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            input()

        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()


