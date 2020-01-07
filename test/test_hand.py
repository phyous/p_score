import unittest
from decimal import Decimal
from lib.deck import Deck
from lib.hand import Hand


class TestHand(unittest.TestCase):

    def test_sort(self):
        deck = Deck().shuffle()
        hand = Hand(deck.cards)
        srted = [c for c in hand.sort().cards]
        expected = [('♣', '2'), ('♢', '2'), ('♡', '2'), ('♠', '2'), ('♣', '3'), ('♢', '3'), ('♡', '3'), ('♠', '3'),
                    ('♣', '4'), ('♢', '4'), ('♡', '4'), ('♠', '4'), ('♣', '5'), ('♢', '5'), ('♡', '5'), ('♠', '5'),
                    ('♣', '6'), ('♢', '6'), ('♡', '6'), ('♠', '6'), ('♣', '7'), ('♢', '7'), ('♡', '7'), ('♠', '7'),
                    ('♣', '8'), ('♢', '8'), ('♡', '8'), ('♠', '8'), ('♣', '9'), ('♢', '9'), ('♡', '9'), ('♠', '9'),
                    ('♣', '10'), ('♢', '10'), ('♡', '10'), ('♠', '10'), ('♣', 'J'), ('♢', 'J'), ('♡', 'J'), ('♠', 'J'),
                    ('♣', 'Q'), ('♢', 'Q'), ('♡', 'Q'), ('♠', 'Q'), ('♣', 'K'), ('♢', 'K'), ('♡', 'K'), ('♠', 'K'),
                    ('♣', 'A'), ('♢', 'A'), ('♡', 'A'), ('♠', 'A')]
        self.assertEqual(srted, expected)

    def test_ascending_by_one(self):
        self.assertEqual(False, Hand(["7H", "6H", "5H", "8H", "3H"]).ascending_by_one)

    def test_pase_card(self):
        self.assertEqual(('♣', '10'), Hand.parse_card("10C"))
        self.assertEqual(('♣', '10'), Hand.parse_card("C10"))
        self.assertEqual(('♣', '10'), Hand.parse_card("10♣"))
        self.assertEqual(('♣', '10'), Hand.parse_card("♣10"))

        self.assertEqual(('♡', 'A'), Hand.parse_card("AH"))
        self.assertEqual(('♡', 'A'), Hand.parse_card("HA"))
        self.assertEqual(('♡', 'A'), Hand.parse_card("A♡"))
        self.assertEqual(('♡', 'A'), Hand.parse_card("♡A"))

        self.assertEqual(('♡', '2'), Hand.parse_card("2H"))
        self.assertEqual(('♡', '2'), Hand.parse_card("H2"))
        self.assertEqual(('♡', '2'), Hand.parse_card("2♡"))
        self.assertEqual(('♡', '2'), Hand.parse_card("♡2"))

    def test_score_straight_flush(self):
        self.assertEqual(Decimal("9.06"), Hand(["2C", "3C", "4C", "5C", "6C"]).score_straight_flush())
        self.assertEqual(Decimal("9.14"), Hand(["10H", "JH", "QH", "KH", "AH"]).score_straight_flush())
        self.assertEqual(Decimal("0"), Hand(["2C", "3C", "4C", "5C", "6H"]).score_straight_flush())
        self.assertEqual(Decimal("0"), Hand(["2C", "3C", "4C", "5C", "7C"]).score_straight_flush())

    def test_score_four_of_a_kind(self):
        self.assertEqual(Decimal("8.0602"), Hand(["6C", "6H", "6S", "6D", "2C"]).score_four_of_a_kind())
        self.assertEqual(Decimal("8.1413"), Hand(["AC", "AH", "AS", "AD", "KC"]).score_four_of_a_kind())
        self.assertEqual(Decimal("0"), Hand(["AC", "KH", "AS", "AD", "KC"]).score_four_of_a_kind())
        self.assertEqual(Decimal("0"), Hand(["AC", "2H", "AS", "AD", "KC"]).score_four_of_a_kind())

    def test_score_full_house(self):
        self.assertEqual(Decimal("7.0602"), Hand(["6C", "6H", "6S", "2D", "2C"]).score_full_house())
        self.assertEqual(Decimal("7.1413"), Hand(["AC", "AH", "AS", "KD", "KC"]).score_full_house())
        self.assertEqual(Decimal("0"), Hand(["AC", "AH", "AS", "AD", "KC"]).score_full_house())
        self.assertEqual(Decimal("0"), Hand(["AC", "2H", "AS", "AD", "KC"]).score_full_house())

    def test_score_flush(self):
        self.assertEqual(Decimal("6.1413110706"), Hand(["KH", "6H", "AH", "7H", "JH"]).score_flush())
        self.assertEqual(Decimal("6.0706050403"), Hand(["7H", "6H", "5H", "4H", "3H"]).score_flush())
        self.assertEqual(Decimal("0"), Hand(["AC", "AH", "AS", "AD", "KC"]).score_flush())
        self.assertEqual(Decimal("0"), Hand(["AC", "2C", "KC", "4C", "KD"]).score_flush())

    def test_score_straight(self):
        self.assertEqual(Decimal("5.06"), Hand(["2C", "3C", "4C", "5C", "6C"]).score_straight())
        self.assertEqual(Decimal("5.13"), Hand(["KC", "JC", "9C", "10C", "QD"]).score_straight())
        self.assertEqual(Decimal("0"), Hand(["AC", "AH", "AS", "AD", "KC"]).score_straight())
        self.assertEqual(Decimal("0"), Hand(["2C", "3C", "4C", "5C", "AC"]).score_straight())

    def test_score_three_of_a_kind(self):
        self.assertEqual(Decimal("4.020605"), Hand(["2C", "2H", "2D", "5C", "6C"]).score_three_of_a_kind())
        self.assertEqual(Decimal("4.141312"), Hand(["AC", "AH", "AD", "KC", "QC"]).score_three_of_a_kind())
        self.assertEqual(Decimal("4.141313"), Hand(["AC", "AH", "AD", "KC", "KH"]).score_three_of_a_kind())
        self.assertEqual(Decimal("0"), Hand(["AC", "2H", "AD", "KC", "KH"]).score_three_of_a_kind())

    def test_score_two_pairs(self):
        self.assertEqual(Decimal("3.140206"), Hand(["2C", "2H", "AD", "AC", "6C"]).score_two_pairs())
        self.assertEqual(Decimal("3.131214"), Hand(["KC", "KH", "QD", "QC", "AC"]).score_two_pairs())
        self.assertEqual(Decimal("0"), Hand(["KC", "5H", "2D", "QC", "AC"]).score_two_pairs())
        self.assertEqual(Decimal("0"), Hand(["KC", "KH", "6D", "QC", "AC"]).score_two_pairs())

    def test_pair(self):
        self.assertEqual(Decimal("2.02141306"), Hand(["2C", "2H", "KD", "AC", "6C"]).score_pair())
        self.assertEqual(Decimal("2.14130806"), Hand(["AC", "AH", "KD", "8C", "6C"]).score_pair())
        self.assertEqual(Decimal("0"), Hand(["2C", "2H", "AD", "AC", "6C"]).score_pair())
        self.assertEqual(Decimal("0"), Hand(["2C", "5H", "9D", "AC", "6C"]).score_pair())

    def test_high_card(self):
        self.assertEqual(Decimal("1.1413060202"), Hand(["2C", "2H", "KD", "AC", "6C"]).score_high_card())
        self.assertEqual(Decimal("1.1414141402"), Hand(["AC", "AH", "AD", "AS", "2C"]).score_high_card())

    def test_score(self):
        self.assertEqual(Decimal("9.06"), Hand(["2C", "3C", "4C", "5C", "6C"]).score())
        self.assertEqual(Decimal("8.0602"), Hand(["6C", "6H", "6S", "6D", "2C"]).score())
        self.assertEqual(Decimal("7.0602"), Hand(["6C", "6H", "6S", "2D", "2C"]).score())
        self.assertEqual(Decimal("6.0807060503"), Hand(["7H", "6H", "5H", "8H", "3H"]).score())
        self.assertEqual(Decimal("5.13"), Hand(["KC", "JC", "9C", "10C", "QD"]).score())
        self.assertEqual(Decimal("4.141312"), Hand(["AC", "AH", "AD", "KC", "QC"]).score())
        self.assertEqual(Decimal("3.131214"), Hand(["KC", "KH", "QD", "QC", "AC"]).score())
        self.assertEqual(Decimal("2.14130806"), Hand(["AC", "AH", "KD", "8C", "6C"]).score())
        self.assertEqual(Decimal("1.1413060302"), Hand(["2C", "3H", "KD", "AC", "6C"]).score())

    def test_score_2(self):
        # test cases taken from: https://en.wikipedia.org/wiki/List_of_poker_hands
        test_cases = [['AH', 'KH', 'QH', 'JH', '10H'],
                      ['10C', '9C', '8C', '7C', '6C'],
                      ['8H', '7H', '6H', '5H', '4H'],
                      ['7D', '6D', '5D', '4D', '3D'],
                      ['7S', '6S', '5S', '4S', '3S'],
                      ['6S', '5S', '4S', '3S', '2S'],
                      ['KS', 'KH', 'KC', 'KD', '3H'],
                      ['7H', '7D', '7S', '7C', 'QH'],
                      ['7H', '7D', '7S', '7C', '10S'],
                      ['4C', '4S', '4D', '4H', '9C'],
                      ['4C', '4S', '4D', '4H', '9D'],
                      ['KC', 'KS', 'KD', 'JC', 'JS'],
                      ['KC', 'KH', 'KD', 'JC', 'JH'],
                      ['8S', '8D', '8H', '7D', '7C'],
                      ['4D', '4S', '4C', '9D', '9C'],
                      ['4D', '4S', '4C', '5C', '5D'],
                      ['KD', 'JD', '9D', '6D', '4D'],
                      ['QC', 'JC', '7C', '6C', '5C'],
                      ['JH', '10H', '9H', '4H', '2H'],
                      ['JS', '10S', '8S', '6S', '3S'],
                      ['JH', '10H', '8H', '4H', '3H'],
                      ['JC', '10C', '8C', '4C', '2C'],
                      ['10D', '8D', '7D', '6D', '5D'],
                      ['10S', '8S', '7S', '6S', '5S'],
                      ['JH', '10H', '9C', '8S', '7H'],
                      ['10S', '9S', '8C', '7H', '6S'],
                      ['9C', '8C', '7C', '6D', '5D'],
                      ['9S', '8S', '7S', '6H', '5H'],
                      ['9S', '9H', '9D', '10D', '8H'],
                      ['9C', '9S', '9H', '10D', '8D'],
                      ['6H', '6D', '6S', 'QC', '4S'],
                      ['3D', '3S', '3C', 'KS', '2S'],
                      ['3D', '3S', '3C', 'JC', '7H'],
                      ['3D', '3S', '3C', 'JS', '5D'],
                      ['KD', 'KS', '7D', '7H', '8H'],
                      ['KC', 'KS', '7C', '7H', '8C'],
                      ['10D', '10S', '2S', '2C', 'KC'],
                      ['5C', '5S', '4D', '4H', '10H'],
                      ['5C', '5S', '3C', '3D', 'QS'],
                      ['5C', '5S', '3C', '3D', 'JS'],
                      ['9C', '9D', 'QS', 'JH', '5H'],
                      ['8S', '8D', '10H', '6C', '5S'],
                      ['8H', '8C', '10C', '6S', '5C'],
                      ['6D', '6H', 'KS', '7H', '4C'],
                      ['6D', '6H', 'QH', 'JS', '2C'],
                      ['6D', '6H', 'QS', '8C', '7D'],
                      ['6D', '6H', 'QD', '8H', '3S'],
                      ['KS', '6C', '5H', '3D', '2C'],
                      ['QS', 'JD', '6C', '5H', '3C'],
                      ['QS', '10D', '8C', '7D', '4S'],
                      ['QH', '10H', '7C', '6H', '4S'],
                      ['QC', '10C', '7D', '5C', '4D'],
                      ['QH', '10D', '7S', '5S', '2H'],
                      ['10C', '8S', '7S', '6H', '4D'],
                      ['10D', '8D', '7S', '6C', '4C']]

        scores = list(map(lambda t: Hand(t).score(), test_cases))
        # Check generated scores are strictly descending
        self.assertEqual(scores, sorted(scores, reverse=True))


if __name__ == '__main__':
    unittest.main()
