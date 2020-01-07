from enum import Enum
from typing import Optional, Dict

from lib.deck import Deck
from lib.hand import Hand

# Simulates a simple hold'em round with no betting. Assumes all players are in the round until the end.
from lib.round_score import RoundScore


class Outcome(Enum):
    LOSS = -1
    TIE = 0
    WIN = 1


class SimpleRound:
    community_cards: Hand
    player_hands: Dict[int, Optional[Hand]]
    deck: Deck

    def __init__(self, num_players: int = 4, p1_override: Hand = None):
        if num_players < 1:
            raise Exception("Can't play a round with less than 1 player")

        self.deck = Deck(omit_cards=p1_override).shuffle()
        self.player_hands = {}
        for i in range(0, num_players):
            if p1_override and i == 0:
                self.player_hands[i] = p1_override
                continue
            self.player_hands[i] = Hand(self.deck.deal_cards(2))
        self.community_cards = Hand(self.deck.deal_cards(5))

    def results(self) -> Dict[int, Outcome]:
        round_score = RoundScore(self.player_hands, self.community_cards)
        result = {}
        winning_result = max([v for k, v in round_score.scores.items()])
        tie = len(list(filter(lambda v: v == winning_result, round_score.scores.values()))) > 1
        for k, score in round_score.scores.items():
            if score == winning_result:
                if tie:
                    result[k] = Outcome.TIE
                else:
                    result[k] = Outcome.WIN
            else:
                result[k] = Outcome.LOSS
        return result

    def player_result(self, player_id: int) -> Outcome:
        return self.results()[player_id]
