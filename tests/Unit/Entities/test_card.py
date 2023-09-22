from modules.Entities.Card import Card

import unittest


class CardTest(unittest.TestCase):

    def test_valid_card(self):
        card = Card('1234567890123456', '12', '24', '123', 'Visa')
        self.assertTrue(card.is_valid())
        card = Card('1234567890123456', '01', '24', '123', 'Visa')
        self.assertTrue(card.is_valid())

    def test_invalid_card_number(self):
        card = Card('123456789012345A', '12', '23', '123', 'Visa')
        self.assertFalse(card.is_valid())

    def test_invalid_card_year(self):
        card = Card('123456789012345A', '12', '2', '123', 'Visa')
        self.assertFalse(card.is_valid())

    def test_mask(self):
        card = Card('1234567890123456', '12', '24', '123', 'Visa')
        self.assertEqual('************3456', card.mask())
