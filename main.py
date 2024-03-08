import time
from pygame import mixer
from generate import *
from ai import *

class Player():
    def __init__(self, deck, table, foundationPiles):
        self.deck = deck
        self.table = table
        self.foundationPiles = foundationPiles
        self.score = 0

    def last_card_clicked_on(self, mouse_position):
        """
        Checks if the last card was clicked on and returns the index of the last card the mouse clicked on.
        """
        # Loops through all piles
        for i in range(len(self.table.cardsOnTable)):

            # Takes the position of the last card including its size : (x, y, w, h)
            positionLastCard = self.table.get_position_last_card(i)

            # If the mouse clicked on the last card of a pile and the pile isn't empty, checks if the card can be moved
            if self.is_mouse_in_rectangle(positionLastCard, mouse_position) and not(len(self.table.cardsOnTable[i]) == 0):
                return i

        return None

    def event_triggered(self):
        """
        Deals with different events :
        - If the player clicks on the deck : draws cards from deck or if the deck is empty, it rinitialize it.
        - If the player clicks on a card that can be moved to a foundation pile : it makes that move.
        - If the player clicks on a foundation pile
        """
        # 1 - Verifies that the mouse clicked on something

        # Takes the position IF the mouse is pressed
        mouse_position = self.is_mouse_pressed()

        # If the mouse is not pressed, return False (no event was triggered)
        if mouse_position == None:
            return False

        # 2 - If the mouse clicked on the table
        if self.is_mouse_in_rectangle((self.table.STARTING_POSITION_TABLE[0], self.table.STARTING_POSITION_TABLE[1], WINDOW_WIDTH, WINDOW_HEIGHT), mouse_position):
            
            # 2.1 - Checks if the mouse clicked on the last card of a pile
            index = self.last_card_clicked_on(mouse_position)
            if index != None:
                if self.foundationPiles.moved_to_foundation(index, self.table, self.deck):
                    self.score += 15
                    return True
                else: 
                    return False

            # 2.2 - Checks if the mouse clicked on an upper card. Detects which card was clicked on and takes its index in the table
            (gain, move_made) = self.table.upper_card(mouse_position, self.deck)
            self.score += gain 
            return move_made

        # 3 - Else, the mouse clicked on the top of the window
        else:

            #  3.1 - Checks if the mouse pressed on the deck
            deckPosition = self.deck.get_position_deck()

            # 3.1.1 - If the mouse clicked on the (closed) deck, draws up to 3 cards or re-initialized the deck
            if self.is_mouse_in_rectangle(deckPosition, mouse_position):
                self.deck.picks_3_cards()
                return True

            # 3.1.2 - Checks if the mouse clicked on the open deck
            openDeckPostion = self.deck.get_position_deck(True)

            # If the mouse clicked on the open deck, places the card if possible
            if self.is_mouse_in_rectangle(openDeckPostion, mouse_position):

                cardShown = None if len(self.deck.cardsShown) == 0 else (self.deck.cardsShown[max(NUM_CARDS_SHOWN, -len(self.deck.cardsShown))] , False)

                # If the deck is not empty, places the card on the foundation piles IF possible
                if cardShown != None:
                    if self.foundationPiles.places_card(cardShown, self.deck, self.table):
                        self.score += 15
                        return True

                    else:
                        (gain, move_made) = self.table.move_to_pile(-1, self.deck, fromDeck=True)
                        self.score += gain

                        # If a move isn't made, checks if the stockpile is empty. 
                        if not(move_made) and len(self.deck.stockpile) == 0:
                            self.deck.reinitialize_deck()
                            return True

                        return move_made

                # Else, does nothing
                else:
                    return False

            # 3.2 Checks if the mouse clicked on the foundation piles

            # Searches the Suit of the foundation pile picked
            suitFoundation = None
            for i in range(NUM_PILES):
                # If the mouse clicked on a certain foundation pile, suitFoundation takes the index
                if self.is_mouse_in_rectangle(self.foundationPiles.get_position_foundation(i), mouse_position):
                    suitFoundation = Suit(i)
                    break

            # If the mouse clicked on a foundation pile and it's not empty
            if suitFoundation != None:
                rankFoundation = Rank(self.foundationPiles.cardsOnPiles[suitFoundation])

                if rankFoundation.value > 0:

                    # Checks if the card can be moved
                    for i in range(NUM_TABLE):
                        move = (-1, i, (rankFoundation, suitFoundation))
                        if self.table.can_be_moved_in_table(move, self.deck, fromFoundation=True):
                            # Makes the move
                            self.score += self.table.makes_move_in_table(move, self.deck, fromFoundation=True)

                            # Deletes the last card from foundation pile
                            self.foundationPiles.cardsOnPiles[suitFoundation] -= 1
                            break


        return False

    """ ---------- PREDICATES ----------"""
    def is_mouse_pressed(self):
        """
        Returns the mouse's position if it's pressed
        """
        if pygame.mouse.get_pressed()[0]:
            return pygame.mouse.get_pos()

        return None

    def is_mouse_in_rectangle(self, rectangle, mouse):
        """
        Returns True if the mouse's position is inside a rectangle (x, y, width, height).
        """
        return rectangle[0] <= mouse[0] <= rectangle[0] + rectangle[2] and rectangle[1] <= mouse[1] <= rectangle[1] + rectangle[3]

    def game_won(self):
        """
        Returns True if the game is won, ie :
            - If the foundation pile is full
            OR
            - If the deck is empty and no cards are hidden
        """

        if self.foundationPiles.piles_full() or (self.deck.deck_empty() and self.table.no_hidden_cards()):
            self.score += 200 
            return True 
        else: return False

    """ ---------- DISPLAYING ----------"""

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

    def draws_window(self, screen):
        screen.fill(BACKGROUND_COLOR)
        self.deck.displays_closed_deck(screen)
        self.deck.displays_open_deck(screen)
        self.table.displays_table(screen)
        self.foundationPiles.displays_foundation_piles(screen)
        self.displays_score(screen)
        pygame.display.update()

    def displays_end_game(self, screen):
        # Displays the background
        screen.fill(BACKGROUND_COLOR)
        self.displays_score(screen)

    def displays_score(self, screen):

        # Font
        myFont_game = pygame.font.SysFont('Arial', 30)

        # Displays the score
        text_score = "SCORE :"
        label_name_score = myFont_game.render(text_score, 1, BLACK)

        text_score = str(self.score)
        label_score = myFont_game.render(text_score, 1, BLACK)

        screen.blit(label_name_score, (20, WINDOW_HEIGHT - 200)) # "SCORE :"
        screen.blit(label_score, (150, WINDOW_HEIGHT - 200))    # [score]

    def close_pygame(self):
        """
        Closes everything.
        """
        pygame.display.quit()
        pygame.quit()
        sys.exit()


def main():
    theDeck = Deck()
    theTable = Table(theDeck)
    theFoundationPiles = FoundationPiles()
    thePlayer = Player(theDeck, theTable, theFoundationPiles)
    screen = thePlayer.initialize_pygame()
    running = True

    while running:
        thePlayer.draws_window(screen)

        # Quit
        for event in pygame.event.get():
            thePlayer.event_triggered()

            if event.type == pygame.QUIT:
                running = False

        # If the game is won, close the game.
        if thePlayer.game_won():
            print(thePlayer.score)
            running = False

    thePlayer.close_pygame()


if __name__ == "__main__":
    main()
