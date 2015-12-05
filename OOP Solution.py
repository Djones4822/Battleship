#Battleship OOP Implementation
#David Jones


class Ship(object):
    """Parent class of all ships."""
    def __init__(self):
        self.sunk = False
        
    def check_position(self, position, board):
        """Checks the given position against the board to make sure there are no
        intersections of ships and that the entire ship is on the game board"""
        spaces = self.health
        direciton = self.direction

    @property
    def position(self):
        user_position = raw_input("""Where would you like to place this ship?
                                    \n\n-> """)
        if user_position not in GAMEBOARD_OBJECT: #Haven't thought this part all the way through yet
            print "You haven't given a valid position!"
            position()
        else:
            pass
        
    @property
    def direction(self):
        user_direction = raw_input("""What direction would you like it to face? 
                                Vertical or Horizontal?\n\n-> """)
        if user_direction.lower() not in ('vertical','horizontal'):
            print "You haven't given a valid direction!"
            direction()
        else:
            return user_direction
            
class Submarine(Ship):
    """Child class of ship with 3 placement positions"""
    def __init__(self):
        super(Submarine).__init__()
        self.health = 3
        

class AircraftCarrier(Ship):
    """Child class of ship with 5 placement positions"""
    def __init__(self):
        super(AircraftCarrier).__init__()
        self.health = 5
        
class PatrolShip(Ship):
    """Child class of ship with 2 placement positions"""
    def __init__(self):
        super(PatrolShip).__init__()
        self.health = 2
        
    

class Board(object):
    pass

class Player(object):
    pass

class Computer(object): 
    pass




Sub: 3, aircraft:5, patrol:2
