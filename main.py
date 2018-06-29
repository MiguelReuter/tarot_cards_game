# encoding: utf-8

from constants import *
import GameEngine
from Player import *

if __name__ == "__main__":
    players = [Player("player " + str(i)) for i in range(4)]

    game = GameEngine.GameEngine(players)
    bg = game._board_game
    bg.mix_deck()
    bg.deal()


    for _ in range(CARDS_NB_PER_PLAYER[len(players)]):
        print("*"*50)
        bg.new_turn()


    for p in players:
        print(p.won_deck.get_score())

    print(sum(p.won_deck.get_score() for p in players) + bg._dog.get_score())
