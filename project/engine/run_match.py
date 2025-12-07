import random
from django.db import transaction
from ..models import Match, MoveEvent
from arena import step_game


def run_match(bot1, bot2, board, max_turns=5000):
    """
    Run a full snake match between bot1 and bot2 on board.
    Creates Match and MoveEvents.
    """

    # Avoid dirty writes!  Rolls back if anything fails.  
    with transaction.atomic():
        # create Match 
        match = Match.objects.create(
            bot1=bot1,
            bot2=bot2,
            board=board,
        )

        # initial positions 
        b1_start = [(1, 1), (0, 1), (0, 0)]
        b2_start = [
            (board.width - 2, board.height - 2),
            (board.width - 1, board.height - 2),
            (board.width - 1, board.height - 1),
        ]

        # Initial apples 
        obstacles = set(map(tuple, board.board_json.get("obstacles", [])))
        apples = []
        while len(apples) < board.num_apples:
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

        # move 0 
        prev = MoveEvent.objects.create(
            match=match,
            move_number=0,
            bot1_dir="RIGHT",
            bot2_dir="LEFT",
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
            prev = MoveEvent.objects.create(**data)

        # finalize match
        match.total_turns = prev.move_number
        match.apples_a = sum(
            [ev.bot1_ate for ev in match.move_events.all()]
        )
        match.apples_b = sum(
            [ev.bot2_ate for ev in match.move_events.all()]
        )

        match.a_survival_time = (
            prev.move_number if prev.bot1_alive else
            max([ev.move_number for ev in match.move_events.filter(bot1_alive=True)])
        )
        match.b_survival_time = (
            prev.move_number if prev.bot2_alive else
            max([ev.move_number for ev in match.move_events.filter(bot2_alive=True)])
        )

        if match.a_survival_time > match.b_survival_time:
            match.winner = 1
        elif match.a_survival_time < match.b_survival_time:
            match.winner = 2
        else:
            match.winner = 0  # tie

        match.save()

        return match
