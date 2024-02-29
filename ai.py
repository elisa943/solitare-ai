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