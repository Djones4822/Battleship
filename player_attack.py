from ships import AbstractShip, Submarine, PatrolShip, AircraftCarrier
from board import Board
from random import choice
from string import ascii_uppercase as ASCII_UPPERCASE

SHIP_NAMES = {  Submarine.NAME : Submarine,
                AircraftCarrier.NAME : AircraftCarrier,
                PatrolShip.NAME : PatrolShip
                }
                
def player_attack():
    '''Main game loop for player_attack mode'''
    board = Board()
    board.comp_attack = False
    player_shots = 20
    #set computer positions
    for Ship in SHIP_NAMES.values():
        while True:
            placement = choice(Board.ALL_POSITIONS)
            hor_or_vert = choice(['1','2'])
            pos, value = board.get_positions_for_ship(placement, hor_or_vert, Ship.SIZE)
            if value == 0:
                board.ships.append(Ship(pos))
                break
    print 'Computer is Ready!\nYou have 20 Shots to win...\n\nGood Luck!'
    
    while any(ship.sunk == False for ship in board.ships) and player_shots:
        print board
        print 'Where would you like to attack?\n'
        user_attack = raw_input('-> ').upper()
        if user_attack in Board.ALL_POSITIONS and user_attack not in board.shot_positions:
            shot_return, shot_return_ship = board.shoot(user_attack)
            if shot_return:
                print 'Hit!'
                shot_return_ship.hit_positions.append(user_attack)
                sunk_check_value, sunk_check_ship = board.is_ship_sunk()
                if sunk_check_value:
                    print 'You\'ve sunk the {}!'.format(sunk_check_ship.NAME)
            else:
                print 'Miss!'
        else:
            print 'You\'ve either entered and invalid position or you\'ve \
already shot there!'
    if not player_shots:
        'You lose. Sorry! Better luck next time!'
    else:
        print 'You win!! You sunk all of the ships!'
    return None
        
    
