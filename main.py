import pygame
import sys
import random
from time import sleep
from pygame import mixer
from enum import Enum
from generate import * 

def initialize_pygame():
    # Initialization
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((800, 800))

    # Title and Icon
    pygame.display.set_caption("Solitaire AI")
    icon = pygame.image.load("images/icon.jpeg")
    pygame.display.set_icon(icon)

def close_pygame():
    pygame.display.quit()
    pygame.quit()
    sys.exit()




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

def main():
    initialize_pygame()

    theDeck = Deck()
    theTable = Table(d)
    theFoundationPiles = FoundationPiles()
    thePlayer = Player(theDeck, theTable, theFoundationPiles)

    close_pygame()


if __name__ == "__main__":
    main()
