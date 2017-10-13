from modules.Entities.Card import Card

import unittest


class CardTest(unittest.TestCase):

    def test_valid_card(self):
        card = Card('1234ABCD', '1234', '12', '25', 'Visa')
        self.assertTrue(card.is_valid())
        card = Card('1234ABCD', '1234', '01', '26', 'Visa')
        self.assertTrue(card.is_valid())

    def test_invalid_card_number(self):
        card = Card('1234ABCD', '123', '12', '25', 'Visa')
        self.assertFalse(card.is_valid())

    def test_invalid_card_year(self):
        card = Card('1234ABCD', '1234', '12', '2', 'Visa')
        self.assertFalse(card.is_valid())
