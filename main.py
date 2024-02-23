# https://opengameart.org/content/boardgame-pack
import sys
import time 
from pygame import mixer
from generate import * 

class Player():
    def __init__(self, deck, table, foundationPiles):
        self.deck = deck
        self.table = table
        self.foundationPiles = foundationPiles

    def is_mouse_pressed(self):
        if pygame.mouse.get_pressed()[0]:
            return pygame.mouse.get_pos()
        
        return None

    def is_mouse_in_rectangle(self, rectangle, mouse):
        """
        Returns True if the mouse's position is inside a rectangle (x, y, width, height). 
        """
        return rectangle[0] <= mouse[0] <= rectangle[0] + rectangle[2] and rectangle[1] <= mouse[1] <= rectangle[1] + rectangle[3]

    def event_triggered(self, deck, table):
        """
        Draws cards from deck if even was triggered. 
        If the deck is empty, it rinitialize it. 
        """
        mouse_position = self.is_mouse_pressed()
        
        if mouse_position == None:
            return False
        else:
            
            # Checks if the mouse pressed on the deck 
            deckPosition = deck.get_position_deck()
            
            # If the mouse clicked on the deck, draws up to 3 cards or re-initialized the deck
            if self.is_mouse_in_rectangle(deckPosition, mouse_position):
                deck.picks_3_cards()

            # If the mouse clicked on a card
            for i in range(len(table.cardsOnTable)):
                
                # Represents the position of the last card, including its size. 
                positionLastCard = table.get_position_last_card(i)

                # If the mouse clicked on a the last card of 
                if self.is_mouse_in_rectangle(positionLastCard, mouse_position):
                    print("hello")
                

    def initialize_pygame(self):
        # Initialization
        pygame.init()
        pygame.font.init()
        screen = pygame.display.set_mode((1200, 1000))
        
        # Title and Icon
        pygame.display.set_caption("Solitaire AI")
        icon = pygame.image.load("images/icon.jpeg")
        pygame.display.set_icon(icon)

        return screen

    def close_pygame(self):
        pygame.display.quit()
        pygame.quit()
        sys.exit()


class PlayerAI():
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


def draws_window(screen, deck, table, foundationPiles):
    screen.fill(BACKGROUND_COLOR)
    deck.displays_closed_deck(screen)
    deck.displays_open_deck(screen)
    table.displays_table(screen)
    foundationPiles.displays_foundation_piles(screen)
    pygame.display.update()


def main():

    theDeck = Deck()
    theTable = Table(theDeck)
    theFoundationPiles = FoundationPiles()
    thePlayer = Player(theDeck, theTable, theFoundationPiles)
    screen = thePlayer.initialize_pygame()
    running = True

    draws_window(screen, theDeck, theTable, theFoundationPiles)

    theDeck.displays_open_deck(screen)

    while running:

        # Quit 
        for event in pygame.event.get():
            thePlayer.event_triggered(theDeck, theTable)

            if event.type == pygame.QUIT:
                running = False
        
        # If the game is won, close the game. 
        if theFoundationPiles.game_won():
            running = False 

        draws_window(screen, theDeck, theTable, theFoundationPiles)
    
    thePlayer.close_pygame()


if __name__ == "__main__":
    main()
