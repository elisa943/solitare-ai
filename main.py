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
NUM_RANKS = 14
NUM_SUITS = 4

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
    SPADES = 2
    HEARTS = 3

class Deck():
    def __init__(self):
        self.stockpile = []
        self.cardsShown = []

        # Adds all possible cards
        for i in range(14):
            for j in range(4):
                self.stockpile.append((Rank(i), Suit(j)))

        # Deck is shuffled at the very beginning 
        random.shuffle(self.stockpile)

    # Picks one card at the top of the deck
    def picks_card(self, withdraw=True):

        cardPicked = self.stockpile.pop(-1)

        # If asked not to withdraw the card, puts it back in the deck 
        if not(withdraw):
            self.stockpile.append(card)

        return cardPicked
    
    def reinitialize_deck(self):
        # If the deck is empty, re-initialize it
        if len(self.stockpile) == 0:
            self.stockpile = self.cardsShown.reverse()
            self.cardsShown = []

        # Else, does nothing

    def shows_3_cards(self):
        """
        Displays up to 3 cards by adding them to self.cardsShown
        """

        # If impossible to display new cards, re-initialize the deck
        if len(self.stockpile) == 0:
            raise ImplementationError
        
        # Else, adds up to 3 cards the cardsShown list
        for _ in range(min(3, len(self.stockpile))):
            newCard = self.picks_card()
            self.cardsShown.append(newCard)


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
    
    def cards_compatible(self, cardUp, cardDown):
        """
        Returns True if we can put cardDown under cardUp
        """
        # Checks if cardUp's rank is equal to cardDown's rank + 1 
        if cardUp[0] != cardDown[0] + 1:
            return False 
        
        # Checks if cardUp's suit is the same color as cardDown's
        if cardUp[1] % 2 != cardDown[1] % 2:
            return False

        return True

    def contains_card(self, index, card):
        """
        Checks if the index contains the card
        """
        for (c, hidden) in self.cardsOnTable[index]:
            if not(hidden) and c == card:
                return True 
        return False 

    def stack_of_cards(self, index, card):
        """
        Returns a sublist of self.cardsOnTable[index] with card being the first element 
        and deletes it from the deck. 
        """
        if not(self.contains_card(index, card)):
            raise ImplementationError
        
        num_cards = len(self.cardsOnTable[index])
        i = 0
        indexOfCard = None

        while i < num_cards and indexOfCard == None:
            
            # If the card is found and it's not hidden, takes its index
            if self.cardsOnTable[index][i][0] == card and not(self.cardsOnTable[index][i][0][1]) :
                indexOfCard = i
            
            i += 1
        
        res = self.cardsOnTable[index][indexOfCard:num_cards]

        # Deletes those cards
        for _ in range(indexOfCard, num_cards):
            self.cardsOnTable[index].pop(-1)

        return res

    def adds_stack_of_cards(self, index, stack):
        """
        Given a stack of cards, adds that stack in the table's index. 
        """
        for card in stack:
            self.cardsOnTable[index].append(card)

    def makes_move_in_table(self, move):
        """
        Returns True if the move is made. 
        'move' is a tuple containing (source, destination, card) with : 
            - source : int, index of the table 
            - destination : int, index of the table 
            - card : (Rank, Suit), card

        The move is relative to the table and not the foundation piles
        """
        source = move[0]
        destination = move[1]
        card = move[2]

        # Checks if the source index contains the card
        if not(self.contains_card(source, card)):
            raise ImplementationError

        # Takes the last card of the destination 
        lastCardOfDestination = self.cardsOnTable[destination][-1]

        # If those cards are compatible, makes the move 
        if self.cards_compatible(lastCardOfDestination, card):
            
            to_be_moved = self.stack_of_cards(source, card)
            self.adds_stack_of_cards(destination, to_be_moved)

            # Reveals the last card from source index if possible 
            if len(self.cardsOnTable[source]) > 0:
                self.cardsOnTable[source][-1][1] = False 

            return True
        else:
            return False


class FoundationPiles():
    def __init__(self):
        self.cardsOnPiles = {}
        for i in range(NUM_PILES):
            self.cardsOnPiles[Suit(i)] = -1
    
    def receives_card(self, s):
        if self.cardsOnPiles[s] == KING:
            raise ImplementationError
        else:
            self.cardsOnPiles[s] += 1
    
    def gives_card(self, s):
        if self.cardsOnPiles[s] == -1:
            raise ImplementationError
        else:
            self.cardsOnPiles[s] -= 1

    def game_won(self):
        """
        Returns True if the game is won
        """
        for i in range(NUM_PILES):
            
            if self.cardsOnPiles[Suit(i)] != Rank(13):
                return False

        return True 
    
    def adds_to_piles(self, card):
        """
        Returns True of the card can be added on top of the pile foundation
        """
        rank = card[0]
        suit = card[1]

        # If card can be added on pile foundation, then it's added and returns True
        if self.cardsOnPiles[suit] == rank - 1:
            self.cardsOnPiles[suit] += 1
            return True
        else:
            return False




class Player():
    def __init__(self, deck, table, foundationPiles):
        self.deck = deck
        self.table = table
        self.foundationPiles = foundationPiles
    
    def possible_actions(self):
        """
        TODO : Returns list of possibles actions
        """
        possibleActions = []

        # ! Check if cards shown on deck can be used 

        # ! Checks if cards in the table can be moved 
            # Checks if cards can be moved inside the table or onto the foundation pile
        
        return possible_actions


class PlayerAI():
    def __init__(self, deck, table, foundationPiles):
        self.deck = deck
        self.table = table
        self.foundationPiles = foundationPiles

d = Deck()
t = Table(d)
f = FoundationPiles()

pygame.display.quit()
pygame.quit()
sys.exit()
