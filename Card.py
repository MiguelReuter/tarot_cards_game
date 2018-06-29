# encoding : utf-8

class AbstractCard:
    # encoding : utf-8
    def __init__(self):
        self._score = 0.5

    def get_score(self):
        return self._score


class Oudler(AbstractCard):
    def __init__(self):
        self._score = 4.5


class Card(AbstractCard):
    def __init__(self, suit, value):
        super().__init__()
        self._suit = suit
        self._value = value
        self._set_score()

    def _set_score(self):
        if self._value == "V":
            self._score = 1.5
        elif self._value == "C":
            self._score = 2.5
        elif self._value == "D":
            self._score = 3.5
        elif self._value == "R":
            self._score = 4.5

    def get_value(self):
        return self._value

    def get_suit(self):
        return self._suit

    def __repr__(self):
        return self._suit + " " + str(self._value)


class Trump(AbstractCard):
    def __init__(self, value):
        super().__init__()
        self._value = value

    def get_value(self):
        return self._value

    def __repr__(self):
        return "# " + str(self._value)


# Oudlers
class Trump1(Trump, Oudler):
    def __init__(self):
        Trump.__init__(self, 1)
        Oudler.__init__(self)

    def __repr__(self):
        return "Petit"


class Trump21(Trump, Oudler):
    def __init__(self):
        Trump.__init__(self, 21)
        Oudler.__init__(self)

    def __repr__(self):
        return "21"


class Excuse(Oudler):
    def __init__(self):
        Oudler.__init__(self)

    def __repr__(self):
        return "Excuse"
