# File: board_generator.py
# Author: Dawson Maska (dawsonwm@bu.edu), 11/25/2025
# Description: Generates different types of snake boards based on user input from the BoardGeneratorForm.

import random

def rect_walls(width, height):
    """Return a list of (x, y) for outer walls."""
    walls = []
    for x in range(width):
        walls.append((x, 0))
        walls.append((x, height - 1))
    for y in range(height):
        walls.append((0, y))
        walls.append((width - 1, y))
    return walls


# -----------------------------------------------------------
# 1. OPEN FIELD (no obstacles, no wraparound)
# -----------------------------------------------------------
def gen_open(width, height, wraparound):
    return {
        "type": "open",
        "obstacles": [],
        "wrap": wraparound
    }


# -----------------------------------------------------------
# 2. OUTER WALLS (classic snake)
# -----------------------------------------------------------
def gen_outer_wall(width, height, wraparound):
    return {
        "type": "outer_wall",
        "obstacles": rect_walls(width, height),
        "wrap": wraparound
    }


# -----------------------------------------------------------
# 4. INNER MAZE (why do I do this to myself)
# -----------------------------------------------------------

# edit of the design found at https://inventwithpython.com/recursion/chapter11.html, to give credit

WALL = 1
EMPTY = 0

def generate_maze(log_w, log_h):
    """
    Generate a maze on a logical grid of size log_w x log_h.
    log_w and log_h should be odd and >= 3.
    Returns a dict {(x, y): WALL/EMPTY}.
    """

    maze = {}
    for x in range(log_w):
        for y in range(log_h):
            maze[(x, y)] = WALL

    def neighbors_two_steps(x, y):
        res = []
        if y > 1:
            res.append((x, y - 2))
        if y < log_h - 2:
            res.append((x, y + 2))
        if x > 1:
            res.append((x - 2, y))
        if x < log_w - 2:
            res.append((x + 2, y))
        return res

    visited = set()
    stack = [(1, 1)]
    visited.add((1, 1))
    maze[(1, 1)] = EMPTY

    while stack:
        x, y = stack[-1]

        unvisited = [
            (nx, ny) for (nx, ny) in neighbors_two_steps(x, y)
            if (nx, ny) not in visited
        ]

        if not unvisited:
            stack.pop()
            continue

        nx, ny = random.choice(unvisited)
        visited.add((nx, ny))

        # Carve passage between (x, y) and (nx, ny)
        mx = (x + nx) // 2
        my = (y + ny) // 2
        maze[(mx, my)] = EMPTY
        maze[(nx, ny)] = EMPTY

        stack.append((nx, ny))

    return maze

def add_multiple_exits(maze, log_w, log_h, exit_count=3):
    """
    Convert some border walls into empty cells if they border an empty interior cell,
    to create multiple exits.
    """

    candidates = []

    for x in range(log_w):
        for y in range(log_h):
            if x in (0, log_w - 1) or y in (0, log_h - 1):
                if maze[(x, y)] == WALL:
                    # Check for adjacent empty interior cell
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < log_w and 0 <= ny < log_h:
                            if maze[(nx, ny)] == EMPTY:
                                candidates.append((x, y))
                                break

    random.shuffle(candidates)
    for (x, y) in candidates[:exit_count]:
        maze[(x, y)] = EMPTY

    return maze


def gen_inner_maze(width, height, wraparound):
    """
    Maze with:
      - 3-cell empty border all around
      - corridors 2 cells wide
      - multiple exits into the outer ring
    """
    BORDER = 3
    CELL_SCALE = 2

    inner_w = width  - 2 * BORDER
    inner_h = height - 2 * BORDER

    if inner_w <= 0 or inner_h <= 0:
        # Board too small, just no obstacles
        return {
            "type": "inner_maze",
            "obstacles": [],
            "wrap": wraparound,
        }

    # Logical grid size
    log_w = inner_w // CELL_SCALE
    log_h = inner_h // CELL_SCALE

    if log_w < 3 or log_h < 3:
        # Still too small for a real maze
        return {
            "type": "inner_maze",
            "obstacles": [],
            "wrap": wraparound,
        }

    maze = generate_maze(log_w, log_h)
    maze = add_multiple_exits(maze, log_w, log_h, exit_count=3)

    obstacles = []

    for x in range(log_w):
        for y in range(log_h):
            if maze[(x, y)] == WALL:
                base_x = BORDER + x * CELL_SCALE
                base_y = BORDER + y * CELL_SCALE

                for dx in range(CELL_SCALE):
                    for dy in range(CELL_SCALE):
                        gx = base_x + dx
                        gy = base_y + dy

                        # Make sure we never invade the 3-cell border
                        if (
                            BORDER <= gx < width  - BORDER
                            and BORDER <= gy < height - BORDER
                        ):
                            obstacles.append((gx, gy))

    return {
        "type": "inner_maze",
        "obstacles": obstacles,
        "wrap": wraparound,
    }



    

# -----------------------------------------------------------
# 5. SCATTERED BLOCKS (random obstacles)
# -----------------------------------------------------------
def gen_scattered_blocks(width, height, wraparound, density=0.05):
    obstacles = []
    total_cells = width * height
    block_count = int(total_cells * density * random.uniform(0.8, 1.5))

    for _ in range(block_count):
        x = random.randrange(width)
        y = random.randrange(height)
        obstacles.append((x, y))

    return {
        "type": "scattered_blocks",
        "obstacles": obstacles,
        "wrap": wraparound
    }


# -----------------------------------------------------------
# 6. CORRIDORS (tunnels)
# -----------------------------------------------------------
def gen_corridors(width, height, wraparound):
    obstacles = []

    # Every 4 rows, add a horizontal wall segment with some holes
    for y in range(3, height - 3, 4):
        for x in range(1, width - 1):
            if x % 5 != 0:  # holes every 5 cells
                obstacles.append((x, y))

    return {
        "type": "corridors",
        "obstacles": obstacles,
        "wrap": wraparound
    }


# -----------------------------------------------------------
# 7. TWO BOX ARENAS (two symmetric chambers)
# -----------------------------------------------------------
def gen_two_box_arenas(width, height, wraparound):
    obstacles = []

    mid = width // 2

    # Left box
    for x in range(2, mid - 2):
        obstacles.append((x, 2))
        obstacles.append((x, height - 3))
    for y in range(2, height - 2):
        obstacles.append((2, y))
        obstacles.append((mid - 3, y))

    # Right box
    for x in range(mid + 2, width - 2):
        obstacles.append((x, 2))
        obstacles.append((x, height - 3))
    for y in range(2, height - 2):
        obstacles.append((mid + 2, y))
        obstacles.append((width - 3, y))

    return {
        "type": "two_box_arenas",
        "obstacles": obstacles,
        "wrap": wraparound
    }


# -----------------------------------------------------------
# Generator dispatcher
# -----------------------------------------------------------
def generate_board(board_type, width, height, wraparound):
    generators = {
        "open": gen_open,
        "outer_wall": gen_outer_wall,
        "inner_maze": gen_inner_maze,
        "scattered_blocks": gen_scattered_blocks,
        "corridors": gen_corridors,
        "two_box_arenas": gen_two_box_arenas,
    }

    data = generators[board_type](width, height, wraparound)

    return data
