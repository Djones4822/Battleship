from ships import AbstractShip, Submarine, PatrolShip, AircraftCarrier
from board import Board
from random import choice
from string import ascii_uppercase as ASCII_UPPERCASE
from computer_attack import computer_attack
from player_attack import player_attack

SHIP_NAMES = {  Submarine.NAME : Submarine,
                AircraftCarrier.NAME : AircraftCarrier,
                PatrolShip.NAME : PatrolShip
                }
def main():
    print 'Welcome to Battleship!\n\nEnter 1 to defend against the computer, or \
enter 2 to attack the computer!\n\n'
    while True:
        gamemode = raw_input('-> ')
        if gamemode == '1':
            computer_attack()
            break
        elif gamemode == '2':
            player_attack()
            break
        else:
            print 'You suck! Enter 1 or 2!'
    
    print '\n\nPlay again? (Yes or No)\n'
    response = raw_input('-> ')
    if response.lower() == 'yes':
        main()
    
    print 'Thanks for playing!'
    
