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

class GameBoard:
    """
    Game Board class that receives either AI board or user's board at the init
    """
    def __init__(self, board):
        self.board = board  # we create 2 boards, one for ai and one for human      

    def get_letters2numbers():
        """
        :return: the dict for translation of column names into numbers, 
        to make it look more like a chessboard.
        """
        letters2numbers = {
            'A': 0, 'B': 1, 'C': 2,
            'D': 3, 'E': 4, 'F': 5
        }
        return letters2numbers

    def print_board(self):
        """
        prints out the board to the console
        """
        print("  A B C D E F")
        print("  +-+-+-+-+-+")
        row_num = 1
        for row in self.board:
            print(f"{row_num}|{'|'.join(row)}|")
            row_num += 1
        print("  +-+-+-+-+-+")
        
    

            
            
class Cell:
    MIN_COORD = 0
    MAX_COORD = 6
    
    
    """The cell object on the board with specific coordinates"""
    # dont forget the method to validate the placement of the ship (perhaps using filter)
    def __init__(self, x_row, y_col) -> None:
        self.x_row = x_row
        self.y_col = y_col
        
    def __eq__(self, other) -> bool:
        return self.x_row == other.x_row and self.y_col == other.y_col
    
    @property
    def occupied(self) -> bool:  # occupied by ship? (in ship.list)
        return self.occupied
    
    @occupied.setter
    def occupied(self):
        if 
    
    @property
    def contour(self) -> bool:  # belongs to the contour around the ship?
        pass
    
    @property
    def outside(self) -> bool:  # outside the board?
        return not (Cell.MIN_COORD <= self.x_row <= Cell.MAX_COORD and \
                    Cell.MIN_COORD <= self.y_col <= Cell.MAX_COORD)


class BattleShip:
    """The battleship itself.
    """
    def __init__(self, head, size, orientation) -> None:
        """
        Args:
            size (int): [the length of the ship: 1 three-cell, 2 two-cells, 4 one-cell ships in the flotilla]
            nose (Cell): [the coords of the nose of the ship]
            orientation (str): [hor = horizontal, left-to-right; vert = vertical, downwards]
            hit (list of bool): [len of the ship size, becomes True with each hit]
        """
        self.size = size
        self.head = head
        self.orientation = orientation
        self.hit = [False] * size

    @property
    def is_destroyed(self):
        return all(self.hit)
    
    def ship_cells(self) -> list:
        """
        Returns:
            list: [all the cells on the board occupied by the ship]
        """
        






ai_board = human_board = [[' ']*Cell.MAX_COORD for _ in range(Cell.MAX_COORD)]
aigb = GameBoard(ai_board)
hugb = GameBoard(human_board)
aigb.print_board()
hugb.print_board()