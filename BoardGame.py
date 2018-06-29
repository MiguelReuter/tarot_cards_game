# encoding : utf-8

import random

from constants import *
from Card import *
from Deck import *

class BoardGame:
    def __init__(self, game_engine):
        self._game_engine = game_engine
        # decks
        self._dog = Deck()
        self._last_trick = None
        self._current_trick = Deck()

        self._deck = self.init_deck()

        # players
        self._taker = game_engine.players[0]
        self._dealer = game_engine.players[0]
        self._last_trick_leader = game_engine.players[0]

    def set_dog(self, dog):
        self._dog = dog

    def get_last_trick(self):
        return self._last_trick

    def get_current_trick(self):
        return self._current_trick

    def init_deck(self):
        _cards = []
        # standard cards
        for c in SUITS:
            for v in VALUES:
                _cards.append(Card(c, v))
        # atouts
        for v in range(2, 21):
            _cards.append(Trump(v))
        # bouts
        _cards.append(Trump1())
        _cards.append(Trump21())
        _cards.append(Excuse())

        return Deck(_cards)

    def mix_deck(self):
        random.shuffle(self._deck._cards)

    def cut_deck(self, pos):
        self._deck = Deck(self._deck._cards[pos:] + self._deck._cards[:pos])

    def deal(self):
        pl_n = self._game_engine.get_players_nb()

        target_dog_size = DOG_SIZE[pl_n]
        target_cards_nb_per_player = CARDS_NB_PER_PLAYER[pl_n]

        dog_deal_idx = random.sample(range(1, int(target_cards_nb_per_player * pl_n / 3) - 1), target_dog_size)
        dog_deal_idx.sort()

        current_p_i = 0
        packets_nb = int(target_cards_nb_per_player * pl_n / 3) + target_dog_size
        for packet_i in range(packets_nb):
            if packet_i in dog_deal_idx:
                self._dog += self._deck.pop_cards(1)
            else:
                self._game_engine.players[current_p_i]._hand_deck += self._deck.pop_cards(3)
                current_p_i = (current_p_i + 1) %  pl_n

    def get_playable_cards(self, player):
        pl_hand_deck = player.hand_deck
        # if player is the first to play
        if self._current_trick.get_cards_nb() == 0:
            return pl_hand_deck.cards

        fst_card_played = self._current_trick.cards[0]
        # Excuse played
        if isinstance(fst_card_played, Excuse):
            if self._current_trick.get_cards_nb() == 1:
                return pl_hand_deck.cards
            else:
                fst_card_played = self._current_trick.cards[1]
        # Trump played
        if isinstance(fst_card_played, Trump):
            pl_trumps = pl_hand_deck.get_trump_cards()
            # no trump in player's hand
            if len(pl_trumps) == 0:
                return pl_hand_deck.cards
            else:
                highest_trump_played = self._current_trick.get_highest_trump_card()
                c = pl_hand_deck.get_higher_trump_cards(highest_trump_played.get_value())

                if len(c) > 0:
                    if pl_hand_deck.get_excuse() != None:
                        return c + [pl_hand_deck.get_excuse()]
                    else:
                        return c
                else:
                    return pl_trumps
        # Standard card played
        else:
            suit = fst_card_played.get_suit()
            c = pl_hand_deck.get_cards_with_specific_suit(suit)
            if len(c) > 0:
                if pl_hand_deck.get_excuse() != None:
                    return c + [pl_hand_deck.get_excuse()]
                else:
                    return c
            else:
                pl_trumps = pl_hand_deck.get_trump_cards()
                if len(pl_trumps) == 0:
                    return pl_hand_deck.cards
                else:
                    highest_trump_played = self._current_trick.get_highest_trump_card()
                    c = pl_hand_deck.get_higher_trump_cards(0 if highest_trump_played == None else highest_trump_played.get_value())
                    if len(c) > 0:
                        if pl_hand_deck.get_excuse() != None:
                            return c + [pl_hand_deck.get_excuse()]
                        else:
                            return c
                    else:
                        return pl_trumps

    def new_turn(self, last_turn=False):
        self._current_trick = Deck()
        players = self._game_engine.players

        for pl_i in range(self._game_engine.get_players_nb()):
            last_trick_leader_index = self._game_engine.players.index(self._last_trick_leader)

            pl = players[(pl_i + last_trick_leader_index) % self._game_engine.get_players_nb()]
            c = self.get_playable_cards(pl)
            pl.play_card(c[0])


        # add trick to the winner
        self.get_trick_winner().won_deck += self.get_current_trick()


        self._last_trick_leader = self.get_trick_winner()
        print("winner : ", self._last_trick_leader._name)




    def get_trick_winner(self):
        winner_index = -1
        trick = self.get_current_trick()

        highest_trump = trick.get_highest_trump_card()
        if highest_trump != None:
            winner_index = trick.cards.index(highest_trump)
        else:
            if isinstance(trick.cards[0], Excuse) == False:
                first_card = trick.cards[0]
            else:
                first_card = trick.cards[1]
            winner_index = trick.cards.index(trick.get_highest_card_with_specific_suit(first_card.get_suit()))

        # get winner (offset because players[0] is not necesserly the first to play)
        leader_index = (self._game_engine.players.index(self._last_trick_leader) + winner_index) % self._game_engine.get_players_nb()

        return self._game_engine.players[leader_index]
