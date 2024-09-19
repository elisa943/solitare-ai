import time
from pygame import mixer
from ai import *
from game import *

def main():
    
    theDeck = Deck()
    theTable = Table(theDeck)
    theFoundationPiles = FoundationPiles()
    #thePlayer = Player(theDeck, theTable, theFoundationPiles)
    theAIPlayer = PlayerAI(theDeck, theTable, theFoundationPiles)

    theGame = Game(theDeck, theTable, theFoundationPiles, 0)

    screen = theAIPlayer.initialize_pygame()
    running = True

    # Plays music
    pygame.mixer.init
    mixer.music.load("music/calm_music.mp3")
    mixer.music.play(-1)

    while running:
        theAIPlayer.draws_window(screen)

        # Quit
        for event in pygame.event.get():
            if theAIPlayer.event_triggered(): 
                #theAIPlayer.displays_possible_actions_in_terminal()
                print("Move made")
            if event.type == pygame.QUIT:
                print(theAIPlayer.score)
                running = False

        # If the game is won, close the game.
        if theAIPlayer.game_won():
            print(theAIPlayer.score)
            running = False

    theAIPlayer.close_pygame()


if __name__ == "__main__":
    main()
