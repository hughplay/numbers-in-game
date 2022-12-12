import math
import random
import re

import matplotlib.pyplot as plt
import numpy as np
from treys.card import Card
from treys.deck import Deck
from treys.evaluator import Evaluator


class CustomDeck(Deck):
    def __init__(
        self, seed: int = None, suits: str = "shdc", ranks="23456789TJQKA"
    ):
        self.suits = suits
        self.ranks = ranks
        super().__init__(seed)

    def shuffle(self) -> None:
        self.cards = CustomDeck.GetFullDeck(suits=self.suits, ranks=self.ranks)
        self._random.shuffle(self.cards)

    @staticmethod
    def GetFullDeck(suits: str = "shdc", ranks="23456789TJQKA") -> list[int]:
        if CustomDeck._FULL_DECK:
            return list(CustomDeck._FULL_DECK)

        for rank in ranks:
            for suit in suits:
                CustomDeck._FULL_DECK.append(Card.new(rank + suit))

        return list(CustomDeck._FULL_DECK)


class Simulator:
    def __init__(
        self,
        seed: int = 0,
        suits: str = "shdc",
        ranks="23456789TJQKA",
        n_players: int = 2,
    ):
        self.suits = suits
        self.ranks = ranks
        self.n_players = n_players

        random.seed(seed)
        self.evaluator = Evaluator()

    def step(self, verbose: bool = False):
        self.deck = CustomDeck(suits=self.suits, ranks=self.ranks)
        board = self.deck.draw(5)
        hands = [self.deck.draw(2) for _ in range(self.n_players)]
        ranks = [self.evaluator.evaluate(hand, board) for hand in hands]
        data = {
            "board": board,
            "hands": hands,
            "ranks": ranks,
        }

        if verbose:
            print(f"Board: {Card.ints_to_pretty_str(board)}")
            for i, hand in enumerate(hands):
                print(f"Hand {i}: {Card.ints_to_pretty_str(hand)}")
            self.evaluator.hand_summary(board, hands)

        return data

    def run(self, n=100, progress_bar=False):
        records = []

        rounds = range(n)
        if progress_bar:
            try:
                from tqdm import trange

                rounds = trange(n, ncols=80)
            except ImportError:
                print("warning: tqdm not installed, progress bar disabled")

        for _ in rounds:
            records.append(self.step())
        return records
