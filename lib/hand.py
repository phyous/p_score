from __future__ import annotations

import math
from typing import List, Tuple, Union, Dict
from decimal import *
from lib.rank import HandRank, CardRank

import functools


class Hand:
    cards: List[Tuple[str, str]]

    def __init__(self, cards: Union[Hand, List[str], List[Tuple[str, str]]] = None):
        if cards is None:
            self.cards = []
        elif isinstance(cards, Hand):
            self.cards = Hand.cards
        elif isinstance(cards[0], Tuple):
            self.cards = cards
        else:
            self.cards = list(map(lambda card: Hand.parse_card(card), cards))

        self.sort()
        self.rank_dict = self.compute_rank_dict()
        self.suit_dict = self.compute_suit_dict()
        self.ascending_by_one = self.compute_ascending_by_one()

    def compute_rank_dict(self) -> Dict[str, List[Tuple[str, str]]]:
        rank_dict = {}
        for c in self.cards:
            rank = c[1]
            if rank not in rank_dict:
                rank_dict[rank] = [c]
            else:
                rank_dict[rank].insert(0, c)
        return rank_dict

    def compute_suit_dict(self) -> Dict[str, List[Tuple[str, str]]]:
        suit_dict = {}
        for c in self.cards:
            suit = c[0]
            if suit not in suit_dict:
                suit_dict[suit] = [c]
            else:
                suit_dict[suit].insert(0, c)
        return suit_dict

    def compute_ascending_by_one(self) -> bool:
        num_cards = len(self.cards)
        if num_cards == 0:
            return False

        differences = [(CardRank.RANKS[self.cards[i][1]] - CardRank.RANKS[self.cards[i - 1][1]] == 1) for i in range(1, num_cards)]
        if not functools.reduce(lambda a, b: a and b, differences):
            return False
        else:
            return True

    RANK_STR = {'H': '♡', 'D': '♢', 'C': '♣', 'S': '♠'}

    @staticmethod
    def parse_card(card_str: str) -> Tuple[str, str]:
        def convert(s: str) -> Tuple[str, str]:
            for k, v in Hand.RANK_STR.items():
                s = s.replace(k, v)
            s = sorted(s)
            l = list(s)
            if len(l) == 2:
                return l[1], l[0]
            elif len(l) == 3:
                n = l[0] + l[1]
                if n == "01": 
                    n = "10"
                return l[2], n
            else:
                raise Exception(f"Error parsing card {s}")

        return convert(card_str)

    @staticmethod
    def sort_cards(cards: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        def sort_key(card: Tuple[str, str]) -> int:
            return CardRank.RANKS[card[1]] * 10 + CardRank.SUITS[card[0]]

        cards = sorted(cards, key=sort_key)
        return cards

    def sort(self) -> Hand:
        self.cards = Hand.sort_cards(self.cards)
        return self

    ######################
    # SCORING
    # Based on https://www.adda52.com/poker/poker-rules/cash-game-rules/tie-breaker-rules
    ######################

    def score_straight_flush(self) -> Decimal:
        # All cards the same suit
        if len(self.suit_dict.keys()) != 1:
            return Decimal(HandRank.NONE)

        # Cards ascending monotonically by 1
        if not self.ascending_by_one:
            return Decimal(HandRank.NONE)

        # tiebreaker1 is the rank of the highest card in the hand
        tiebreaker1 = Decimal(CardRank.RANKS[self.cards[4][1]]) / Decimal(100)

        return Decimal(HandRank.STRAIGHT_FLUSH) + Decimal(tiebreaker1)

    def score_four_of_a_kind(self) -> Decimal:
        # find a rank with 4 elements
        four_search = list(filter(lambda c: len(c) == 4, self.rank_dict.values()))
        if not four_search:
            return Decimal(HandRank.NONE)

        # tiebreaker1 is the rank of the 4
        four_rank = four_search[0][0][1]
        tiebreaker1 = Decimal(CardRank.RANKS[four_rank]) / Decimal(math.pow(10, 2))

        # tiebreaker2 is the rank of the kicker
        kicker_key = list(self.rank_dict.keys() - four_rank)[0]
        kicker_card = self.rank_dict[kicker_key][0]
        tiebreaker2 = Decimal(CardRank.RANKS[kicker_card[1]]) / Decimal(math.pow(10, 4))

        return Decimal(HandRank.FOUR_OF_A_KIND) + tiebreaker1 + tiebreaker2

    def score_full_house(self) -> Decimal:
        # find a rank with 3 elements
        three_search = list(filter(lambda c: len(c) == 3, self.rank_dict.values()))
        if not three_search:
            return Decimal(HandRank.NONE)

        # find a rank with 2 elements
        two_search = list(filter(lambda c: len(c) == 2, self.rank_dict.values()))
        if not two_search:
            return Decimal(HandRank.NONE)

        # tiebreaker1 is the rank of the 3 of a kind
        three_rank = three_search[0][0][1]
        tiebreaker1 = Decimal(CardRank.RANKS[three_rank]) / Decimal(math.pow(10, 2))

        # tiebreaker2 is the rank of the 2 of a kind
        two_rank = two_search[0][0][1]
        tiebreaker2 = Decimal(CardRank.RANKS[two_rank]) / Decimal(math.pow(10, 4))

        return Decimal(HandRank.FULL_HOUSE) + tiebreaker1 + tiebreaker2

    def score_flush(self) -> Decimal:
        # All cards the same suit
        if len(self.suit_dict.keys()) != 1:
            return Decimal(HandRank.NONE)

        # tiebreakers 1..5 are the highest cards in descending order
        return Decimal(HandRank.FLUSH) + \
               sum(Decimal(CardRank.RANKS[self.cards[4 - i][1]]) / Decimal(math.pow(10, (i + 1) * 2)) for i in range(0, 5))

    def score_straight(self) -> Decimal:
        # Cards ascending monotonically by 1
        if not self.ascending_by_one:
            return Decimal(HandRank.NONE)

        # tiebreaker1 is the rank of the highest card in the hand
        tiebreaker1 = Decimal(CardRank.RANKS[self.cards[4][1]]) / Decimal(100)

        return Decimal(HandRank.STRAIGHT) + Decimal(tiebreaker1)

    def score_three_of_a_kind(self) -> Decimal:
        # find a rank with 3 elements
        three_search = list(filter(lambda c: len(c) == 3, self.rank_dict.values()))
        if not three_search:
            return Decimal(HandRank.NONE)

        # tiebreaker1 is the rank of the 3
        three_rank = three_search[0][0][1]
        tiebreaker1 = Decimal(CardRank.RANKS[three_rank]) / Decimal(math.pow(10, 2))

        kickers = list(reversed(Hand.sort_cards(functools.reduce(lambda a, b: a + b, [self.rank_dict[k] for k in list(
            self.rank_dict.keys() - three_rank)]))))
        # tiebreaker2 is the rank of the highest kicker
        tiebreaker2 = Decimal(CardRank.RANKS[kickers[0][1]]) / Decimal(math.pow(10, 4))
        # tiebreaker3 is the rank of the 2nd highest kicker
        tiebreaker3 = Decimal(CardRank.RANKS[kickers[1][1]]) / Decimal(math.pow(10, 6))

        return Decimal(HandRank.THREE_OF_A_KIND) + tiebreaker1 + tiebreaker2 + tiebreaker3

    def score_two_pairs(self) -> Decimal:
        # find 2 ranks with 2 elements
        two_search = list(filter(lambda c: len(c) == 2, self.rank_dict.values()))
        if len(two_search) != 2:
            return Decimal(HandRank.NONE)
        pair_rank_keys = list([p[0][1] for p in two_search])
        pair_ranks = sorted([CardRank.RANKS[p] for p in pair_rank_keys], reverse=True)

        # tiebreaker1 & 2 are the highest & second highest pair ranks
        tiebreaker1 = Decimal(pair_ranks[0]) / Decimal(math.pow(10, 2))
        tiebreaker2 = Decimal(pair_ranks[1]) / Decimal(math.pow(10, 4))

        # tiebreaker3 is the rank of the kicker
        kicker_key = list(set(self.rank_dict.keys()).difference(set(pair_rank_keys)))[0]
        tiebreaker3 = Decimal(CardRank.RANKS[kicker_key]) / Decimal(math.pow(10, 6))

        return Decimal(HandRank.TWO_PAIR) + tiebreaker1 + tiebreaker2 + tiebreaker3

    def score_pair(self) -> Decimal:
        pair_search = list(filter(lambda c: len(c) == 2, self.rank_dict.values()))
        if len(pair_search) != 1:
            return Decimal(HandRank.NONE)
        pair_rank_key = pair_search[0][1]
        pair_rank = CardRank.RANKS[pair_rank_key[1]]
        tiebreaker1 = Decimal(pair_rank) / Decimal(math.pow(10, 2))

        remaining_cards = Hand.sort_cards(list(set(self.cards).difference(pair_search[0])))

        return Decimal(HandRank.PAIR) + \
               tiebreaker1 + \
               sum(Decimal(CardRank.RANKS[remaining_cards[2 - i][1]]) / Decimal(math.pow(10, (i + 2) * 2)) for i in
                   range(0, 3))

    def score_high_card(self) -> Decimal:
        return Decimal(HandRank.HIGH_CARD) + \
               sum(Decimal(CardRank.RANKS[self.cards[4 - i][1]]) / Decimal(math.pow(10, (i + 1) * 2)) for i in range(0, 5))

    SCORE_RANK = [score_straight_flush, score_four_of_a_kind, score_full_house, score_flush, score_straight,
                  score_three_of_a_kind, score_two_pairs, score_pair, score_high_card]

    def score(self) -> Decimal:
        if len(self.cards) != 5:
            raise Exception("Can only score hands of 5 cards")

        for f in Hand.SCORE_RANK:
            score = f(self)
            if score != Decimal(HandRank.NONE):
                return score

    # Helper Methods
    def __str__(self):
        output = ""
        for c in self.cards:
            output += f"{c[0]}{c[1]}  "
        return output