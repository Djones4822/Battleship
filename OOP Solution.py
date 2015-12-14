#Battleship OOP Implementation
#David Jones
from string import ascii_uppercase as ASCII_UPPERCASE
from itertools import chain

COLS_MAP = {'A': 0, 'C': 2, 'B': 1, 'E': 5, 'D': 4, 'G': 6, 'F':5, 'I': 8, 'H': 7, 'J': 9}  
REV_COL_MAP = {i:let for i, let in COLS_MAP.items()}

class AbstractShip(object):
    """Parent class of all ships."""
    def __init__(self, positions):
        self.sunk = False
        self.positions = Board.get_positions_for_ship(start_position, direction, self.size)
        self.hit_positions = []

    def check_overlap(self, other_ship):
        for pos in self.positions:
            if pos in other_ship.positions:
                return True, pos
        return False, None
        
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

    COL_LABEL = '     ' + '   '.join(ASCII_UPPERCASE[:10])
    
    board = [['.']*10 for i in range(10)]
    positions = []
    shot_positions = []
    
    for i in range(1,11):
        positions.append([])
        for let in COLS_MAP.keys():
            positions[i-1].append(let+str(i))
    
    def __init__(self, ships):
        self.ships = ships
            
    def __str__(self):
        print Board.COL_LABEL
        for index, i in enumerate(Board.positions):
            print '   ' + '-' * 41
            print '{:' '<2d} | {} |'.format(index+1, ' | '.join(i))
        print '   ' + '-' * 41
        return ''
        
    @classmethod
    def get_positions_for_ship(cls, start_position, direc, length):
        for row in cls.positions:
            if start_position not in row:
                return None, -1
        
        col = start_position[0]
        row = start_position[1] - 1
        
        if direc.lower() == 'horizontal':
            positions = [chr(ord(col)+i) + str(row) for i in range(length)]
        elif direc.lower() == 'vertical':
            positions = [col + str(row+i) for i in range(length)]
            
        all_pos_list = chain(*cls.positions)
        
        for pos in positions:
            if pos not in all_pos_list:
                return None, 1
        
        return positions, 0
        
        
class Player(object):
    pass

class Computer(object): 
    pass

ships = []
ship_names = [PatrolShip.name, Submarine.name, AircraftCarrier.name]

start_position = 'A1'
direction = 'Horizontal' 
positions, return_value = Board.get_positions_for_ship(start_position, direction, PatrolShip.size)

for ship_name in ship_names:
    'where would you like to place {}'.format(ship_name)
    if not positions:
         pass
    else:
        ships.append(PatrolShip(positions))
board = Board(ships)

is_hit, ship_name = board.shoot(shot_position)

 

def get_user_start_position():
    pass
