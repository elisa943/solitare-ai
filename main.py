# https://opengameart.org/content/boardgame-pack
import sys
import time 
from pygame import mixer
from generate import * 

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1000

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

    def last_card_clicked_on(self, mouse_position, foundationPiles, table):
        """
        Checks if the last card was clicked on and returns the index of the last card the mouse clicked on. 
        """
        # Loops through all piles 
        for i in range(len(table.cardsOnTable)):

            # Takes the position of the last card including its size : (x, y, w, h)
            positionLastCard = table.get_position_last_card(i)

            # If the mouse clicked on the last card of a pile and the pile isn't empty, checks if the card can be moved
            if self.is_mouse_in_rectangle(positionLastCard, mouse_position) and not(len(table.cardsOnTable[i]) == 0):
                return i 
        
        return None 

    def event_triggered(self, deck, table, foundationPiles):
        """
        Deals with different events : 
        - If the player clicks on the deck : draws cards from deck or if the deck is empty, it rinitialize it. 
        - If the player clicks on a card that can be moved to a foundation pile : it does that move. 
        """
        # 1 - Verifies that the mouse clicked on something 

        # Takes the position IF the mouse is pressed 
        mouse_position = self.is_mouse_pressed()
        
        # If the mouse is not pressed, return False (no event was triggered)
        if mouse_position == None:
            return False

        # 2 - If the mouse clicked on the table 
        if self.is_mouse_in_rectangle((table.STARTING_POSITION_TABLE[0], table.STARTING_POSITION_TABLE[1], WINDOW_WIDTH, WINDOW_HEIGHT), mouse_position):

            # 2.1 - Checks if the mouse clicked on the last card of a pile 
            index = self.last_card_clicked_on(mouse_position, foundationPiles, table)

            if index != None:

                # 2.1.1 - Checks if it can be moved to its foundation pile

                # lastCard represents the last of the index-th pile
                lastCard = table.cardsOnTable[index][-1]

                # If the card can be added to its foundation pile
                if foundationPiles.can_be_moved_in_foundation(lastCard):

                    # The card is added to its foundation pile
                    foundationPiles.adds_to_piles(lastCard[0][1])

                    # And is deleted from its previous pile
                    table.deletes_card(lastCard, index)

                    # Reveals the last card if possible 
                    if len(table.cardsOnTable[index]) > 0:
                        newLastCard = (table.cardsOnTable[index][-1][0], False)
                        table.cardsOnTable[index].pop(-1)
                        table.cardsOnTable[index].append(newLastCard)
                    
                    return True 

                # 2.1.2 - Checks if it can be moved to another pile 

                # List of all possible index it can be moved to
                compatibleIndexes = table.compatible_index(index, -1)

                # If there are no compatibles indexes, does nothing : the card can't be moved
                if len(compatibleIndexes) == 0:
                    return False 
                
                # Else, there is at least one possibility : takes the first possibility and makes the move
                else:
                    card = table.cardsOnTable[index][-1] # card + hidden
                    table.makes_move_in_table((index, compatibleIndexes[0], card[0]))

            # 2.2 - If it's not the last card, detects which card was clicked on and takes its index in the table
            cardChosen = table.card_in_position(mouse_position)

            # If the player didn't click on a card then do nothing 
            if cardChosen == None:
                return False 
            
            # If the card chosen is hidden then do nothing
            elif table.cardsOnTable[cardChosen[0]][cardChosen[1]][1]:
                return False 
            
            # Else, the player clicked on a card shown (we know it's not a last card)
            else:

                # List of all possible index it can be moved to
                compatibleIndexes = table.compatible_index(cardChosen[0], cardChosen[1])
                
                # If there are no compatibles indexes, does nothing : the card can't be moved
                if len(compatibleIndexes) == 0:
                    return False 
                
                # Else, there is at least one possibility 
                else:
                    card = table.cardsOnTable[cardChosen[0]][cardChosen[1]]
                    table.makes_move_in_table((cardChosen[0], compatibleIndexes[0], card[0]))

        # 3 - Else, the mouse clicked on the top of the window 
        else:

            #  * Checks if the mouse pressed on the deck 
            deckPosition = deck.get_position_deck()
            
            # If the mouse clicked on the (closed) deck, draws up to 3 cards or re-initialized the deck
            if self.is_mouse_in_rectangle(deckPosition, mouse_position):
                deck.picks_3_cards()
                return True 

            # * Checks if the mouse clicked on the open deck 
            openDeckPostion = deck.get_position_deck(True)
            
            # If the mouse clicked on the open deck, places the card if possible
            if self.is_mouse_in_rectangle(openDeckPostion, mouse_position):

                cardShown = None if len(deck.cardsShown) == 0 else (deck.cardsShown[-3], False)

                # If the deck is not empty, places the card IF possible
                if cardShown != None:
                    foundationPiles.places_card(cardShown, deck, table)
                    return True
                
                # Else, does nothing 
                else:
                    return False

            # * Checks if the mosue clicked on the foundation piles



        return False

    def initialize_pygame(self):
        # Initialization
        pygame.init()
        pygame.font.init()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
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
