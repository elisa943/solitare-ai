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
        for i in range(14):
            for j in range(4):
                self.stockpile.append((Rank(i), Suit(j)))
        random.shuffle(self.stockpile)

    def picks_cards(numOfCards, withdraw=True):
        cardsPicked = []
        for i in range(min(numOfCards, len(self.stockpile))):
            cardsPicked.append(self.stockpile.pop(-1))
        
        return cardsPicked

        if not(withdraw):
            for card in cardsPicked:
                self.stockpile.append(card)
                
        return cardsPicked



class Table():
    def __init__(self):
        self.cardsOnTable = [[] for _ in range(NUM_TABLE)]


class FoundationPiles():
    def __init__(self):
        self.cardsOnPiles = [[] for _ in range(NUM_PILES)]

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

pygame.display.quit()
pygame.quit()
sys.exit()
