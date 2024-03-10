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

class TABLE_TO_TABLE():
    def __init__(self, source, destination):
        self.source = source 
        self.destination = destination 

class PILES_TO_TABLE():
    def __init__(self, suit, tableIndex):
        self.tableIndex = tableIndex
        self.suit = suit 

class PlayerAI():
    def __init__(self, deck, table, foundationPiles):
        self.deck = deck
        self.table = table
        self.foundationPiles = foundationPiles

    def possible_actions_from_foundation(self):
        """
        Returns a list of all possible actions from foundation piles 
        """
        possibleActions = []

        for suit, value in self.foundationPiles.cardsOnPiles.items():
            if value > 0:
                cardOnPile = (Rank(value), suit)
                for i in range(len(self.table.cardsOnTable)):
                    if self.table.can_be_moved_in_table((-1, i, cardOnPile), self.deck, fromFoundation=True):
                        possibleActions.append(PILES_TO_TABLE(suit, i))

        return possibleActions

    def possible_actions_from_deck(self):
        """
        Returns all possible actions from deck
        """
        possibleActions = []

        cardFromDeck = self.deck.picks_card(withdraw=False)
        rank = cardFromDeck[0].value 
        suit = cardFromDeck[1]

        # - From deck to foundation piles 
        if self.foundationPiles.can_be_moved_in_foundation((cardFromDeck, False)):
            possibleActions.append(DECK_TO_PILES(suit))

        # - From deck to table 
        for i in range(len(self.table.cardsOnTable)):
            if len(self.table.cardsOnTable[i]) != 0:
                # Takes the last card from the i-th pile 
                lastCard = self.table.cardsOnTable[i][-1][0]

                # Checks if they're compatible 
                if self.table.cards_compatible(lastCard, cardFromDeck):
                    possibleActions.append(DECK_TO_TABLE(i))

        return possibleActions

    def possible_actions_from_table(self):
        """
        Returns list of all possible actions from table
        """
        possibleActions = []

        # From table to table
        for i in range(len(self.table.cardsOnTable)):
            for j in range(len(self.table.cardsOnTable[i])):
                for index in self.table.compatible_index((i, j), self.deck):
                    possibleActions.append(TABLE_TO_TABLE((i, j), index))

        # From table to foundation piles 
        for i in range(len(self.table.cardsOnTable)):
            if len(self.table.cardsOnTable[i]) > 0:
                lastCard = self.table.cardsOnTable[i][-1]
                if self.foundationPiles.can_be_moved_in_foundation(lastCard):
                    possibleActions.append(TABLE_TO_PILES(i, lastCard[0][1]))
                
        return possibleActions


    def possible_actions(self):
        """
        Returns list of all possible actions. 
        """
        possibleActions = []

        # ! From Table 
        #fromTable = self.possible_actions_from_table()
        #for m in fromTable: possibleActions.append(m)


        # From Foundation Piles 
        fromFoundation = self.possible_actions_from_foundation()
        for m in fromFoundation: possibleActions.append(m)

        # From Deck  
        fromDeck = self.possible_actions_from_deck()
        for m in fromDeck: possibleActions.append(m)

        # Draw cards 
        possibleActions.append(DRAW_CARDS())

        return possibleActions