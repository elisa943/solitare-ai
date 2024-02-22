import pygame
import sys
import random
from math import sqrt
from time import sleep
from pygame import mixer
from enum import Enum

# Initialization
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((800, 800))

# Title and Icon
pygame.display.set_caption("Solitaire AI")
icon = pygame.image.load("images/icon.jpeg")
pygame.display.set_icon(icon)

# Variables
NUM_TABLE = 7
NUM_PILES = 4

class ImplementationError(Exception):
    pass

class Rank(Enum):
    ACE = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5 
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

class Suit(Enum):
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3

class Deck():
    def __init__(self):
        self.stockpile = []

        # Adds all possible cards
        for i in range(14):
            for j in range(4):
                self.stockpile.append((Rank(i), Suit(j)))

        # Deck is shuffled at the very beginning 
        random.shuffle(self.stockpile)

    # Picks one card at the top of the deck
    def picks_card(self, withdraw=True):

        cardPicked = self.stockpile.pop(-1)

        if not(withdraw):
            self.stockpile.append(card)

        return cardPicked


class Table():
    def __init__(self, startingDeck):
        self.cardsOnTable = [[] for _ in range(NUM_TABLE)]

        # Each part of the table is a Queue containing tuples (card, hidden) with hidden being a boolean
        for i in range(NUM_TABLE):

            # Adds hidden card(s) 
            for j in range(i):
                self.cardsOnTable[i].append((startingDeck.picks_card(), True))

            # Adds the first card shown
            self.cardsOnTable[i].append((startingDeck.picks_card(), False))



class FoundationPiles():
    def __init__(self):
        self.cardsOnPiles = {}
        for i in range(NUM_PILES):
            self.cardsOnPiles[Suit(i)] = -1
    
    def receives_card(s):
        if self.cardsOnPiles[s] == KING:
            raise ImplementationError
        else:
            self.cardsOnPiles[s] += 1
    
    def gives_card(s):
        if self.cardsOnPiles[s] == -1:
            raise ImplementationError
        else:
            self.cardsOnPiles[s] -= 1

class Player():
    def __init__(self, deck, table, foundationPiles):
        self.deck = deck
        self.table = table
        self.foundationPiles = foundationPiles


class PlayerAI():
    def __init__(self, deck, table, foundationPiles):
        self.deck = deck
        self.table = table
        self.foundationPiles = foundationPiles

d = Deck()
t = Table(d)


pygame.display.quit()
pygame.quit()
sys.exit()
