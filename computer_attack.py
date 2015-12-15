from ships import AbstractShip, Submarine, PatrolShip, AircraftCarrier
from board import Board
from random import choice
from string import ascii_uppercase as ASCII_UPPERCASE

SHIP_NAMES = {  Submarine.NAME : Submarine,
                AircraftCarrier.NAME : AircraftCarrier,
                PatrolShip.NAME : PatrolShip
                }

BAD_PLACEMENT_MESSAGE = '''
Your ship is too big for those spaces. Remember that\
if you want a vertical ship, then the position you give is \
the top position. If you wankt a horizontal ship then the \
position is the left most.'''
                
def computer_attack():
    '''Main game loop of computer_attack mode using Ships classes and Board class''
    board = Board()
    board.comp_attack = True
    
    #DEBUGGING
    #board.shot_positions.append('D3')
    #board.shot_positions.append('C3')
    #board.last_miss = False
    #END DEBUGGING
    
    print 'Would you like to play a smart or a dumb computer?\nEnter 1 for Smart or 2 for Dumb\n'
    while True:
        smart_or_dumb = raw_input('-> ')
        if smart_or_dumb == '1' or smart_or_dumb == '2':
            board.smart_attack_on = not bool(int(smart_or_dumb)-1)
            break
        else:
            print 'Enter 1 or 2 please.'
    
    print 'How many tries do you want to give the computer? Enter any number'
    response = None
    while True:
        try:
            response = int(raw_input('-> '))
            break
        except ValueError:
            pass
    comp_tries = response
    
    
    #settup loop for each ship
    #DEBUGGING
    print 'ships: {}'.format(SHIP_NAMES.keys())
    #END DEBUGGING
    for ship_name in SHIP_NAMES.keys():
        print board
        acceptable_answer = False
        while not acceptable_answer:
            print 'Where would you like to place {}\n'.format(ship_name)
            user_position = raw_input('-> ').upper()
            print 'What direction would like it to face?\nEnter 1 for vertical or 2 for horizontal.'
            user_direction = raw_input('-> ')
            if user_position in board.ALL_POSITIONS and user_direction == '1' \
                                                    or user_direction == '2':
                return_positions, return_value = \
                                                board.get_positions_for_ship(
                                                    user_position, 
                                                    user_direction, 
                                                    SHIP_NAMES[ship_name].SIZE)
                if return_value == 0:
                    if board.ships:
                        for ship in board.ships:
                            if any((position in ship.positions) for position in return_positions):
                                print 'Your ships are overlapping!'
                        else:
                            board.ships.append(SHIP_NAMES[ship_name](return_positions))
                            acceptable_answer = True
                    else:
                        board.ships.append(SHIP_NAMES[ship_name](return_positions))
                        acceptable_answer = True
                        
                elif return_value == 1:
                    print BAD_PLACEMENT_MESSAGE
            else:
                    print 'You entered an invalid starting position.'

    #DEBUGGING
    #for ship in board.ships:
    #    if ship.NAME == 'Aircraft Carrier':
    #        ship.hit_positions.append('D3')
    #        ship.hit_positions.append('C3')
    #END DEBUGGING
    
    #main play - computer sends consecutive attacks and player is asked if hit      
    while comp_tries:
        print board
        shot = board.smart_attack()
        shot_return, shot_return_ship = board.shoot(shot)
        print 'Computer shoots {}!'.format(shot)
        #ask user about hit
        while True:
            print 'Was it a hit?\nYes or No?'
            response = raw_input('-> ')
            if response.lower() == 'yes':
                if shot_return:
                    shot_return_ship.hit_positions.append(shot)
                    sunk_check_value, sunk_check_ship = board.is_ship_sunk()
                    if sunk_check_value == 1:
                        print 'Right! The computer sunk your {}!'.format(sunk_check_ship.NAME)
                        board.last_miss = True
                        break
                    else:
                        print 'Right! The computer hit your {}!'.format(shot_return_ship.NAME)
                        board.last_miss = False
                        break
                else:
                    print 'Are you sure?\n'
            if response.lower() == 'no':
                if not shot_return:
                    print 'Right! Computer missed!'
                    board.last_miss = True
                    break
                else:
                    print 'Are you sure?\n'
                    
        #End turn, check gameover status
        if all(ship.sunk == True for ship in board.ships):
            print board
            print 'Game Over! Lets be honest though, it was inevitable. You suck.'
            break
        
        #DEBUGGING
        for ship in board.ships:
            print 'DEBUGGING:', ship.NAME, ship.positions, ship.hit_positions, ship.sunk
        comp_tries -= 1
        
        if not comp_tries:
            print 'You win!'
            if board.smart_attack_on and response >= 20:
                print 'You\'re smarter than our best computer! Good job! You should probably work for the government or something, I donno. What am I, a scientist?\n'
    return None
