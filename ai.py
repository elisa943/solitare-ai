from generate import *

class DRAW_CARDS():
    pass 

class DECK_TO_TABLE():
    def __init__(self, tableIndex):
        self.tableIndex = tableIndex

class DECK_TO_PILES():
    def __init__(self, suit):
        self.suit = suit 

class TABLE_TO_PILES():
    def __init__(self, tableIndex, suit):
        self.tableIndex = tableIndex
        self.suit = suit 

class PILES_TO_TABLE():
    def __init__(self, suit, tableIndex):
        self.tableIndex = tableIndex
        self.suit = suit 

class PlayerAI():
    def __init__(self, deck, table, foundationPiles):
        self.deck = deck
        self.table = table
        self.foundationPiles = foundationPiles

    def possible_actions(self):
        """
        Returns list of all possibles actions. 

        An action can either have class DRAW_CARD

        """
        possibleActions = []

        # 1) Checks if cards in the table can be moved 
            # Checks if cards can be moved inside the table or onto the foundation pile

        # 2) Takes card from deck 
        cardFromDeck = self.deck.picks_card(withdraw=False)
        rank = cardFromDeck[0].value 
        suit = cardFromDeck[1]

        # Checks if it can be moved to its foundation pile  
        if self.foundationPiles.cardsOnPiles[suit] == rank - 1:
            possibleActions.append(DECK_TO_PILES(suit))

        # Checks if it can be moved to the table 
        for i in range(len(self.table.cardsOnTable)):
            if len(self.table.cardsOnTable[i]) != 0:
                # Takes the last card from the i-th pile 
                lastCard = self.table.cardsOnTable[i][-1][0]

                # Checks if they're compatible 
                if self.table.cards_compatible(lastCard, cardFromDeck):
                    possibleActions.append(DECK_TO_TABLE(i))


        # Draw cards 
        possibleActions.append(DRAW_CARDS())

        return possibleActions