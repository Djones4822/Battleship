from string import ascii_uppercase as ASCII_UPPERCASE
from random import choice
import time


class AbstractShip(object):
    """Parent class of all ships."""
    def __init__(self, positions):
        self.sunk = False
        self.positions = positions
        self.hit_positions = []
        self.guess_shot = []


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
    COL_LABEL = '    ' + '   '.join([str(i) for i in range(1,11)])
    ALL_POSITIONS = [let + str(i) for let in COLS_MAP.keys() for i in range(1,11)]
    
    def __init__(self):
        self.ships = []
        self.shot_positions = []
        self.comp_attack = None
        self.last_miss = True
        
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
            message += '  ' + '-' * 41 + '\n'
            message += '{} | {} |'.format(ASCII_UPPERCASE[index], ' | '.join(i)) + '\n'
        message += '  ' + '-' * 41 + '\n'

        return message
        
    def get_positions_for_ship(self, start_position, direc, length):
        if start_position not in Board.ALL_POSITIONS:
            print 'start position not in valid positions'
            return None, -1
        
        col = start_position[0]
        row = int(start_position[1:]) 
        
        if direc == '1':
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
        return col, row
        
    def smart_attack(self):
        if self.smart_attack_on:
            for ship in self.ships:
                if not ship.sunk and ship.hit_positions:
                    if len(ship.hit_positions) == 1:
                        if not ship.guess_shot:
                            know = ship.hit_positions[0]
                            tries = []
                            tries.append(chr(ord(know[0])-1) + know[1:])
                            tries.append(chr(ord(know[0])+1) + know[1:])
                            tries.append(know[0] + str(int(know[1:]) + 1))
                            tries.append(know[0] + str(int(know[1:]) - 1))
                            print ('DEBUGGING: All Possible tries: {}'.format(tries))
                            for try_shot in tries:
                                if try_shot in Board.ALL_POSITIONS and try_shot not in self.shot_positions:
                                    ship.guess_shot.append(try_shot)
                        print('DEBUGGING: Valid tries: {}'.format(ship.guess_shot))
                        shot = choice(ship.guess_shot)
                        ship.guess_shot.remove(shot)
                        print ('DEBUGGING: Chosen shot: {} \nDEBUGGING: remaining guesses: {}'.format(shot, ship.guess_shot))
                        return shot
                    else:
                        if not self.last_miss:
                            knowns = ship.hit_positions[-2:]
                            known1, known2 = knowns[0], knowns[1]
                            k1_col, k1_row = ord(known1[0]), int(known1[1:])
                            k2_col, k2_row = ord(known2[0]), int(known2[1:])
                            slope = (k2_col - k1_col, k2_row - k1_row)
                            index = (k2_col + slope[0], k2_row + slope[1])
                            shot = chr(index[0]) + str(index[1])
                            print ('DEBUGGING: slope: {}\tknown1: {}\tknown2: {}\tshot: {}'.format(slope, known1, known2, shot))
                            if shot not in Board.ALL_POSITIONS:
                                self.last_miss = True
                                return self.smart_attack()
                            return shot
                        else:
                            print 'DEBUGGING: Last shot missed, now heading in other direction starting from the first shot'
                            knowns = ship.hit_positions[0:2]
                            known1, known2 = knowns[0], knowns[1]
                            k1_col, k1_row = ord(known1[0]), int(known1[1:])
                            k2_col, k2_row = ord(known2[0]), int(known2[1:])
                            slope = (k1_col - k2_col, k1_row - k2_row)
                            index = (k1_col + slope[0], k1_row + slope[1])
                            shot = chr(index[0]) + str(index[1])
                            fixer = ship.hit_positions.pop(0)
                            ship.hit_positions.append(fixer)
                            print ('DEBUGGING: slope: {}\tknown1: {}\tknown2: {}\tshot: {}'.format(slope, known1, known2, shot))
                            return shot

        return choice([pos for pos in self.ALL_POSITIONS if pos not in self.shot_positions])

SHIP_NAMES = {  Submarine.NAME : Submarine,
                AircraftCarrier.NAME : AircraftCarrier,
                PatrolShip.NAME : PatrolShip
                }

BAD_PLACEMENT_MESSAGE = '''
Your ship is too big for those spaces. Remember that\
if you want a vertical ship, then the position you give is \
the top position. If you wankt a horizontal ship then the \
position is the left most.'''

def setup_player_board():
    player_board = Board()
    player_board.comp_attack = True
    
    print 'Would you like to play a smart or a dumb computer?\nEnter 1 for Smart or 2 for Dumb\n'
    while True:
        smart_or_dumb = raw_input('-> ')
        if smart_or_dumb == '1' or smart_or_dumb == '2':
            player_board.smart_attack_on = not bool(int(smart_or_dumb)-1)
            break
        else:
            print 'Enter 1 or 2 please.'
            
    
    print 'Ok, Please place your ships!\n\n'
    for ship in SHIP_NAMES.values():
        print 'You have 1 {} that is {} spaces large.'.format(ship.NAME, ship.SIZE)
        
    for ship_name in SHIP_NAMES.keys():
        print player_board
        acceptable_answer = False
        while not acceptable_answer:
            print 'Please give the top/left most point of where you want your {} to go. e.g. A9 or F4\n'.format(ship_name)
            user_position = raw_input('-> ').upper()
            print 'What direction would like it to face?\nEnter 1 for vertical or 2 for horizontal.'
            user_direction = raw_input('-> ')
            if user_position in Board.ALL_POSITIONS and user_direction == '1' \
                                                    or user_direction == '2':
                return_positions, return_value = \
                                                player_board.get_positions_for_ship(
                                                    user_position, 
                                                    user_direction, 
                                                    SHIP_NAMES[ship_name].SIZE)
                if return_value == 0:
                    if player_board.ships:
                        for ship in player_board.ships:
                            if any((position in ship.positions) for position in return_positions):
                                print 'Your ships are overlapping!'
                        else:
                            player_board.ships.append(SHIP_NAMES[ship_name](return_positions))
                            acceptable_answer = True
                    else:
                        player_board.ships.append(SHIP_NAMES[ship_name](return_positions))
                        acceptable_answer = True
                        
                elif return_value == 1:
                    print BAD_PLACEMENT_MESSAGE
            else:
                    print 'You entered an invalid starting position.'
    print 'Ok! Here\'s your board!'
    print player_board
    return player_board
    
def setup_computer_board():
    computer_board = Board()
    computer_board.comp_attack = False
    
    for Ship in SHIP_NAMES.values():
        while True:
            placement = choice(Board.ALL_POSITIONS)
            hor_or_vert = choice(['1','2'])
            pos, value = computer_board.get_positions_for_ship(placement, hor_or_vert, Ship.SIZE)
            if value == 0:
                computer_board.ships.append(Ship(pos))
                break
        
    return computer_board

def competitive_play():
    
    player_board = setup_player_board()
    computer_board = setup_computer_board()
    
    print 'Ok... Ready? Game is starting in 5 Seconds!'
    time.sleep(5)
    
    #main game loop
    print '\n\n\n\n\n\n\n\n\nSTARTING GAME!!!\n\n'
    turn_count = 0
    while player_board.ships and computer_board.ships:
        turn_count +=1
        print 'Turn Number {}!'.format(turn_count)
        
        #Here, the Player attacks the computer's board using the computer_board object
        print 'Player Turn!\n'
        print 'Here\'s what you know about the computer\'s Board'
        print computer_board
        #Player Attacks the Computer
        while True:
            print 'Where would you like to attack?\n'
            user_attack = raw_input('-> ').upper()
            if user_attack in Board.ALL_POSITIONS and user_attack not in computer_board.shot_positions:
                shot_return, shot_return_ship = computer_board.shoot(user_attack)
                if shot_return:
                    print 'Hit!'
                    shot_return_ship.hit_positions.append(user_attack)
                    sunk_check_value, sunk_check_ship = computer_board.is_ship_sunk()
                    if sunk_check_value:
                        print 'You\'ve sunk the {}!'.format(sunk_check_ship.NAME)
                    break
                else:
                    print 'Miss!'
                    break
            else:
                print 'You\'ve either entered and invalid position or you\'ve already shot there!\n'

        if all(ship.sunk == True for ship in computer_board.ships):
            print computer_board
            print 'You win! Yayyyyyy'
            return 1, turn_count
        time.sleep(1.5)

        #Here the computer attacks the player's board using the player_board object
        print '\nComputer Turn!\n'
        time.sleep(1)
        print 'Here\'s your board'
        print player_board
        time.sleep(1)
        shot = player_board.smart_attack()
        shot_return, shot_return_ship = player_board.shoot(shot)
        print 'Computer shoots {}!'.format(shot)
        #ask user about hit
        while True:
            print 'Hit or Miss?'
            response = raw_input('-> ')
            if response.lower() == 'hit':
                if shot_return:
                    shot_return_ship.hit_positions.append(shot)
                    sunk_check_value, sunk_check_ship = player_board.is_ship_sunk()
                    if sunk_check_value == 1:
                        print 'Right! The computer hit and sunk your {}!'.format(sunk_check_ship.NAME)
                        player_board.last_miss = True
                        break
                    else:
                        print 'Right! The computer hit your {}!'.format(shot_return_ship.NAME)
                        player_board.last_miss = False
                        break
                else:
                    print 'Are you sure?\n'
            if response.lower() == 'miss':
                if not shot_return:
                    print 'Right! Computer missed!'
                    player_board.last_miss = True
                    break
                else:
                    print 'Are you sure?\n'
                    
        if all(ship.sunk == True for ship in player_board.ships):
            print computer_board
            print 'You lose! The Computer won! This is why you never go in against a Sicilian when death is on the line!'
            return 0, turn_count
        
        time.sleep(3)
    
def main():
    print 'Welcome to Battleship!\n\n'
    print 'Press Enter to Play!\n'
    raw_input('')
    
    result, tries = competitive_play()
    
    if result:
        print 'Wow, it took you {} tries to win! Good job!'.format(tries)
    else:
        print 'Jeez, how long did it take for you to lose in {} tries?'.format(tries)
    
    print '\n\nPlay again? (Yes or No)\n'
    response = raw_input('-> ')
    if response.lower() == 'yes':
        main()
    
    print 'Thanks for playing!'
    
if __name__ == '__main__':
    main()
else:
    main()
