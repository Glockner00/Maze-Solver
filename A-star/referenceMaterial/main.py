import pygame
from queue import PriorityQueue

# Constants
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (28, 134, 238)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
GREY = (128, 128, 128)


class Tile:
    # Constructor
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbours = []

    def get_pos(self):
        return self.row, self.col

    # Functions that describes a tiles different states.
    def is_closed(self):
        return self.color == RED

    def is_opened(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == YELLOW

    def is_end(self):
        return self.color == BLUE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = YELLOW

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = BLUE

    def make_path(self):
        self.color = PURPLE

    # Draw a single tile
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y,
                                           self.width, self.width))

    # Check if neighbours are barriers or not.
    def update_neighbours(self, grid):
        self.neighbours = []
        # Down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row + 1][self.col])
        # Up
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row - 1][self.col])
        # Left
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col - 1])
        # Right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col + 1])

    # "less than", compares lt tile and other tile.
    # The other tile is always going to be greater than lt:s tile
    def __lt__(self, other):
        return False


# Main algorithm.
def a_star(draw, grid, start, end):
    count = 0  # Keeps track of the queue
    open_set = PriorityQueue()
    # Adding the start node with the original f-score (which is zero)
    open_set.put((0, count, start))
    came_from = {}  # keeps track of which node we came from

    # a table with a uniqe key for every tile.
    g_score = {tile: float("inf") for row in grid for tile in row}
    g_score[start] = 0  # start nodes g score.

    # a table with a uniqe key for every tile.
    f_score = {tile: float("inf") for row in grid for tile in row}
    # Heuristic, makes an estimate how far the end node is from the start node.
    f_score[start] = h(start.get_pos(), end.get_pos())  # start nodes f score.

    # keeps track of all the items in/not in the PriorityQueue
    open_set_hash = {start}  # set

    # if the set i empty we have checked all the possible node.
    while not open_set.empty():
        for event in pygame.event.get():
            #  A way of exiting the algorithm.
            if event.type == pygame.QUIT:
                pygame.quit()

        # if we get the same f score we will instead look at the count
        # (PriorityQueue).
        current = open_set.get()[2]  # the node.

        # take the node that poped of the PriorityQueue and sync the hash.
        # ensures that there are no duplicates.
        open_set_hash.remove(current)

        if current == end:  # path found.
            path(came_from, end, draw)
            return True

        # all edges are 1, neighbours g_score -> distance to current node
        # (currently known shortest distance) and add 1
        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            # Found a shorter way
            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(),
                                                      end.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

        draw()

        if current != start:
            current.make_closed()
    return False


# Heuristic function for the main algorithm.
# Returns the distance between point 1 and point 2 using manhattan distance
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)


# Reconstruct the path.
def path(came_from, current_tile, draw):
    while current_tile in came_from:
        current_tile = came_from[current_tile]
        current_tile.make_path()
        draw()


# Make an empty grid. without grid lines.
# returns a 2D array with tile objects.
def make_grid(rows, width):
    grid = []
    gap = width // rows  # gap between each row/width of each cube.
    for i in range(rows):
        grid.append([])  # 2D - array
        for j in range(rows):
            tile = Tile(i, j, gap, rows)
            grid[i].append(tile)
    return grid


# Drawing grey gridlines for the gird.
def draw_grid(win, rows, width):
    gap = width // rows  # width of each cube.
    for i in range(rows):

        # Vertical lines
        pygame.draw.line(win, GREY, (0, i*gap), (width, i * gap))
        for j in range(rows):

            # Horizontal lines
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


# Main draw function that draws the grid with help of the Tile class.
def draw(win, grid, rows, width):
    win.fill(WHITE)  # Fill entire window with WHITE
    for row in grid:
        for tile in row:
            tile.draw(win)

    # Draw gridlines on top.
    draw_grid(win, rows, width)
    pygame.display.update()


# Returns the coordinates that are clicked.
def mouse_clicked_position(pos, row, width):
    gap = width // row  # width of each cube
    y, x = pos
    row = y // gap
    col = x // gap

    return row, col


# Main method.
def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # LEFT CLICK - enter start, end and barriers
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = mouse_clicked_position(pos, ROWS, width)
                tile = grid[row][col]

                # First click
                if not start and tile != end:
                    start = tile
                    start.make_start()

                # Second click
                if not end and tile != start:
                    end = tile
                    end.make_end()

                # Third click
                if tile != end and tile != start:
                    tile.make_barrier()

            # RIGHT CLICK - reset Tile
            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = mouse_clicked_position(pos, ROWS, width)
                tile = grid[row][col]
                tile.reset()

                # reset start and end
                if tile == start:
                    start = None
                elif tile == end:
                    end = None

            # Key down, start algorithm
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for tile in row:
                            tile.update_neighbours(grid)
                    # Lambda calls an anonymous function
                    # Allows for calling this specifik draw in a_star.
                    a_star(lambda: draw(win, grid, ROWS, width),
                           grid, start, end)
    pygame.QUIT


main(WIN, WIDTH)
