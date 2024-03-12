import time
from pygame import mixer
from ai import *

def main():

    theDeck = Deck()
    theTable = Table(theDeck)
    theFoundationPiles = FoundationPiles()
    thePlayer = Player(theDeck, theTable, theFoundationPiles)
    theAIPlayer = PlayerAI(theDeck, theTable, theFoundationPiles)
    screen = thePlayer.initialize_pygame()
    running = True

    print(theAIPlayer.possible_actions())

    # Plays music
    pygame.mixer.init
    mixer.music.load("music/calm_music.mp3")
    mixer.music.play(-1)

    while running:
        thePlayer.draws_window(screen)

        # Quit
        for event in pygame.event.get():
            if thePlayer.event_triggered(): print(theAIPlayer.possible_actions())
            if event.type == pygame.QUIT:
                print(thePlayer.score)
                running = False

        # If the game is won, close the game.
        if thePlayer.game_won():
            print(thePlayer.score)
            running = False

    thePlayer.close_pygame()


if __name__ == "__main__":
    main()
