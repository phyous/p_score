import unittest
from decimal import Decimal

from lib.hand import Hand
from lib.round_score import RoundScore
from lib.simple_round import SimpleRound


class TestHand(unittest.TestCase):

    def test_init(self):
        round = SimpleRound(num_players=4)

        self.assertEqual(4, len(round.player_hands.keys()))
        for ph in round.player_hands.values():
            self.assertEqual(2, len(ph.cards))

        self.assertEqual(5, len(round.community_cards.cards))

    def test_init_p1_override(self):
        round = SimpleRound(num_players=4, p1_override=Hand(["AS", "AD"]))

        self.assertEqual(4, len(round.player_hands.keys()))
        for ph in round.player_hands.values():
            self.assertEqual(2, len(ph.cards))

        self.assertEqual(5, len(round.community_cards.cards))
        self.assertEqual(round.player_hands[0].cards, Hand(["AS", "AD"]).cards)

    def test_round_score_generate_possible_hands(self):
        score = RoundScore.generate_possible_hands(
            Hand(["2S", "3D"]),
            Hand(["4S", "5D", "6C", "7D", "8H"])
        )

        self.assertEqual(21, len(score))
        self.assertEqual(21, len(set(score)))

    def test_round_score_val(self):
        p1 = Hand(["AS", "AD"])
        p2 = Hand(["KC", "AC"])
        community = Hand(["QC", "JC", "10C", "AH", "2S"])

        scores = RoundScore({1: p1, 2: p2}, community).compute_score()

        self.assertEqual(Decimal("4.141211"), scores[1])
        self.assertEqual(Decimal("9.14"), scores[2])

    def test_simple_round_outcome(self):
        p1 = Hand(["AS", "AD"])
        p2 = Hand(["KC", "AC"])
        community = Hand(["QC", "JC", "10C", "AH", "2S"])

        sr = SimpleRound(num_players=2)
        sr.player_hands = {1: p1, 2: p2}
        sr.community_cards = community

        self.assertEqual(SimpleRound.Outcome.LOSS, sr.determine_outcome(1))
        self.assertEqual(SimpleRound.Outcome.WIN, sr.determine_outcome(2))

    def test_simple_round_outcome_tie(self):
        p1 = Hand(["AS", "2D"])
        p2 = Hand(["AC", "2H"])
        community = Hand(["QC", "JC", "10C", "5H", "2S"])

        sr = SimpleRound(num_players=2)
        sr.player_hands = {1: p1, 2: p2}
        sr.community_cards = community

        self.assertEqual(SimpleRound.Outcome.TIE, sr.determine_outcome(1))
        self.assertEqual(SimpleRound.Outcome.TIE, sr.determine_outcome(2))



