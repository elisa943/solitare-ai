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

    def event_triggered(self, deck, table, foundationPiles):
        """
        Deals with different events : 
        - If the player clicks on the deck : draws cards from deck or if the deck is empty, it rinitialize it. 
        - If the player clicks on a card that can be moved to a foundation pile : it does that move. 
        """
        # Takes the position IF the mouse is pressed 
        mouse_position = self.is_mouse_pressed()
        
        # If the mouse is not pressed, return False (no event was triggered)
        if mouse_position == None:
            return False
            
        #  * Checks if the mouse pressed on the deck 
        deckPosition = deck.get_position_deck()
        
        # If the mouse clicked on the deck, draws up to 3 cards or re-initialized the deck
        if self.is_mouse_in_rectangle(deckPosition, mouse_position):
            deck.picks_3_cards()
            return True 

        # * Checks if the mouse clicked on the open deck 
        openDeckPostion = deck.get_position_deck(True)
        
        # If the mouse clicked on the open deck, places the card
        if self.is_mouse_in_rectangle(openDeckPostion, mouse_position):

            cardShown = None if len(deck.cardsShown) == 0 else (deck.cardsShown[-3], False)

            if cardShown != None:
                foundationPiles.places_card(cardShown, deck, table)
            else:
                return False

        # * Checks if the mouse clicked on a card on the table 
        for i in range(len(table.cardsOnTable)):
            
            # ! For now : only checks if the last card was clicked on 

            # Takes the position of the last card, including its size : (x, y, w, h)
            positionLastCard = table.get_position_last_card(i)

            # Check if the table's index is empty
            empty = len(table.cardsOnTable[i]) == 0

            # If the mouse clicked on the last card of a pile and the pile isn't empty, checks if the card can be moved
            if self.is_mouse_in_rectangle(positionLastCard, mouse_position) and not(empty):
                
                # Checks is the card can be moved in its foundation pile 

                # lastCard represents the last of the i-th pile
                lastCard = table.cardsOnTable[i][-1]

                # If the card can be added to its foundation pile
                if foundationPiles.can_be_moved_in_foundation(lastCard):

                    # The card is added to its foundation pile
                    foundationPiles.adds_to_piles(lastCard[0][1])

                    # And is deleted from its previous pile
                    table.deletes_card(lastCard, i)

                    # Reveals the last card if possible 
                    if len(table.cardsOnTable[i]) > 0:
                        newLastCard = (table.cardsOnTable[i][-1][0], False)
                        table.cardsOnTable[i].pop(-1)
                        table.cardsOnTable[i].append(newLastCard)


                # ! Checks if it can be moved to another pile in the table
                
                break
        
        
        return False

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

    def draws_window(self, screen, deck, table, foundationPiles):
        screen.fill(BACKGROUND_COLOR)
        deck.displays_closed_deck(screen)
        deck.displays_open_deck(screen)
        table.displays_table(screen)
        foundationPiles.displays_foundation_piles(screen)
        pygame.display.update()

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


def main():

    theDeck = Deck()
    theTable = Table(theDeck)
    theFoundationPiles = FoundationPiles()
    thePlayer = Player(theDeck, theTable, theFoundationPiles)
    screen = thePlayer.initialize_pygame()
    running = True

    

    while running:
        thePlayer.draws_window(screen, theDeck, theTable, theFoundationPiles)

        # Quit 
        for event in pygame.event.get():
            thePlayer.event_triggered(theDeck, theTable, theFoundationPiles)

            if event.type == pygame.QUIT:
                running = False
        
        # If the game is won, close the game. 
        if theFoundationPiles.game_won():
            running = False 


    
    thePlayer.close_pygame()


if __name__ == "__main__":
    main()
