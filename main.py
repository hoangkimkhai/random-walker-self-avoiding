import pygame

from random import shuffle
import time

import pygame.draw

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Random walker - Self Avoiding")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Spot:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.width = width
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.visited = False
        self.rad = self.width / 4
        self.center_x = self.x + width / 2
        self.center_y = self.y + width / 2
        self.comeFrom = None
        self.directions = [[1, 0, False], [0, 1, False], [-1, 0, False], [0, -1, False]]
        self.final = True
        shuffle(self.directions)

    def get_center(self):
        return self.center_x, self.center_y

    def get_pos(self):
        return self.row, self.col

    def visit(self, come_from):
        self.comeFrom = come_from;
        self.visited = True

    def draw(self, win):
        if self.visited:
            pygame.draw.circle(win, self.color, (self.center_x, self.center_y), self.rad)
            if self.comeFrom is not None:
                self.draw_line(win, self.comeFrom)
        else:
            pygame.draw.rect(win, BLACK, (self.x, self.y, self.width, self.width))

    def draw_line(self, win, fr):
        frx, fry = fr.get_center()
        pygame.draw.line(win, self.color, (frx, fry), (self.center_x, self.center_y), 2)

    def is_visited(self):
        return self.visited

    def make_final(self):
        if self.final:
            self.color = (150, 23, 69)
        else:
            self.make_reverse()

    def make_reverse(self):
        self.color = (64, 224, 208)

    def un_visited(self):
        self.visited = False
        self.comeFrom = None
        self.directions = [[1, 0, False], [0, 1, False], [-1, 0, False], [0, -1, False]]

    def __lt__(self, other):
        return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap)
            grid[i].append(spot)
    return grid


def draw(win, grid, rows):
    win.fill(BLACK)
    for i in range(rows):
        for j in range(rows):
            grid[i][j].draw(win)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def is_complete(grid, rows):
    for i in range(rows):
        for j in range(rows):
            if not grid[i][j].is_visited():
                return False
    return True


def algorithm(draw, path, grid, rows):
    time.sleep(0.1)
    while not is_complete(grid, rows):
        cur = path[len(path) - 1]
        next_spot = get_next_spot(cur, grid, rows)
        if next_spot is None:
            remove = path.pop()
            remove.un_visited()
        else:
            next_spot.visit(cur)
            path.append(next_spot)
    haha = []
    while len(path) > 0:
        cur = path.pop()
        cur.make_final()
        if cur.final:
            cur.final = False
        else:
            cur.final = True
        haha.append(cur)
        time.sleep(0.1)
        draw()
        if len(path) == 0:
            path = haha.copy()
            haha = []


def get_next_spot(current, grid, rows):
    for option in current.directions:
        if not option[2]:
            cur_pos_x, cur_pos_y = current.get_pos()
            if rows > cur_pos_x + option[0] >= 0 and rows > cur_pos_y + option[1] >= 0:
                next_spot = grid[cur_pos_x + option[0]][cur_pos_y + option[1]]
                if not next_spot.visited:
                    option[2] = True
                    return next_spot

    return None


def main(win):
    rows = 6
    grid = make_grid(rows, 800)
    start = grid[2][2]
    start.visited = True
    path = [start]
    draw(win, grid, rows)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        algorithm(lambda: draw(win, grid, rows), path, grid, rows)


main(WIN)
