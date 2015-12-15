class AbstractShip(object):
    """Parent class of all ships. With sunk (bool), positions (list), hit_positions (list), and guess_shot (list)"""
    def __init__(self, positions):
        self.sunk = False
        self.positions = positions
        self.hit_positions = []
        self.guess_shot = []


class Submarine(AbstractShip):
    """Child class of ship with 3 placement positions"""
    SIZE = 3
    NAME = 'Submarine'



class AircraftCarrier(AbstractShip):
  """Child class of ship with 5 placement positions"""
    SIZE = 5
    NAME = 'Aircraft Carrier'


class PatrolShip(AbstractShip):
  """Child class of ship with 2 placement positions"""
    SIZE = 2
    NAME = 'Patrol Ship'
