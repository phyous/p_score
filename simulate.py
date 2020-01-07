from pprint import pprint
from typing import List, Tuple, Dict

from lib.deck import Deck
from lib.hand import Hand
from lib.simple_round import SimpleRound
import time


# Single process simulation
def simulate_all_hands(num_players: int = 4, iterations_per_hand: int = 10) -> Dict[str, Dict[str, int]]:
    outcomes = {}
    target_iterations = 52 * 51 * iterations_per_hand
    cur_iterations = 0
    log_interval = 1000
    time_checkpoint_s = time.time()
    initial_t = time_checkpoint_s

    for c1 in Deck().cards:
        for c2 in Deck().cards:
            win = 0
            loss = 0
            tie = 0
            if c1 != c2:
                for it in range(0, iterations_per_hand):
                    outcome = simulate_round_with_override(num_players, [c1, c2])
                    if outcome == SimpleRound.Outcome.WIN:
                        win += 1
                    elif outcome == SimpleRound.Outcome.TIE:
                        tie += 1
                    else:
                        loss += 1
                    cur_iterations += 1
                    if cur_iterations % log_interval == 0:
                        new_t = time.time()
                        delta_t = new_t - time_checkpoint_s
                        time_checkpoint_s = new_t
                        speed = round(log_interval / delta_t, 2)
                        print(f"{round((float(cur_iterations) / float(target_iterations)) * 100, 2)}% Complete - "
                              f"{cur_iterations}/{target_iterations} - "
                              f"simulations/s: {speed} - "
                              f"time remaining: {round((target_iterations - cur_iterations) / speed / 3600, 2)}h")
                c1_str = f"{c1[0]}{c1[1]}"
                c2_str = f"{c2[0]}{c2[1]}"

                if c1_str not in outcomes:
                    outcomes[c1_str] = {}
                outcomes[c1_str][c2_str] = {'w': win, 'l': loss, 't': tie}

    print(
        f"Total simulation time: {round((time.time() - initial_t) / 3600.0, 2)}h "
        f"({round((time.time() - initial_t), 2)}s)")
    return outcomes


def simulate_round_with_override(num_players: int, p1_override: List[Tuple[str, str]] = None) -> SimpleRound.Outcome:
    sr = SimpleRound(num_players=num_players, p1_override=Hand(p1_override))
    return sr.player_result(1)


def main():
    ret = simulate_all_hands(num_players=4, iterations_per_hand=100)
    pprint(ret)


if __name__ == "__main__":
    main()
