# encoding : utf-8

import random

from BoardGame import *
from constants import *

class GameEngine:
    def __init__(self, players):
        if len(players) not in (3, 4, 5):
            raise ValueError('Wrong players number (must be 3, 4 or 5 and not {})'.format(len(players)))

        self.players = players
        self._board_game = BoardGame(self)

        for pl in players:
            pl.set_game_engine(self)

    def _get_board_game(self):
        return self._board_game
    def _set_board_game(self, bg):
        self._board_game = bg
    board_game = property(_get_board_game, _set_board_game)

    def get_players_nb(self):
        return len(self.players)
