# File: arena.py
# Author: Dawson Maska (dawsonwm@bu.edu), 12/2/2025
# Description: Runs the snake arena matches between specified bots on specified boards. (Runs a single move, let view handle the game loop)

import random
from collections import deque

DIR_DELTAS = {
    "UP":    (0, -1),
    "RIGHT": (1, 0),
    "DOWN":  (0, 1),
    "LEFT":  (-1, 0),
}

RELATIVE_MOVES = ["LEFT", "STRAIGHT", "RIGHT"]

RELATIVE_DELTAS = {
    "STRAIGHT": 0,
    "LEFT": -1,
    "RIGHT": 1
}

DIRECTIONS = ["UP", "RIGHT", "DOWN", "LEFT"]



def first_step_toward_target(head, targets, board, my_body, other_body, obstacles, wrap):
    """
    Use BFS to find the first absolute direction 
    along a shortest path from head to any apple.
    Returns a direction string, or None if no path exists.
    """

    if not targets:
        return None

    width, height = board.width, board.height

    # Cells we are not allowed to go into
    blocked = set(obstacles)
    # Avoid crashing into own body except for current head
    blocked.update(my_body[1:])
    # Avoid other snake completely
    blocked.update(other_body)

    targets = set(targets)

    # BFS queue: (position, first_dir_taken) apparently deque is best to use for this for efficiency
    q = deque()
    visited = set()

    # Start at head, no direction chosen yet
    q.append((tuple(head), None))
    visited.add(tuple(head))

    while q:
        (x, y), first_dir = q.popleft()

        # If we reached an apple, return the first step that led us here
        if (x, y) in targets and first_dir is not None:
            return first_dir

        # Explore neighbors
        for dir_name, (dx, dy) in DIR_DELTAS.items():
            nx = x + dx
            ny = y + dy

            if wrap:
                nx %= width
                ny %= height
            else:
                if not (0 <= nx < width and 0 <= ny < height):
                    continue

            nxt = (nx, ny)

            if nxt in blocked or nxt in visited:
                continue

            visited.add(nxt)

            # If we have not chosen a first step yet, this neighbor is
            # reached by taking dir_name as the first step.
            if first_dir is None:
                q.append((nxt, dir_name))
            else:
                q.append((nxt, first_dir))

    # No path found
    return None


def rotate_direction(current, relative):
    """Rotate a direction by a relative move"""
    delta = RELATIVE_DELTAS[relative]
    idx = DIRECTIONS.index(current)

    return DIRECTIONS[(idx + delta) % len(DIRECTIONS)]

def manhattan(a, b):
    """Return the Manhattan distance between points a and b"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def min_self_distance(head, body):
    """Return the minimum distance from head to any other part of body"""
    min_distance = float("inf")

    for x, y in body[1:]:
        distance = abs(head[0] - x) + abs(head[1] - y)
        if distance < min_distance:
            min_distance = distance

    return min_distance

def adjacent_self_count(head, body):
    """Return the count of body segments adjacent to head"""
    count = 0

    for x, y in body[1:]:
        distance = abs(head[0] - x) + abs(head[1] - y)
        if distance == 1:
            count += 1

    return count


def choose_bot_move(bot, my_body, other_body, apples, board, current_dir):
    """
    Decide LEFT / STRAIGHT / RIGHT based on bot personality.
    Personality attributes are explained in models.py
    """

    head = my_body[0]
    obstacles = set(map(tuple, board.board_json.get("obstacles", [])))
    wrap = board.board_json.get("wrap", False)

    # where should we go to reach an apple?
    path_dir = None
    if apples:
        path_dir = first_step_toward_target(
            head=head,
            targets=apples,
            board=board,
            my_body=my_body,
            other_body=other_body,
            obstacles=obstacles,
            wrap=wrap,
        )

    best_score = -float("inf")
    best_moves = []

    for rel in RELATIVE_MOVES:
        score = 0.0

        # simulate next head position
        new_dir = rotate_direction(current_dir, rel)
        dx, dy = DIR_DELTAS[new_dir]
        nx = head[0] + dx
        ny = head[1] + dy

        if wrap:
            nx %= board.width
            ny %= board.height
        elif not (0 <= nx < board.width and 0 <= ny < board.height):
            score -= 1000
            continue

        new_head = (nx, ny)

        # collision checks
        if (
            new_head in obstacles
            or new_head in my_body
            or new_head in other_body
        ):
            score -= 1000
            continue

        # Strong bonus for following the BFS path toward food if it exists
        if path_dir is not None and new_dir == path_dir:
            # Factor in greediness
            score += bot.greediness * 3.0

        # # greediness (local distance change toward nearest apple)
        # if apples:
        #     nearest = min([(manhattan(head, a), a) for a in apples])[1]
        #     before = manhattan(head, nearest)
        #     after = manhattan(new_head, nearest)
        #     score += (bot.greediness * (before - after))

        # caution (local free space)
        free_neighbors = 0
        for ddx, ddy in DIR_DELTAS.values():
            tx = new_head[0] + ddx
            ty = new_head[1] + ddy

            if wrap:
                tx %= board.width
                ty %= board.height

            if (
                0 <= tx < board.width
                and 0 <= ty < board.height
                and (tx, ty) not in obstacles
                and (tx, ty) not in my_body
                and (tx, ty) not in other_body
            ):
                free_neighbors += 1

        score += bot.caution * free_neighbors

        # introversion (avoid other snake)
        if other_body:
            dist_before = manhattan(head, other_body[0])
            dist_after = manhattan(new_head, other_body[0])
            score += bot.introversion * (dist_after - dist_before)

        # circliness (compactness / self adjacency)
        if len(my_body) > 3:
            min_dist = min_self_distance(new_head, my_body)
            adj_count = adjacent_self_count(new_head, my_body)

            score += bot.circliness * (2 - min(min_dist, 2))
            score += bot.circliness * 0.5 * adj_count

        # direction bias
        if rel == "LEFT":
            score -= bot.direction_bias
        elif rel == "RIGHT":
            score += bot.direction_bias

        # chaos
        score += random.uniform(-bot.chaos, bot.chaos)

        # pick best
        if score > best_score:
            best_score = score
            best_moves = [rel]
        elif score == best_score:
            best_moves.append(rel)

    if not best_moves:
        return random.choice(RELATIVE_MOVES)

    return random.choice(best_moves)



def step_game(prev, bot1, bot2, board):
    """
    prev: MoveEvent instance (previous turn)
    bot1, bot2: Bot model instances
    board: Board model instance

    Returns: dict suitable for MoveEvent.objects.create
    """

    # unpack previous state 
    b1_body = list(prev.bot1_body)
    b2_body = list(prev.bot2_body)

    b1_move = prev.bot1_move
    b2_move = prev.bot2_move

    b1_alive = prev.bot1_alive
    b2_alive = prev.bot2_alive

    apples = list(prev.apple_positions)

    turn = prev.move_number + 1

    # move heads 
    def next_head(body, direction):
        dx, dy = DIR_DELTAS[direction]
        x, y = body[0]
        return (x + dx, y + dy)
    
    # boundary / wrap handling (should be handled by bot move choice, but just in case)
    def normalize(pos):
        x, y = pos
        if board.board_json.get("wrap"):
            return (x % board.width, y % board.height)
        return (x, y)

    # bot decisions
    if b1_alive:
        rel1 = choose_bot_move(bot1, b1_body, b2_body, apples, board, b1_move)
        new_dir1 = rotate_direction(b1_move, rel1)
        h1 = next_head(b1_body, new_dir1)
        h1 = normalize(h1)
    else:
        new_dir1 = "NONE"
    
    if b2_alive:
        rel2 = choose_bot_move(bot2, b2_body, b1_body, apples, board, b2_move)
        new_dir2 = rotate_direction(b2_move, rel2)
        h2 = next_head(b2_body, new_dir2)
        h2 = normalize(h2)
    else:
        new_dir2 = "NONE"

    # turn board obstacles into list of tuples for checking
    obstacles = set(map(tuple, board.board_json.get("obstacles", [])))

    def dies(head, body, other_body):
        if not board.board_json.get("wrap"):
            if not (0 <= head[0] < board.width and 0 <= head[1] < board.height):
                return True
        if head in obstacles:
            return True
        if head in body:
            return True
        if head in other_body:
            return True
        return False

    if b1_alive and dies(h1, b1_body[:-1], b2_body):
        b1_alive = False
    if b2_alive and dies(h2, b2_body[:-1], b1_body):
        b2_alive = False

    # apple handling
    b1_ate = False
    b2_ate = False

    if b1_alive and h1 in apples:
        apples.remove(h1)
        b1_ate = True
    if b2_alive and h2 in apples:
        apples.remove(h2)
        b2_ate = True

    # update bodies 
    if b1_alive:
        b1_body.insert(0, h1)
        if not b1_ate:
            b1_body.pop()

    if b2_alive:
        b2_body.insert(0, h2)
        if not b2_ate:
            b2_body.pop()

    # respawn apples
    apple_cells = get_apple_cells(board, obstacles)

    while len(apples) < board.food_count:
        for _ in range(100):
            p = random.choice(apple_cells)
            if (
                p not in apples
                and p not in b1_body
                and p not in b2_body
            ):
                apples.append(p)
                break

    # return next MoveEvent data 
    return {
        "match": prev.match,
        "move_number": turn,
        "bot1_move": new_dir1,
        "bot2_move": new_dir2,
        "bot1_body": b1_body,
        "bot2_body": b2_body,
        "bot1_alive": b1_alive,
        "bot2_alive": b2_alive,
        "apple_positions": apples,
        "bot1_ate": b1_ate,
        "bot2_ate": b2_ate,
    }
    

    
# Helper function so apples only spawn in the boxes in the two_box_arenas map
def get_apple_cells(board, obstacles):
    """Return list of valid apple spawn cells for this board."""
    board_type = board.board_json.get("type")

    # Special handling for two-box arenas
    if board_type == "two_box_arenas":
        w, h = board.width, board.height
        mid = w // 2
        cells = []

        # Left box 
        for x in range(3, mid - 3):
            for y in range(3, h - 3):
                if (x, y) not in obstacles:
                    cells.append((x, y))

        # Right box 
        for x in range(mid + 3, w - 3):
            for y in range(3, h - 3):
                if (x, y) not in obstacles:
                    cells.append((x, y))

        return cells

    # Default - anywhere that isn't an obstacle
    cells = []
    for x in range(board.width):
        for y in range(board.height):
            if (x, y) not in obstacles:
                cells.append((x, y))
    return cells
