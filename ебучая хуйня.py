class BoardException():
    """General exception class that can happen in the game
    """
    pass

class ShipOutsideBoard(BoardException):
    """When trying to place your ship outside the board
    """
    pass

class AlreadyShot(BoardException):
    """When you already tried to shoot these coords
    """
    pass

class Dot:
    
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        
    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"
    
    
class Ship:
    
    def __init__(self, length, start_coords, orientation, hp) -> None:
        self.length = length
        self.start_coords = start_coords
        self.orientation = orientation
        self.hp = hp
        
    def dots(self):
        """Returns the list with all dots occupied by a ship
        """
        pass
    
class Board:
    
    def __init__(self) -> None:
        self.cells = 