# encoding : utf-8

from Card import *
from Deck import *

class Player:
    def __init__(self, name):
        self._name = name
        self._hand_deck = Deck()
        self._won_deck = Deck()

    def _get_hand_deck(self):
        return self._hand_deck
    def _set_hand_deck(self, deck):
        self._hand_deck = deck
    hand_deck = property(_get_hand_deck, _set_hand_deck)

    def _get_won_deck(self):
        return self._won_deck
    def _set_won_deck(self, deck):
        self._won_deck = deck
    won_deck = property(_get_won_deck, _set_won_deck)

    def set_game_engine(self, game_engine):
        self._game_engine = game_engine
        self._board_game = game_engine.board_game

    def play_card(self, card):
        print("{} played {}".format(self._name, card))
        self.hand_deck.cards.remove(card)
        _current_trick = self._board_game.get_current_trick()
        _current_trick.push_cards([card])
