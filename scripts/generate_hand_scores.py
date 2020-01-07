from decimal import Decimal
from pprint import pprint
from typing import List, Tuple, Dict

from lib.deck import Deck
from lib.hand import Hand
from lib.simple_round import SimpleRound


def score_all_hands() -> Dict[Tuple[str, str], Decimal]:
    scores = {}

    for c1 in Deck().cards:
        for c2 in Deck().cards:
            for c3
            if c1 != c2:

                outcome = simulate_round(num_players, [c1, c2])
                if outcome == SimpleRound.Outcome.WIN:
                    win += 1
                elif outcome == SimpleRound.Outcome.TIE:
                    tie += 1
                else:
                    loss += 1
                cur_iterations += 1
                if cur_iterations % log_interval == 0:
                    print(f"{round((float(cur_iterations)/float(target_iterations))*100, 2)}% Complete - {cur_iterations}/{target_iterations}")


    return scores


def simulate_round(num_players: int, p1_override: List[Tuple[str, str]]) -> SimpleRound.Outcome:
    sr = SimpleRound(num_players=num_players, p1_override=Hand(p1_override))
    return sr.determine_outcome(1)


def main():
    ret = simulate_all_hands(num_players = 4, iterations_per_hand=1)
    pprint(ret)


if __name__ == "__main__":
    main()
