import pygame
import a_star
import unc
import bfs
import dfs

WIDTH = 800
HEIGHT = 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Visualization.")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BORDER_BLACK = (0, 0, 1)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (150, 0, 0)
PURPLE = (255, 0, 255)
YELLOW = (100, 100, 0)
GREY = (225, 225, 225)


class Spot:

    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.color = WHITE
        self.x = row * width
        self.y = col * width
        self.width = width
        self.total_rows = total_rows
        self.neighbours = []

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == YELLOW

    def is_border(self):
        return self.color == BORDER_BLACK

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_barrier(self):
        self.color = BLACK

    def make_open(self):
        self.color = GREEN

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = YELLOW

    def make_path(self):
        self.color = PURPLE

    def make_border(self):
        self.color = BORDER_BLACK

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.total_rows))

    def __lt__(self, other):
        return False


class Board:

    def __init__(self, window, rows, width):
        self.window = window
        self.rows = rows
        self.width = width
        self.grid = self.make_grid()

    def make_grid(self):
        grid = []
        gap = self.width // self.rows

        for i in range(self.rows):
            grid.append([])
            for j in range(self.rows):
                spot = Spot(i, j, gap, self.rows)
                grid[i].append(spot)
                if (i == 0 or j == 0) or (i == self.rows - 1 or j == self.rows - 1):
                    spot.make_border()

        return grid

    def draw_grid(self):
        gap = self.width // self.rows
        for i in range(self.rows):
            pygame.draw.line(self.window, GREY, (i * gap, 0), (i * gap, self.width))
            for j in range(self.rows):
                pygame.draw.line(self.window, GREY, (0, j * gap), (self.width, j * gap))

    def update_neighbours(self):
        forX = [-1, 0, 1, 0]
        forY = [0, -1, 0, 1]

        for row in self.grid:
            for current_spot in row:
                if 0 < current_spot.row < self.rows - 1 and 0 < current_spot.col < self.rows - 1:
                    for neighbour in range(0, 4):
                        curr_neighbour = self.grid[current_spot.row + forX[neighbour]][current_spot.col + forY[neighbour]]

                        if not (curr_neighbour.is_barrier() or curr_neighbour.is_border()):
                            current_spot.neighbours.append(curr_neighbour)

    def draw_board(self):
        self.window.fill(WHITE)

        for row in self.grid:
            for spot in row:
                spot.draw(self.window)

        self.draw_grid()
        pygame.display.update()

    def get_clicked_spot(self, pos):
        x, y = pos

        spot_width = self.width // self.rows

        spot_row = x // spot_width
        spot_col = y // spot_width

        for row in self.grid:
            for spot in row:
                if spot.row == spot_row and spot.col == spot_col:
                    return spot

    def get_start_spot(self):
        for row in self.grid:
            for spot in row:
                if spot.is_start():
                    return spot

    def get_goal_state(self):
        for row in self.grid:
            for spot in row:
                if spot.is_end():
                    return spot

    def is_goal_state(self, current_spot):
        return current_spot.is_end()

    def get_successors(self, current_spot):
        return current_spot.neighbours


board = Board(WIN, 40, WIDTH)

start = True
end = False

while True:
    board.draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            curr_spot = board.get_clicked_spot(pos)

            if start:
                curr_spot.make_start()
                start = False
                end = True
            elif end:
                curr_spot.make_end()
                end = False
            elif not curr_spot.is_start() and not curr_spot.is_end():
                curr_spot.make_barrier()

        elif pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            curr_spot = board.get_clicked_spot(pos)

            if curr_spot.is_start():
                start = True
                curr_spot.reset()
            elif curr_spot.is_end():
                end = True
                curr_spot.reset()
            elif not curr_spot.is_border():
                curr_spot.reset()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not start:
                board.update_neighbours()
                path = a_star.a_star(board)

                for spot in path:
                    spot.make_path()
                    print(f"--({spot.row}, {spot.col})--")

                print(f"Length: {len(path)} steps")
