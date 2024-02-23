# https://opengameart.org/content/boardgame-pack
import sys
import time 
from pygame import mixer

from generate import * 

def initialize_pygame():
    # Initialization
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1200, 1000))
    
    # Title and Icon
    pygame.display.set_caption("Solitaire AI")
    icon = pygame.image.load("images/icon.jpeg")
    pygame.display.set_icon(icon)

    return screen

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

def draws_window(screen, deck, table, foundationPiles):
    screen.fill(BACKGROUND_COLOR)
    deck.displays_closed_deck(screen)
    deck.displays_open_deck(screen)
    table.displays_table(screen)
    foundationPiles.displays_foundation_piles(screen)
    pygame.display.update()


def main():
    screen = initialize_pygame()
    theDeck = Deck()
    theTable = Table(theDeck)
    theFoundationPiles = FoundationPiles()
    thePlayer = Player(theDeck, theTable, theFoundationPiles)
    
    draws_window(screen, theDeck, theTable, theFoundationPiles)

    running = True

    while running:

        # Quit 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # If the game is won, close the game. 
        if theFoundationPiles.game_won():
            running = False 
    
    close_pygame()


if __name__ == "__main__":
    main()
