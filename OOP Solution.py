#Battleship OOP Implementation
#David Jones
from string import ascii_uppercase as ASCII_UPPERCASE
from itertools import chain
from random import choice

bad_placement_message = '''
You've entered an invalid position. Please check to 
make sure that it your ship is completely on the board
and that no ships are overlapping!

Remember that the position you give is the top if
you want vertical, or the left if you want horizontal.'''

class AbstractShip(object):
    """Parent class of all ships."""
    def __init__(self, positions, hit_positions = []):
        self.sunk = False
        self.positions = positions
        self.hit_positions = hit_positions


class Submarine(AbstractShip):
    SIZE = 3
    NAME = 'Submarine'
    """Child class of ship with 3 placement positions"""
    def __init__(self, positions):
        super(Submarine, self).__init__(positions)
        self.hit_positions = []


class AircraftCarrier(AbstractShip):
    SIZE = 5
    NAME = 'Aircraft Carrier'
    """Child class of ship with 5 placement positions"""
    def __init__(self, positions):
        super(AircraftCarrier, self).__init__(positions)
        self.hit_positions = []


class PatrolShip(AbstractShip):
    SIZE = 2
    NAME = 'Patrol Ship'
    """Child class of ship with 2 placement positions"""
    def __init__(self, positions):
        super(PatrolShip, self).__init__(positions)
        self.hit_positions = []


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
        for ship in self.ships:
            for pos in ship.positions:
                index = self.board_position_conversion(pos)
                char = 'S'
                board[index[0]][index[1]] = char
        for pos in Board.shot_positions:
            index = self.board_position_conversion(pos)
            for ship in self.ships:
                if pos in ship.positions:
                    char = 'X'
                else:
                    char = 'O'
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
                print 'HIT {}'.format(ship.NAME)
                return 1, ship.NAME
        else:
            print 'MISS'
            return 0, None

    def is_ship_sunk(self):
        for ship in self.ships:
            if len(ship.hit_positions) == ship.SIZE and ship.sunk == False:
                ship.sunk = True
                return 1, ship.NAME
        return 0, None

    def board_position_conversion(self, position):
        col = Board.COLS_MAP[position[0]]
        row = int(position[1:]) - 1
        return row, col


def main():
    board = Board()
    ships = []
    ship_names = {  PatrolShip.NAME : PatrolShip,
                    Submarine.NAME : Submarine,
                    AircraftCarrier.NAME : AircraftCarrier}
    for ship_name in ship_names.keys():
        print board
        while True:
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
                                                    ship_names[ship_name].SIZE)
                if return_value == 0:
                    if ships:
                        for ship in ships:
                            if all(position not in ship.positions for position in return_positions):
                                board.ships.append(ship_names[ship_name](return_positions))
                                break
                    else:
                        board.ships.append(ship_names[ship_name](return_positions))
                        break
            print bad_placement_message

    # main game loop
    while True:
        print board
        shot = choice([pos for pos in board.ALL_POSITIONS if pos not in board.shot_positions])
        shot_return, shot_return_ship = board.shoot(shot)
        print 'Computer shoots {}!\n\n'.format(shot)
        while True:
            print 'Was it a hit? \n Yes or No? -> '
            response = raw_input('')
            if response.lower() == 'yes':
                if shot_return:
                    ship_names[shot_return_ship].hit_positions.append(shot)
                    sunk_check_value, sunk_check_ship = board.is_ship_sunk()
                    if sunk_check_value == 1:
                        print 'Right! The computer sunk your {}!'.format(sunk_check_ship)
                        break
                    else:
                        print 'Right! The computer hit your {}!'.format(shot_return_ship)
                        break
                else:
                    print 'Are you sure?\n'
            if response.lower() == 'no':
                if not shot_return:
                    print 'Right! Computer missed!'
                    break
                else:
                    print 'Are you sure?\n'

        #Game over Check
        if all(ship.sunk == True for ship in board.ships):
            print 'Game Over! Lets be honest though, it was inevitable. Sorry.'
            break

main()
