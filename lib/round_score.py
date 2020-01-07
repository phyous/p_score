from decimal import Decimal
from typing import List, Dict, Tuple

from lib.hand import Hand


class RoundScore:
    def __init__(self, player_hands: Dict[int, Hand], community_cards: Hand):
        self.player_hands = player_hands
        self.community_cards = community_cards
        self.scores = self.compute_score()

    @staticmethod
    def generate_possible_hands(player_hand: Hand, community_cards: Hand) -> List[Hand]:
        possible_hands = [Hand(community_cards.cards.copy())]
        for i in range(0, 5):
            clone1 = community_cards.cards.copy()
            clone2 = clone1.copy()
            clone1[i] = player_hand.cards[0]
            clone2[i] = player_hand.cards[1]

            possible_hands += [Hand(clone1), Hand(clone2)]

        for i in range(0, 5):
            for j in range(0, 5):
                if i != j and i > j:
                    clone = community_cards.cards.copy()
                    clone[i] = player_hand.cards[0]
                    clone[j] = player_hand.cards[1]
                    possible_hands.append(Hand(clone))

        return possible_hands

    SCORE_CACHE = {}

    def compute_score(self, cache: bool = True) -> Dict[int, Decimal]:
        scores = {}
        for player_id, hand in self.player_hands.items():
            possible_hands = RoundScore.generate_possible_hands(hand, self.community_cards)
            score_list = []
            for h in possible_hands:
                hand_key = str(h)
                if cache and hand_key in RoundScore.SCORE_CACHE:
                    score_list.append(RoundScore.SCORE_CACHE[hand_key])
                else:
                    h_score = h.score()
                    score_list.append(h_score)
                    if cache: RoundScore.SCORE_CACHE[hand_key] = h_score
            scores[player_id] = max(score_list)
        return scores

    def winner(self) -> List[Tuple[int, Decimal]]:
        def sort_key(v: Tuple[int, Decimal]) -> Decimal:
            return v[1]

        sorted_scores = sorted( [(k, v) for k, v in self.scores.items()], key=sort_key, reverse=True)
        winning_score = sorted_scores[0][1]
        return list(filter(lambda s: s[1] == winning_score, sorted_scores))