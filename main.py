import pygame
from astar import astar

# Base Colors
WHITE = (255, 255, 255)
GRAY = (230, 230, 230)

# Main Colors
DARK_GRAY = (125, 125, 125)
PATH = (150, 150, 255)
EXAMINED = (220, 220, 220)

# Constants
SCREEN_W = 700
SCREEN_H = 700
MARGIN = 1
SIZE = 23


# POD class representing the grid
class Grid:
    def __init__(self, n):
        self.matrix = []  # Matrix of 0s and 1s
        for r in range(n):
            self.matrix.append([])
            for c in range(n):
                self.matrix[r].append(0)

        self.size = n  # Matrix size
        self.tile_size = (min(SCREEN_H, SCREEN_W) - (n * MARGIN)) // n  # Tile size (for displaying)

        self.start = (0, 0)  # Start location
        self.end = (n - 1, n - 1)  # End location


# REQUIRES: grid is a valid object of the Grid class, path is a list of (r, c) coordinates
# MODIFIES: screen
# EFFECTS: redraws the screen with new grid and path
def update_screen(screen, grid, path, closed):
    screen.fill(GRAY)

    for r in range(grid.size):
        for c in range(grid.size):
            color = WHITE
            if grid.matrix[r][c] == 1:
                color = DARK_GRAY

            for coord in closed:
                count = 0
                if coord == (r, c):
                    count += 1
                    color = EXAMINED
                    continue

            for coord in path:
                if coord == (r, c):
                    color = PATH
                    continue

            rect_x = (MARGIN + grid.tile_size) * c + MARGIN
            rect_y = (MARGIN + grid.tile_size) * r + MARGIN

            pygame.draw.rect(screen, color, [rect_x, rect_y, grid.tile_size, grid.tile_size])


# REQUIRES: grid is a valid object of the Grid class
# MODIFIES: none
# EFFECTS: returns a list of (r, c) coordinates from start to end
def update_path(grid):
    return astar(grid.matrix, grid.start, grid.end)


# REQUIRES: grid is a valid object of the Grid class
# MODIFIES: matrix member variable
# EFFECTS: places/deletes a wall at the mouse
def update_tile(grid):
    pos = pygame.mouse.get_pos()
    column = pos[0] // (grid.tile_size + MARGIN)
    row = pos[1] // (grid.tile_size + MARGIN)
    if 0 <= column < grid.size and 0 <= row < grid.size and (not (row, column) == update_tile.last):
        grid.matrix[row][column] = not grid.matrix[row][column]
        update_tile.last = (row, column)


# Prevents flip/flop
update_tile.last = (-1, -1)


# REQUIRES: grid is a valid object of the Grid class
# MODIFIES: start/end member variable
# EFFECTS: moves the closest start/end to the mouse
def update_start_end(grid):
    pos = pygame.mouse.get_pos()
    column = pos[0] // (grid.tile_size + MARGIN)
    row = pos[1] // (grid.tile_size + MARGIN)

    dist_start = abs(grid.start[0] - row) + abs(grid.start[1] - column)
    dist_end = abs(grid.end[0] - row) + abs(grid.end[1] - column)

    if 0 <= column < grid.size and 0 <= row < grid.size:
        if dist_start < dist_end:
            grid.start = (row, column)
        else:
            grid.end = (row, column)


# Main Method
def main():
    # Initialize pygame
    pygame.init()
    pygame.display.set_caption("A* Pathfinding")
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

    # Initialize a standard grid and path
    grid = Grid(SIZE)
    (path, examined) = update_path(grid)

    # Display loop
    running = True
    left_click = False
    right_click = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left Click
                    left_click = True
                elif event.button == 3:  # Right Click
                    right_click = True
                break
            if event.type == pygame.MOUSEBUTTONUP:
                left_click = False
                right_click = False
                update_tile.last = (-1, -1)

        if left_click:
            update_tile(grid)
            (path, examined) = update_path(grid)
        elif right_click:
            update_start_end(grid)
            (path, examined) = update_path(grid)

        # Draw and update the screen
        update_screen(screen, grid, path, examined)
        pygame.display.flip()

    # Quit pygame
    pygame.quit()


if __name__ == "__main__":
    main()
