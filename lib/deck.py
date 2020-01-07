from __future__ import annotations
import random
from typing import Tuple, List

from lib.hand import Hand
from lib.rank import CardRank


class Deck:
    ROW_WRAP_LIMIT = 5

    def __init__(self, omit_cards: Hand = None):
        self.cards = []
        if omit_cards:
            self.omit_cards_set = set(omit_cards.cards)

        for s in CardRank.SUITS.keys():
            for r in CardRank.RANKS.keys():
                if omit_cards and (s, r) in self.omit_cards_set:
                    continue
                self.cards.append((s, r))

    def shuffle(self) -> Deck:
        random.shuffle(self.cards)
        return self

    def deal_cards(self, num_cards: int = 1) -> List[Tuple[str, str]]:
        if num_cards < 1:
            raise Exception("Can't deal less than 1 card")
        cards = []
        for i in range(0, num_cards):
            cards.append(self.cards.pop(0))
        return cards

    def deal_one(self):
        return self.deal_cards(num_cards=1)

    def __str__(self):
        row = 0
        output = ""
        for c in self.cards:
            output += f"{c[0]}{c[1]} \t\t"
            if row == self.ROW_WRAP_LIMIT:
                output += "\n"
                row = 0
            row += 1
        return output
