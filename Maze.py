"""
@author Axel Glöckner

This program generates a random maze Using a deep first search algorithm.
where the shortest way/solution to the maze is found with the A* algorithm.
The A* algorithm is vizulised with pygame.

CELL COLOR CODING:
GREEN : Start and end points.
BLUE : Shortest way / the solution to the maze.
RED : Closed cell (checked).
YELLOW : Open cell (unchecked).

Enter SPACE to start the search.
"""

import random
import pygame
from queue import PriorityQueue

# CONSTANTS
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (28, 134, 238)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CELL_SIZE = 15

# A class that represents a single Cell in the maze.
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = [True, True, True, True] #top, right, bottom, left
        self.start = False
        self.end = False
        self.color = BLACK
        self.neighbors = []

    def makeOpen(self):
        self.color = YELLOW

    def make_path(self):
        self.color = BLUE

    def make_closed(self):
        self.color = RED
    
    def get_pos(self):
        return self.x, self.y

    # Check if neighbours have barriers between them or not and returns the neighbors that have not.
    def update_neighbours(self, maze: list) -> list:
        #LEFT 
        if self.x>0 and not (maze[self.x-1][self.y].walls[1] and maze[self.x][self.y].walls[3]):
            self.neighbors.append(maze[self.x-1][self.y])
        #RIGHT
        if self.x<len(maze) - 1 and not (maze[self.x+1][self.y].walls[3] and maze[self.x][self.y].walls[1]):
            self.neighbors.append(maze[self.x+1][self.y])
        # DOWN
        if self.y>0 and not (maze[self.x][self.y-1].walls[2] and maze[self.x][self.y].walls[0]):
            self.neighbors.append(maze[self.x][self.y-1])
        # UP
        if self.y<len(maze[0]) - 1 and not (maze[self.x][self.y+1].walls[0] and maze[self.x][self.y].walls[2]):
            self.neighbors.append(maze[self.x][self.y+1])

        return self.neighbors
    
    # For drawing a single cell.
    def draw(self, win):
        cellX, cellY = self.x * CELL_SIZE, self.y * CELL_SIZE
        pygame.draw.circle(win, self.color, (cellX + CELL_SIZE//2, cellY + CELL_SIZE //2), CELL_SIZE//4) 

def generateMaze(w: int, h: int) -> list:
    maze = [[Cell(x,y) for y in range(h)] for x in range(w)] # a 2D array filled with cells
    currentCell = maze[random.randint(0, w-1)][random.randint(0, h-1)] # A random starting point
    currentCell.visited = True 
    visitedCells = [currentCell] # a stack with all visited cells
    
    while visitedCells:  # while there are unvisited cells
        currentCell = visitedCells.pop()  # Pop the last cell

        neighbors = getUnvisitedNeighbors(maze, currentCell) #check the neigbor cells
        if neighbors:
            neighbor = random.choice(neighbors)  # A random neighbor
            removeWall(currentCell, neighbor)  # remove the wall between the cells
            
            # The neibor cells is visited and added to the stack. 
            neighbor.visited = True 
            visitedCells.append(currentCell)
            visitedCells.append(neighbor)

    return maze

# Removes walls between two cells.
def removeWall(current: Cell, choice: Cell):
    if current.x == choice.x:
        if current.y>choice.y:
            current.walls[0] = False
            choice.walls[2] = False
        else:
            current.walls[2] = False
            choice.walls[0] = False
    else:
        if current.x > choice.x:
            current.walls[3] = False
            choice.walls[1] = False
        else:
            current.walls[1] = False
            choice.walls[3] = False

# return neigbors that ar not visited yet.
def getUnvisitedNeighbors(maze: list, cell: Cell) -> list:
    neighbors = []
    x, y = cell.x, cell.y
    if x>0:
        neighbors.append(maze[x-1][y])
    if x<len(maze) - 1:
        neighbors.append(maze[x+1][y])
    if y>0:
        neighbors.append(maze[x][y-1])
    if y<len(maze[0]) - 1:
        neighbors.append(maze[x][y+1])

    return [neighbor for neighbor in neighbors if not neighbor.visited]

# Drawing lines.
def drawMaze(WIN, maze: list):
    for x in range(len(maze)):
        for y in range(len(maze[x])):
            cell = maze[x][y]
            cellX, cellY = x * CELL_SIZE, y * CELL_SIZE
            
            #TOP
            if cell.walls[0]:
                pygame.draw.line(WIN, WHITE, (cellX, cellY), (cellX + CELL_SIZE, cellY))
            #RIGHT
            if cell.walls[1]:
                pygame.draw.line(WIN, WHITE, (cellX + CELL_SIZE, cellY), (cellX + CELL_SIZE, cellY + CELL_SIZE))
            #BOTTOM
            if cell.walls[2]:
                pygame.draw.line(WIN, WHITE, (cellX, cellY + CELL_SIZE), (cellX + CELL_SIZE, cellY + CELL_SIZE))
            #LEFT
            if cell.walls[3]:
                pygame.draw.line(WIN, WHITE, (cellX , cellY), (cellX, cellY + CELL_SIZE))

            if cell.start: 
                pygame.draw.circle(WIN, GREEN, (cellX + CELL_SIZE//2, cellY + CELL_SIZE //2), CELL_SIZE//4)
            
            if cell.end:
                pygame.draw.circle(WIN, GREEN, (cellX + CELL_SIZE//2, cellY + CELL_SIZE //2), CELL_SIZE//4) 

# Draw all cells and the maze on top. 
def draw(win, maze : list):
    win.fill(BLACK)
    for row in maze:
        for cell in row:
            cell.draw(win)

    drawMaze(win, maze)
    pygame.display.update()

# A random start and end point.
def makeStartEnd(maze: list):
    run = True
    while run:
        startX, startY = random.randint(0, len(maze) -1), random.randint(0, len(maze) - 1)
        endX, endY = random.randint(0, len(maze) -1), random.randint(0, len(maze) - 1)
        if maze[startX][startY] != maze[endX][endY]:
            maze[startX][startY].start = True
            maze[endX][endY].end = True
            run = False
    
#Returns the heuristic value between two cells.
def h(p1, p2)-> int:
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)

# Reconstruct the path of A*
def path(came_from: list, current_tile: Cell, draw, win):
    while current_tile in came_from:
        current_tile = came_from[current_tile]
        current_tile.make_path()
        draw()

# A-star Algorithm.
def aStar(maze: list, draw, win):
    start, end = Cell, Cell
    for x in range(len(maze)):
        for y in range(len(maze[x])):
            cell = maze[x][y]
            if cell.start:
                start = cell
            if cell.end:
                end = cell

    count = 0  # Keeps track of the queue
    open_set = PriorityQueue()
    # Adding the start node with the original f-score (which is zero)
    open_set.put((0, count, start))
    came_from = {}  # keeps track of which node we came from

    # a table with a uniqe key for every tile.
    g_score = {cell: float("inf") for row in maze for cell in row}
    g_score[start] = 0  # start nodes g score.

    # a table with a uniqe key for every tile.
    f_score = {cell: float("inf") for row in maze for cell in row}
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
            path(came_from, end, draw, win)
            return True

        # all edges are 1, neighbours g_score -> distance to current node
        # (currently known shortest distance) and add 1
        for neighbour in current.neighbors:
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
                    neighbour.makeOpen()
                    neighbour.draw(win)
            draw()

        if current != start:
            current.make_closed()
    return False

def main():
    print("MAZE DIMENSIONS")
    print("===============")
    x = int(input("x: "))
    y = int(input("y: "))

    HEIGHT = x * CELL_SIZE
    WIDTH = y * CELL_SIZE
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))

    maze = generateMaze(x, y)
    makeStartEnd(maze)

    run = True

    while run: 
        draw(WIN, maze)
        drawMaze(WIN, maze)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # SPACE -> start algorithm
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for row in maze:
                        for cell in row:
                            cell.update_neighbours(maze)
                    aStar(maze, lambda: draw(WIN, maze), WIN)
    pygame.quit()


main()