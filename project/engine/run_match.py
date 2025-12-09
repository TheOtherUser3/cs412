import random
from django.db import transaction
from ..models import Match, MoveEvent, BotBoardStats
from .arena import step_game

# Let us be lazy and just make FakeMoveEvents if we are simulating to save on database hits
class FakeMoveEvent:
    def __init__(
        self,
        match,
        move_number,
        bot1_move,
        bot2_move,
        bot1_body,
        bot2_body,
        bot1_alive,
        bot2_alive,
        apple_positions,
        bot1_ate,
        bot2_ate,
    ):
        self.match = match
        self.move_number = move_number
        self.bot1_move = bot1_move
        self.bot2_move = bot2_move
        self.bot1_body = bot1_body
        self.bot2_body = bot2_body
        self.bot1_alive = bot1_alive
        self.bot2_alive = bot2_alive
        self.apple_positions = apple_positions
        self.bot1_ate = bot1_ate
        self.bot2_ate = bot2_ate

def run_match(bot1, bot2, board, max_turns=5000, simulate=False):
    """
    Run a full snake match between bot1 and bot2 on board.
    Creates Match and MoveEvents.
    """

    # initial positions 
    # if two_box_arenas start must be different
    if board.board_json.get("type", []) == "two_box_arenas":
        b1_start = [(4, 4), (3, 4), (3, 3)]
        b2_start = [
            (board.width - 6, board.height - 6),
            (board.width - 5, board.height - 6),
            (board.width - 5, board.height - 5),
        ]
    else:
        b1_start = [(1, 1), (0, 1), (0, 0)]
        b2_start = [
            (board.width - 2, board.height - 2),
            (board.width - 1, board.height - 2),
            (board.width - 1, board.height - 1),
        ]

    # Initial apples 
    obstacles = set(map(tuple, board.board_json.get("obstacles", [])))
    apples = []
    while len(apples) < board.food_count:
        p = (
            random.randrange(board.width),
            random.randrange(board.height),
        )
        if (
            p not in b1_start
            and p not in b2_start
            and p not in obstacles
            and p not in apples
        ):
            apples.append(p)

    # Accumulator Variables
    apples_a = 0
    apples_b = 0
    a_survival_time = 0
    b_survival_time = 0
    winner = None

    # different behaviour for simulations vs non simulations to save time + space
    if not simulate:
        # Avoid dirty writes! Made sure to find out how to do this online so it rolls back if anything fails.  
        with transaction.atomic():
            # create Match 
            match = Match.objects.create(
                bot1=bot1,
                bot2=bot2,
                board=board,
            )

            # move 0 
            prev = MoveEvent.objects.create(
                match=match,
                move_number=0,
                bot1_move="RIGHT",
                bot2_move="LEFT",
                bot1_body=b1_start,
                bot2_body=b2_start,
                bot1_alive=True,
                bot2_alive=True,
                apple_positions=apples,
                bot1_ate=False,
                bot2_ate=False,
            )

            # simulation loop 
            for _ in range(max_turns):
                if not (prev.bot1_alive or prev.bot2_alive):
                    break

                data = step_game(prev, bot1, bot2, board)

                # Update accumulators
                if data["bot1_ate"]:
                    apples_a += 1
                if data["bot2_ate"]:
                    apples_b += 1

                if data["bot1_alive"]:
                    a_survival_time = data["move_number"]
                if data["bot2_alive"]:
                    b_survival_time = data["move_number"]

                prev = MoveEvent.objects.create(**data)

            # finalize match
            if apples_a > apples_b:
                winner = 1
            elif apples_b > apples_a:
                winner = 2
            else:
                winner = 0

            match.a_survival_time = a_survival_time
            match.b_survival_time = b_survival_time
            match.apples_a = apples_a
            match.apples_b = apples_b
            match.winner = winner
            match.total_turns = prev.move_number
            match.save()

            # Update stats for each bot on this board
            update_bot_board_stats(bot1, board, 1 if winner == 1 else (2 if winner == 2 else 0), a_survival_time, apples_a)
            update_bot_board_stats(bot2, board, 2 if winner == 1 else (1 if winner == 2 else 0), b_survival_time, apples_b)


            return match

    else:
        # simulate-only

        match = None

        # move 0 
        prev = FakeMoveEvent(
            match=match,
            move_number=0,
            bot1_move="RIGHT",
            bot2_move="LEFT",
            bot1_body=b1_start,
            bot2_body=b2_start,
            bot1_alive=True,
            bot2_alive=True,
            apple_positions=apples,
            bot1_ate=False,
            bot2_ate=False,
        )

        # simulation loop 
        for _ in range(max_turns):
            if not (prev.bot1_alive or prev.bot2_alive):
                break

            data = step_game(prev, bot1, bot2, board)

            # Update accumulators
            if data["bot1_ate"]:
                apples_a += 1
            if data["bot2_ate"]:
                apples_b += 1

            if data["bot1_alive"]:
                a_survival_time = data["move_number"]
            if data["bot2_alive"]:
                b_survival_time = data["move_number"]

            prev = FakeMoveEvent(**data)

        # finalize winner 
        if apples_a > apples_b:
            winner = 1
        elif apples_b > apples_a:
            winner = 2
        else:
            winner = 0

        return {
            "winner": winner,
            "apples_a": apples_a,
            "apples_b": apples_b,
            "a_survival_time": a_survival_time,
            "b_survival_time": b_survival_time,
        }



def simulate_matches(bot1, bot2, board, num_runs):
    """Simulate num_sims number of matches between bot1 and bot2 on board, for plotly. 
    Return all relevent results in nice JSON format."""
    results = {
        "bot1": {
            "name": bot1.name,
            "color": bot1.color,
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "avg_turns": 0,
            "avg_apples": 0,
        },
        "bot2": {
            "name": bot2.name,
            "color": bot2.color,
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "avg_turns": 0,
            "avg_apples": 0,
        }
        }
    
    for i in range(1, num_runs + 1):
        match = run_match(bot1, bot2, board, simulate=True)
        if match['winner'] == 1:
            results["bot1"]["wins"] += 1
            results["bot2"]["losses"] += 1
        elif match['winner'] == 2:
            results["bot2"]["wins"] += 1
            results["bot1"]["losses"] += 1
        else:
            results["bot1"]["draws"] += 1
            results["bot2"]["draws"] += 1

        results['bot1']['avg_apples'] = (results['bot1']['avg_apples']*(i-1))/i + match["apples_a"]/i
        results['bot2']['avg_apples'] = (results['bot2']['avg_apples']*(i-1))/i + match["apples_b"]/i 

        results['bot1']['avg_turns'] = (results['bot1']['avg_turns']*(i-1))/i + match["a_survival_time"]/i
        results['bot2']['avg_turns'] = (results['bot2']['avg_turns']*(i-1))/i + match["b_survival_time"]/i 

    
    return results

def update_bot_board_stats(bot, board, outcome, turns, apples):
    """Helper function to update bot stats in the new BotBoardStats model"""

    # get_or_create method lets us easily prevent duplicates
    stats, _ = BotBoardStats.objects.get_or_create(
        bot=bot,
        board=board
    )

    stats.games += 1

    if outcome == 1:
        stats.wins += 1
    elif outcome == 2:
        stats.losses += 1
    else:
        stats.draws += 1

    # running averages
    stats.avg_turns = (stats.avg_turns*(stats.games-1))/stats.games + turns / stats.games
    stats.avg_apples = (stats.avg_apples*(stats.games-1))/stats.games + apples / stats.games

    stats.save()
