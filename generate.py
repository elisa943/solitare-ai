import pygame
from enum import Enum
import random

# Variables
NUM_TABLE = 7
NUM_PILES = 4
NUM_RANKS = 14
NUM_SUITS = 4

WIDTH = 140
HEIGHT = 190

BACKGROUND_COLOR = (34, 139, 34) # Forest green 

imgClosedCard = pygame.image.load("images/Cards/cardBack_red2.png")

class ImplementationError(Exception):
    pass

class Rank(Enum):
    ACE = 1
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

def suit_string_conversion(suit):
    match suit.value:
        case 0:
            return "Clubs"
        case 1:
            return "Diamonds"
        case 2:
            return "Spades"
        case _:
            return "Hearts"

def img_card(card):
    (rank, suit) = card
    suit_string = suit_string_conversion(suit)
    rank_string = str(rank.value)
    return pygame.image.load("images/Cards/card" + suit_string + rank_string + ".png")

class Deck():
    def __init__(self):
        self.stockpile = []
        self.cardsShown = []
        self.CLOSED_DECK_POSITION = (10, 10)
        self.OPEN_DECK_POSITION = (200, 10)

        # Adds all possible cards
        for i in range(1, 14):
            for j in range(4):
                self.stockpile.append((Rank(i), Suit(j)))

        # Deck is shuffled at the very beginning 
        random.shuffle(self.stockpile)

    # Picks one card at the top of the deck
    def picks_card(self, withdraw=True):
        cardPicked = None

        if len(self.stockpile) > 0:
            cardPicked = self.stockpile.pop(-1)

            # If asked not to withdraw the card, puts it back in the deck 
            if not(withdraw):
                self.stockpile.append(card)

        return cardPicked
    
    def reinitialize_deck(self):
        # If the deck is empty, re-initialize it
        if len(self.stockpile) == 0:
            self.cardsShown.reverse()
            self.stockpile = self.cardsShown
            self.cardsShown = []

        # Else, does nothing

    def picks_3_cards(self):
        """
        Adds up to 3 cards to self.cardsShown
        """

        # If impossible to display new cards, re-initialize the deck
        if len(self.stockpile) == 0:
            self.reinitialize_deck()
        else:
            # Else, adds up to 3 cards the cardsShown list
            for _ in range(min(3, len(self.stockpile))):
                newCard = self.picks_card()
                self.cardsShown.append(newCard)

    def displays_closed_deck(self, screen):
        if len(self.stockpile) != 0:
            screen.blit(imgClosedCard, self.CLOSED_DECK_POSITION)

    def displays_open_deck(self, screen):
        """
        Displays 3 cards if possible
        """
        for i in range(min(3, len(self.cardsShown))):
            imgOpenDeck = img_card(self.cardsShown[-1-i])
            positionOfShownCards = (self.OPEN_DECK_POSITION[0] - 20*i, self.OPEN_DECK_POSITION[1])
            screen.blit(imgOpenDeck, positionOfShownCards)

    def get_position_deck(self, open=False):
        """
        Returns (x, y, width, height) of the deck
        """
        if not(open):
            return (self.CLOSED_DECK_POSITION[0], self.CLOSED_DECK_POSITION[1], WIDTH, HEIGHT)
        else:
            return (self.OPEN_DECK_POSITION[0] - 40, self.OPEN_DECK_POSITION[1], 40 + WIDTH, HEIGHT)

    def deletes_shown_card(self):
        """ 
        If possible, deletes the last shown card
        """
        # If some cards are shown
        if len(self.cardsShown) > 0:
            self.cardsShown.pop(max(-3, -len(self.cardsShown)))


class Table():
    def __init__(self, startingDeck):
        self.cardsOnTable = [[] for _ in range(NUM_TABLE)]
        self.STARTING_POSITION_TABLE = (10, 220)
        self.GAP_CARDS_X = 170
        self.GAP_CARDS_Y = 30

        # Each part of the table is a Queue containing tuples (card, hidden) with hidden being a boolean
        for i in range(NUM_TABLE):

            # Adds hidden card(s) 
            for j in range(i):
                self.cardsOnTable[i].append((startingDeck.picks_card(), True))

            # Adds the first card shown
            self.cardsOnTable[i].append((startingDeck.picks_card(), False))

    def table_content(self):
        for i in range(NUM_TABLE):
            for j in range(len(self.cardsOnTable[i])):
                print(self.cardsOnTable[i][j], end="")
            
            print("\n")

    def displays_table(self, screen):
        for i in range(len(self.cardsOnTable)):
            for j in range(len(self.cardsOnTable[i])):
                (card, hidden) = self.cardsOnTable[i][j]
                positionOfCard = (self.GAP_CARDS_X*i + self.STARTING_POSITION_TABLE[0], self.GAP_CARDS_Y*j + self.STARTING_POSITION_TABLE[1])
                
                # If the card is not hiddenn then it is shown on screen
                if not hidden:
                    screen.blit(img_card(card), positionOfCard)
                # Else, we show a closed card
                else:
                    screen.blit(imgClosedCard, positionOfCard)

    def cards_compatible(self, cardUp, cardDown):
        """
        Returns True if we can put cardDown under cardUp
        """
        # Checks if cardUp's rank is equal to cardDown's rank + 1 
        if cardUp[0].value != cardDown[0].value + 1:
            return False 
        
        # Checks if cardUp's suit is the same color as cardDown's
        if cardUp[1].value % 2 == cardDown[1].value % 2:
            return False

        return True

    def contains_card(self, index, card):
        """
        Checks if the index contains the card (not hidden) and returns its second index j.
        """
        for j in range(len(self.cardsOnTable)):
            if not(self.cardsOnTable[index][j][1]) and self.cardsOnTable[index][j][0] == card:
                return j 
        
        return None 

    def stack_of_cards(self, index, card):
        """
        Returns a sublist of self.cardsOnTable[index] with card being the first element. 
        """
        # If the table's index doesn't contain the card, raises an error
        j = self.contains_card(index, card)
        if j == None:
            raise ImplementationError
        
        num_cards = len(self.cardsOnTable[index])

        res = self.cardsOnTable[index][j:num_cards]

        return res

    def adds_stack_of_cards(self, index, stack):
        """
        Given a stack of cards, adds that stack in the table's index. 
        """
        for card in stack:
            self.cardsOnTable[index].append(card)

    def deletes_stack_of_card(self, index, stack):
        """
        Given a list 'stack' of cards, deletes each of them in self.cardsOnTable[index]. 
        """

        for i in range(len(stack)):
            card = stack[i]
            self.cardsOnTable[index].remove(card)

    def can_be_moved_in_table(self, move):
        """ 
        Returns True if the move can be made. 
        move is a tuple (source, destination, card) with : 
            - source : int, index of the table 
            - destination : int, index of the table 
            - card : (Rank, Suit), card
        """

        source = move[0]
        destination = move[1]
        card = move[2]

        # Checks if the source index contains the card
        if self.contains_card(source, card) == None:
            raise ImplementationError

        # Takes the last card of the destination 
        lastCardOfDestination = self.cardsOnTable[destination][-1]

        return self.cards_compatible(lastCardOfDestination[0], card)

    def can_be_moved_in_piles(self, foundationPiles):
        """
        Returns True if the move can be made. 
        'move' is a couple (source, card)
        """
        source = move[0]
        card = move[1]

        # Checks if the source index contains the card
        if self.contains_card(source, card) == None:
            raise ImplementationError
        
        rank = card[0]
        suit = card[1]

        return foundationPiles.cardsOnPiles[suit] == rank.value - 1

    def makes_move_in_table(self, move):
        """
        Makes a move whether or not it's a valid one. 
        
        'move' is a tuple (source, destination, card) with : 
            - source : int, index of the table 
            - destination : int, index of the table 
            - card : (Rank, Suit), card

        The move is relative to the table and not the foundation piles
        """

        source = move[0]
        destination = move[1]
        card = move[2]

        to_be_moved = self.stack_of_cards(source, card)
        # Adds the stack of cards to the destination 
        self.adds_stack_of_cards(destination, to_be_moved)

        # Deletes the stack of cards of the source 
        self.deletes_stack_of_card(source, to_be_moved)

        # Reveals the last card from source index if possible 
        if len(self.cardsOnTable[source]) > 0:
            self.cardsOnTable[source][-1] = (self.cardsOnTable[source][-1][0], False)

    def get_position_last_card(self, index):
        """
        Given a particular index of the table, 
        returns (x, y, w, h) of table's index's last card
        """
        # Represents the index of the last card in the table's index
        j = len(self.cardsOnTable[index]) - 1
        
        # If the table's index is not empty, returns the position of its last card
        if j > -1:
            positionOfCard = (self.GAP_CARDS_X*index + self.STARTING_POSITION_TABLE[0], self.GAP_CARDS_Y*j + self.STARTING_POSITION_TABLE[1])
            return (positionOfCard[0], positionOfCard[1], WIDTH, HEIGHT)
        
        # Else, the table is empty
        else:
            positionOfCard = (self.GAP_CARDS_X*index + self.STARTING_POSITION_TABLE[0], self.STARTING_POSITION_TABLE[1])
            return (positionOfCard[0], positionOfCard[1], WIDTH, HEIGHT)
    
    def deletes_card(self, card, index):
        if self.contains_card(index, card[0]) == None:
            raise ImplementationError
        else:
            self.cardsOnTable[index].remove(card)

    def card_in_position(self, position):
        """
        Given a position (x, y) of the mouse, 
        returns the index (i, j) representing the card 
        that the mouse clicked on. 

        If the mouse clicked on nothing, or a card that is hidden returns None

        Ecart entre cartes en abscisse : 170
        En ordonnée : 20
        """

        i = int((position[0] - self.STARTING_POSITION_TABLE[0]) / self.GAP_CARDS_X)
        j = int((position[1] - self.STARTING_POSITION_TABLE[1]) / self.GAP_CARDS_Y)

        if j < len(self.cardsOnTable[i]):
            return (i, j)

        return None

    def compatible_index(self, i, j):
        """
        Returns a list of all possible new positions of the card of index (i, j)
        """
        # List of all possible index it can be moved to
        compatibleIndexes = []
        
        # Checks if it can be moved to another pile in the table
        for index in range(len(self.cardsOnTable)):
            if i != index:
                card = self.cardsOnTable[i][j]
                if self.can_be_moved_in_table((i, index, card[0])):
                    compatibleIndexes.append(index)
        
        return compatibleIndexes


class FoundationPiles():
    def __init__(self):
        self.STARTING_POSITION_PILES = (520, 10)

        self.cardsOnPiles = {}
        for i in range(NUM_PILES):
            self.cardsOnPiles[Suit(i)] = 0
    
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

    def game_won(self) -> bool:
        """
        Returns True if the game is won
        """
        for i in range(NUM_PILES):
            
            if self.cardsOnPiles[Suit(i)] != Rank(13):
                return False

        return True 

    def can_be_moved_in_foundation(self, theCard):
        """
        Returns True of the card can be added on top of the pile foundation. 
        """
        
        rank = theCard[0][0]
        suit = theCard[0][1]
        hidden = theCard[1]
        
        # If card can be added on pile foundation, then it's added and returns True
        return self.cardsOnPiles[suit] == rank.value - 1 and not(hidden)

    def adds_to_piles(self, suit):
        """
        Adds a card to the suit's foundation pile. 
        """
        if self.cardsOnPiles[suit] < 13:
            self.cardsOnPiles[suit] += 1
        else:
            raise ImplementationError
    
    def places_card(self, theCard, deck, table, index=None):
        """
        Given a card, places the card in its foundation pile IF possible
        - If index is None, then the card is from the deck
        - Else, index represents the index of the card in the table
        """
        # If the card is from the deck 
        if index == None:
            
            # If theCard can be moved in its foundation pile
            if self.can_be_moved_in_foundation(theCard):
                
                # The card is added to its foundation pile
                self.adds_to_piles(theCard[0][1])

                # And is deleted from its previous pile 
                deck.deletes_shown_card()
        
        # Else, the card is from the table
        else:
            print("oh well...")

    def displays_foundation_piles(self, screen):
        """
        Displays the foundation piles
        """
        i = 0
        for pile in self.cardsOnPiles:
            if self.cardsOnPiles[pile] >= 1:
                card = (Rank(self.cardsOnPiles[pile]), Suit(i))
                positionOfPiles = (170*i + self.STARTING_POSITION_PILES[0], self.STARTING_POSITION_PILES[1])
                screen.blit(img_card(card), positionOfPiles)
            i += 1

