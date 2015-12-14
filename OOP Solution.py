#Battleship OOP Implementation
#David Jones
from string import ascii_uppercase as ASCII_UPPERCASE
from itertools import chain
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
    def __init__(self, positions):
        super(Submarine, self).__init__(positions)


class AircraftCarrier(AbstractShip):
    SIZE = 5
    NAME = 'Aircraft Carrier'
    """Child class of ship with 5 placement positions"""
    def __init__(self, positions):
        super(AircraftCarrier, self).__init__(positions)

        
class PatrolShip(AbstractShip):
    SIZE = 2
    NAME = 'Patrol Ship'
    """Child class of ship with 2 placement positions"""
    def __init__(self, positions):
        super(PatrolShip, self).__init__(positions)


class Board(object):
    COLS_MAP = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 
                'E': 4, 'F': 5, 'G':6, 'H': 7, 'I': 8, 'J': 9
                }  
    
    COL_LABEL = '     ' + '   '.join(ASCII_UPPERCASE[:10])
    
    positions = []
    for i in range(1,11):
        positions.append([])
        for let in COLS_MAP.keys():
            positions[i-1].append(let+str(i))
    ALL_POSITIONS = list(chain(*positions))
    
    shot_positions = []
    
    def __init__(self):
        self.ships = []
            
    def __str__(self):
        board = [['.']*10 for i in range(10)]
        
        if self.comp_attack:
            for ship in self.ships:
                for pos in ship.positions:
                    index = self.board_position_conversion(pos)
                    char = 'S'
                    board[index[0]][index[1]] = char
                    
        for pos in Board.shot_positions:
            index = self.board_position_conversion(pos)
            char = 'O'
            for ship in self.ships:
                if pos in ship.positions:
                    char = 'X'
            board[index[0]][index[1]] = char
            
            
        print Board.COL_LABEL
        for index, i in enumerate(board):
            print '   ' + '-' * 41
            print '{:' '<2d} | {} |'.format(index+1, ' | '.join(i))
        print '   ' + '-' * 41
        return ''
        
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
        
        print 'Generated positions for ship: {}'.format(positions)
        for pos in positions:
            if pos not in Board.ALL_POSITIONS:
                return None, 1
        
        return positions, 0
        
    def shoot(self, shot_pos):
        Board.shot_positions.append(shot_pos)
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

Remember that the position you give is the top if
you want vertical, or the left if you want horizontal.'''
                
def computer_attack():
    board = Board()
    board.comp_attack = True
    
    #settup loop for each ship
    for ship_name in SHIP_NAMES.keys():
        print board
        unacceptable_answer = True
        while unacceptable_answer:
            print 'where would you like to place {}\n'.format(ship_name)
            user_position = raw_input('-> ').upper()
            print 'What direction would like it to face?\nEnter 1 for vertical or 2 for horizontal'
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
                        board.ships.append(SHIP_NAMES[ship_name](return_positions))
                        unacceptable_answer = False
            print BAD_PLACEMENT_MESSAGE

    #main play - computer sends consecutive attacks and player is asked if hit      
    while True:
        print board
        shot = choice([pos for pos in board.ALL_POSITIONS if pos not in board.shot_positions])
        shot_return, shot_return_ship = board.shoot(shot)
        print 'Computer shoots {}!\n\n'.format(shot)
        #ask user about hit
        while True:
            print 'Was it a hit? \n Yes or No?'
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
    print 'Computer is Ready!'
    
    while any(ship.sunk == False for ship in board.ships):
        print board
        print 'Where would you like to attack?\n'
        user_attack = raw_input('-> ').upper()
        if user_attack in Board.ALL_POSITIONS and user_attack not in Board.shot_positions:
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
