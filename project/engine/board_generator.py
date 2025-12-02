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
# 4. INNER MAZE (fixed pattern)
# -----------------------------------------------------------
def gen_inner_maze(width, height, wraparound):
    obstacles = []

    # Super simple maze.  Vertical pillars every few columns
    for x in range(3, width - 3, 6):
        for y in range(2, height - 2):
            if y % 4 != 0:
                obstacles.append((x, y))

    return {
        "type": "inner_maze",
        "obstacles": obstacles,
        "wrap": wraparound
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
