from generate import *
from player import *

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
        self.source = source # (i, j)
        self.destination = destination 

class PILES_TO_TABLE():
    def __init__(self, suit, tableIndex):
        self.tableIndex = tableIndex
        self.suit = suit 

class PlayerAI(Player):
    def __init__(self, deck, table, foundationPiles):
        self.deck = deck
        self.table = table
        self.foundationPiles = foundationPiles
        #self.player = player
        # super().__init__(deck, table, foundationPiles)
        self.score = 0
        self.history = []

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

        cardFromDeck = self.deck.cardShown()
        if cardFromDeck != None: 
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
                if i != j:
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

        # From Table 
        fromTable = self.possible_actions_from_table()
        for m in fromTable: possibleActions.append(m)


        # From Foundation Piles 
        fromFoundation = self.possible_actions_from_foundation()
        for m in fromFoundation: possibleActions.append(m)

        # From Deck  
        fromDeck = self.possible_actions_from_deck()
        for m in fromDeck: possibleActions.append(m)

        # Draw cards 
        possibleActions.append(DRAW_CARDS())

        return possibleActions

    def displays_possible_actions_in_terminal(self):
        """
        Displays all possible actions in English
        """
        possible_actions = self.possible_actions()
        print(chr(27) + "[2J")
        print("All possible actions are : ")
        print(possible_actions)
        for action in possible_actions:
            match action:
                case DRAW_CARDS():
                    print("- Draw cards.")
                case DECK_TO_TABLE():
                    card = self.deck.cardShown()
                    print("- Move card", card,"from deck to the", action.tableIndex + 1,"th table.")
                case DECK_TO_PILES():
                    card = self.deck.cardShown()
                    print("- Move card ", card,"from deck to its foundation pile.")
                case TABLE_TO_PILES():
                    print("- Move card from the", action.tableIndex + 1, "th table to its foundation pile.")
                case TABLE_TO_TABLE():
                    print("- Move card from the", action.source[0] + 1, "ith table to the", action.source[1] + 1, "th table.")
                case PILES_TO_TABLE():
                    print("- Move card from the", action.suit, "foundation pile to the", action.tableIndex + 1, "th table.")
                case _: 
                    raise ImplementationError

    def get_position_button():
        """
        TODO : Returns the position of the "auto move" button
        """
        return None

    def result(self, action):
        """
        result() applies an action to a board. The action is supposed to be legal. 
        """
        copy = copy.deepcopy(self)
        
        match type(action):
            case DRAW_CARDS():
                copy.deck.picks_3_cards()
            case DECK_TO_TABLE():
                copy.table.makes_move_in_table((-1, action.suit, copy.deck.cardShown()), copy.deck, fromDeck=True)
            case DECK_TO_PILES():
                copy.foundationPiles.places_card(copy.deck.cardShown(), copy.deck, copy.table)
            case TABLE_TO_PILES():
                copy.foundationPiles.places_card()
            case TABLE_TO_TABLE():
                copy.table.makes_move_in_table((action.source[0], action.destination, copy.table.cardsOnTable[action.source[1]][action.source[1]]), copy.deck)
            case PILES_TO_TABLE():
                copy.table.makes_move_in_table((action.tableIndex, -1, (copy.table.cardsOnTable[action.tableIndex][-1], action.suit)), copy.deck, fromFoundation=True)
            case _: 
                raise ImplementationError
        
        return copy 

    def terminal(self) -> bool:
        """
        TODO : Returns True if a game is stuck <=> impossible to win
        """
        possibleActions = self.possible_actions()

        for action in possibleActions:
            if type(action) != DRAW_CARDS():
                return False

        return True
    """
    def state_value(self):
        return self.player.score

    MiniMax Algorithm : Impossible because only player -> MaxMax lols
    def minimax(self, depth):
        # Returns an optimal action. 
        if self.terminal() or self.player.game_won():
            return self.state_value()
    """