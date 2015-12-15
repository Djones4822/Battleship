from string import ascii_uppercase as ASCII_UPPERCASE
from random import choice


class AbstractShip(object):
    """Parent class of all ships."""
    def __init__(self, positions):
        self.sunk = False
        self.positions = positions
        self.hit_positions = []


class Submarine(AbstractShip):
    SIZE = 3
    NAME = 'Submarine'
    """Child class of ship with 3 placement positions"""


class AircraftCarrier(AbstractShip):
    SIZE = 5
    NAME = 'Aircraft Carrier'
    """Child class of ship with 5 placement positions"""


class PatrolShip(AbstractShip):
    SIZE = 2
    NAME = 'Patrol Ship'
    """Child class of ship with 2 placement positions"""


class Board(object):

    COLS_MAP = {ASCII_UPPERCASE[i] : i for i in range(10)}
    COL_LABEL = '     ' + '   '.join(sorted(COLS_MAP.keys()))
    ALL_POSITIONS = [let + str(i) for let in COLS_MAP.keys() for i in range(1,11)]
    
    def __init__(self):
        self.ships = []
        self.shot_positions = []
        self.comp_attack = None
        
    def __str__(self):
        board_list = [['.']*10 for i in range(10)]
        
        if self.comp_attack:
            for ship in self.ships:
                for pos in ship.positions:
                    index = self.board_position_conversion(pos)
                    char = 'S'
                    board_list[index[0]][index[1]] = char
                    
        for pos in self.shot_positions:
            index = self.board_position_conversion(pos)
            char = 'O'
            for ship in self.ships:
                if pos in ship.positions:
                    char = 'X'
            board_list[index[0]][index[1]] = char
            
        message = '\n' + Board.COL_LABEL + '\n' 
        for index, i in enumerate(board_list):
            message += '   ' + '-' * 41 + '\n'
            message += '{:' '<2d} | {} |'.format(index+1, ' | '.join(i)) + '\n'
        message += '   ' + '-' * 41 + '\n'

        return message
        
    def get_positions_for_ship(self, start_position, direc, length):
        if start_position not in Board.ALL_POSITIONS:
            print 'start position not in valid positions'
            return None, -1
        
        col = start_position[0]
        row = int(start_position[1:]) 
        
        if direc == '2':
            positions = [chr(ord(col)+i) + str(row) for i in range(length)]
        else:
            positions = [col + str(row+i) for i in range(length)]
        
        print '[DEBUGGING] Generated positions for ship: {}'.format(positions)
        for pos in positions:
            if pos not in Board.ALL_POSITIONS:
                return None, 1
        
        
        return positions, 0
        
    def shoot(self, shot_pos):
        self.shot_positions.append(shot_pos)
        for ship in self.ships:
            if shot_pos in ship.positions:
                return 1, ship
        else:
            return 0, None
                
    def is_ship_sunk(self):
        for ship in self.ships:
            if len(ship.hit_positions) == ship.SIZE and ship.sunk == False:
                ship.sunk = True
                return 1, ship
        return 0, None

    def board_position_conversion(self, position):
        col = Board.COLS_MAP[position[0]]
        row = int(position[1:]) - 1
        return row, col

SHIP_NAMES = {  PatrolShip.NAME : PatrolShip,
                Submarine.NAME : Submarine,
                AircraftCarrier.NAME : AircraftCarrier
                }        

BAD_PLACEMENT_MESSAGE = '''
You've entered an invalid position. Please check to 
make sure that it your ship is completely on the board
and that no ships are overlapping!

Remember that the position you give is the top (if
you want vertical) or the left (if you want horizontal).
'''
                
def computer_attack():
    board = Board()
    board.comp_attack = True
    
    #settup loop for each ship
    for ship_name in SHIP_NAMES.keys():
        print board
        unacceptable_answer = True
        while unacceptable_answer:
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
                            if all(position not in ship.positions for position in return_positions):
                                board.ships.append(SHIP_NAMES[ship_name](return_positions))
                                unacceptable_answer = False
                            else: 
                                print BAD_PLACEMENT_MESSAGE
                    else:
                        board.ships.append(SHIP_NAMES[ship_name](return_positions))
                        unacceptable_answer = False
                else:
                   print BAD_PLACEMENT_MESSAGE

    #main play - computer sends consecutive attacks and player is asked if hit      
    while True:
        print board
        shot = choice([pos for pos in board.ALL_POSITIONS if pos not in board.shot_positions])
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
                        break
                    else:
                        print 'Right! The computer hit your {}!'.format(shot_return_ship.NAME)
                        break
                else:
                    print 'Are you sure?\n'
            if response.lower() == 'no':
                if not shot_return:
                    print 'Right! Computer missed!'
                    break
                else:
                    print 'Are you sure?\n'
                    
        #End turn, check gameover status
        if all(ship.sunk == True for ship in board.ships):
            print board
            print 'Game Over! Lets be honest though, it was inevitable. Sorry.'
            break
        
        #DEBUGGING
        for ship in board.ships:
            print ship.NAME, ship.positions, ship.hit_positions, ship.sunk
    
    return None
    
def player_attack():
    board = Board()
    board.comp_attack = False
    #set computer positions
    for Ship in SHIP_NAMES.values():
        while True:
            placement = choice(Board.ALL_POSITIONS)
            hor_or_vert = choice(['1','2'])
            pos, value = board.get_positions_for_ship(placement, hor_or_vert, Ship.SIZE)
            if value == 0:
                board.ships.append(Ship(pos))
                break
    print '\nComputer is Ready!'
    
    while any(ship.sunk == False for ship in board.ships):
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

    print 'Game over! You sunk all of the ships!'
    return None
        
    
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
    
if __name__ == '__main__':
    main()
