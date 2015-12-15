from ships import AbstractShip, Submarine, PatrolShip, AircraftCarrier
from random import choice
from string import ascii_uppercase as ASCII_UPPERCASE
from computer_attack import computer_attack
from player_attack import player_attack

class Board(object):
    
    COLS_MAP = {ASCII_UPPERCASE[i] : i for i in range(10)}
    COL_LABEL = '     ' + '   '.join(sorted(COLS_MAP.keys()))
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
