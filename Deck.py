# encoding : utf-8

from Card import *
from constants import *

class Deck:
    def __init__(self, cards=None):
        if cards == None:
            self._cards = list()
        else:
            self._cards = list(cards)

    def get_score(self):
        return sum(c.get_score() for c in self._cards)

    def _get_cards(self):
        return self._cards
    def _set_cards(self, c):
        self._cards = c

    cards = property(_get_cards, _set_cards)

    def get_cards_nb(self):
        return len(self._cards)

    def get_oudlers(self):
        return [o for o in self._cards if isinstance(o, Oudler)]

    def get_oudlers_nb(self):
        return len(self.get_oudlers())

    def split(self, pos):
        d1 = Deck(self._cards[:pos])
        d2 = Deck(self._cards[pos:])

        return d1, d2

    def __add__(self, deck):
        return Deck(self._cards + deck._cards)

    def pop_cards(self, n):
        return Deck([self._cards.pop() for _ in range(n)])

    def push_cards(self, cards):
        self._cards += cards

    def get_trump_cards(self):
        return [c for c in self._cards if isinstance(c, Trump)]

    def get_highest_trump_card(self):
        _trumps = self.get_trump_cards()
        max_v = 0 if _trumps == [] else max(t.get_value() for t in _trumps)
        for t in _trumps:
            if t.get_value() == max_v:
                return t

    def get_higher_trump_cards(self, value):
        _trumps = self.get_trump_cards()

        h_t = []
        for _t in _trumps:
            if _t.get_value() > value:
                h_t.append(_t)
        return h_t

    def get_excuse(self):
        for c in self._cards:
            if isinstance(c, Excuse):
                return c
        else:
            return None

    def get_cards_with_specific_suit(self, suit):
        return [c for c in self._cards if (isinstance(c, Card) and c.get_suit() == suit)]

    def get_highest_card_with_specific_suit(self, suit):
        c = self.get_cards_with_specific_suit(suit)
        c_v = [VALUES.index(c_i.get_value()) for c_i in c]
        return c[c_v.index(max(c_v))]

    def __repr__(self):
        return self.cards.__repr__()
