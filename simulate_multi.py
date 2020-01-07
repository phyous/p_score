import math
import os
import time
import json
from pprint import pprint
from typing import List, Tuple, Dict

from multiprocessing import Pool

from lib.hand import Hand
from lib.simple_round import SimpleRound, Outcome

LOG_INTERVAL = 10000


# Multi-proc simulation
def simulate_multi(num_players: int, simulation_target: int, num_sim_per_iteration: int, num_proc: int) \
        -> Dict[str, Dict[str, Dict[str, int]]]:
    # https://stackoverflow.com/questions/2046603/is-it-possible-to-run-function-in-a-subprocess-without-threading-or-writing-a-se
    pool = Pool(processes=num_proc)

    # If our goal is to run `num_simulations` simulations, we need to find out how many processes to fork
    # First, divide by num_players - since each simulation is actually n games from each players perspective
    required_iterations = math.ceil(float(simulation_target / num_players))
    # Each process spawned will run `num_sim_per_iteration`. Divide by this number to determine how many processes
    # must be spawned
    required_iterations = math.ceil(float(required_iterations / num_sim_per_iteration))

    results: List[Dict[str, Dict[str, Dict[str, int]]]] = []

    multiple_results = [pool.apply_async(work_block, args=(num_players, num_sim_per_iteration)) for i in
                        range(required_iterations)]
    [results.append(r.get()) for r in multiple_results]
    print(results)

    merged_results = merge_results(results)

    return merged_results


def merge_results(res: List[Dict[str, Dict[str, Dict[str, int]]]]) -> Dict[str, Dict[str, Dict[str, int]]]:
    ret = res.pop()

    for k1, sub_dict in ret.items():
        for k2, stats in sub_dict.items():
            for s, num in stats.items():
                if k1 not in ret:
                    ret[k1] = {}
                if k2 not in ret[k1]:
                    ret[k1][k2] = {}
                ret[k1][k2][s] += num
    return ret


def simulate_round(num_players: int) -> Tuple[SimpleRound, Dict[int, Outcome]]:
    sr = SimpleRound(num_players=num_players)
    return sr, sr.results()


def work_block(num_player: int, num_sim_per_iteration: int = 1000000):
    cur_iterations = 0
    target_iterations = num_sim_per_iteration * num_player
    work_block_result: Dict[str, Dict[str, Dict[str, int]]] = {}
    time_checkpoint_s = time.time()
    initial_t = time_checkpoint_s

    for i in range(0, math.ceil(float(num_sim_per_iteration / num_player))):
        res = simulate_round(num_player)
        hand_results: List[Tuple[Hand, Outcome]] = [(res[0].player_hands[p_id], res[1][p_id]) for p_id in
                                                    range(0, num_player)]
        for r in hand_results:
            cur_iterations += num_player
            hand_cards = r[0].cards
            outcome = r[1]
            card1 = hand_cards[0]
            card2 = hand_cards[1]
            c1_str: str = f"{card1[0]}{card1[1]}"
            c2_str: str = f"{card2[0]}{card2[1]}"
            if c1_str not in work_block_result:
                work_block_result[c1_str] = {}
            if c2_str not in work_block_result[c1_str]:
                work_block_result[c1_str][c2_str] = {'w': 0, 'l': 0, 't': 0}

            if outcome == Outcome.WIN:
                work_block_result[c1_str][c2_str]['w'] += 1
            elif outcome == Outcome.TIE:
                work_block_result[c1_str][c2_str]['t'] += 1
            else:
                work_block_result[c1_str][c2_str]['l'] += 1

            if cur_iterations % LOG_INTERVAL == 0:
                new_t = time.time()
                delta_t = new_t - time_checkpoint_s
                time_checkpoint_s = new_t
                speed = round(LOG_INTERVAL / delta_t, 2)
                print(f"[{os.getpid()}] "
                      f"{round((float(cur_iterations) / float(target_iterations)) * 100, 2)}% Complete - "
                      f"{cur_iterations}/{target_iterations} - "
                      f"simulations/s: {speed} - "
                      f"time remaining: {round((target_iterations - cur_iterations) / speed / 3600, 2)}h")

    print(
        f"Total simulation time: {round((time.time() - initial_t) / 3600.0, 2)}h "
        f"({round((time.time() - initial_t), 2)}s)")
    return work_block_result


def main():
    ret = simulate_multi(num_players=4, simulation_target=700000000, num_sim_per_iteration=1000000, num_proc=16)
    pprint(ret)
    with open("output.json", 'w', encoding='utf8') as json_file:
        json.dump(ret, json_file, ensure_ascii=False)


if __name__ == "__main__":
    main()
