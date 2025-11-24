import random

SCREEN_SIZE = 600
GRID_SIZE = 30
MAZE_SIZE = GRID_SIZE
START = (1, 1)
END = (MAZE_SIZE - 2, MAZE_SIZE - 2) 
CELL_SIZE = SCREEN_SIZE // GRID_SIZE
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def create_initial_grid():
    """Creates a grid full of walls (1s)."""
    grid = [[1 for _ in range(MAZE_SIZE)] for _ in range(MAZE_SIZE)]
    return grid

def is_valid(r, c):
    """Checks if coordinates are within the maze boundaries (excluding outer border)."""
    return 0 < r < MAZE_SIZE - 1 and 0 < c < MAZE_SIZE - 1

def generate_perfect_maze(grid):
    """Generates a perfect maze using the Recursive Backtracker."""
    stack = [START]
    grid[START[0]][START[1]] = 0

    while stack:
        current_r, current_c = stack[-1]
        
        unvisited_neighbors = []
        for dr, dc in DIRECTIONS:
            neighbor_r, neighbor_c = current_r + dr * 2, current_c + dc * 2
            if is_valid(neighbor_r, neighbor_c) and grid[neighbor_r][neighbor_c] == 1:
                unvisited_neighbors.append((dr, dc))
        
        if unvisited_neighbors:
            dr, dc = random.choice(unvisited_neighbors)
            next_r, next_c = current_r + dr * 2, current_c + dc * 2
            
            wall_r, wall_c = current_r + dr, current_c + dc
            grid[wall_r][wall_c] = 0
            
            grid[next_r][next_c] = 0
            stack.append((next_r, next_c))
        else:
            stack.pop()
    
    return grid

def create_braid_maze(grid, wall_removal_ratio=0.08):
    """Removes a percentage of walls to create an imperfect (braid) maze with loops."""
    num_cells_to_open = int((MAZE_SIZE * MAZE_SIZE) * wall_removal_ratio)
    
    removable_walls = []
    for r in range(1, MAZE_SIZE - 1):
        for c in range(1, MAZE_SIZE - 1):
            if grid[r][c] == 1:
                removable_walls.append((r, c))

    random.shuffle(removable_walls)
    
    for r, c in removable_walls[:num_cells_to_open]:
        grid[r][c] = 0
        
    return grid

GRID_SIZE = MAZE_SIZE
MAZE = generate_perfect_maze(create_initial_grid())
MAZE = create_braid_maze(MAZE, wall_removal_ratio=0.08)

MAZE[START[0]][START[1]] = 0
MAZE[END[0]][END[1]] = 0

if random.choice([True, False]):
    MAZE[END[0]][END[1] - 1] = 0 # Force connection from left
else:
    MAZE[END[0] - 1][END[1]] = 0 # Force connection from top
