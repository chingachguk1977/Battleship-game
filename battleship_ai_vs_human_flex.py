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
    
    MIN_COORD = 0
    MAX_COORD = 6
    
    def create_board(self):
        cells_horizontal = []
        for i in range(GameBoard.MAX_COORD):
            cells_vertical = []
            for j in range(GameBoard.MAX_COORD):
                cell_ = Cell(i, j)
                cells_horizontal.append(cell_)
            cells_vertical.append(cells_horizontal)
            
    def print_board(self):
        print("  1 2 3 4 5 6")
        print("  +-+-+-+-+-+")
        for i in range(GameBoard.MAX_COORD):
            for j in range(GameBoard.MAX_COORD):
                cell_status = Cell(i, j)
            print(f"{i+1}|{'|'.join(str(cell_status)*GameBoard.MAX_COORD)}|")
        print("  +-+-+-+-+-+")

            
class Cell:
    _status = None
    ALLOWED_STATI = ['Occupied', 'Contour', 'Free', 'Hit', 'Miss']
    _show = None
    
    """The cell object on the board with specific coordinates and status"""
    # dont forget the method to validate the placement of the ship (perhaps using filter)
    def __init__(self, x_row, y_col) -> None:
        self.x_row = x_row
        self.y_col = y_col
    
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, new_status):
        if new_status in Cell.ALLOWED_STATI:
            self._status = new_status
        
    @property
    def show(self):
        return self._show
    
    @show.setter
    def show(self, yesno: bool):
        if isinstance(yesno, bool):
            self._show = yesno
            
    def __eq__(self, other) -> bool:
        return self.x_row == other.x_row and self.y_col == other.y_col
    
    def __str__(self):
        if self.status == 'Occupied':
            return "█"
        elif self.status == 'Contour':
            return "░"
        elif self.status == 'Free':
            return "≋"
        elif self.status == 'Hit':
            return "⋇"
        elif self.status == 'Miss':
            return "╳"
        else: return "·"
    
    def __repr__(self):
        return f"({self.x_row}, {self.y_col})"
    
    @property
    def occupied(self) -> bool:  # occupied by ship? (in ship.list)
        return self._status == 'Occupied'

    @property
    def contour(self) -> bool:  # belongs to the contour around the ship?
        return self._status == 'Contour'
    
    @property
    def outside(self) -> bool:  # outside the board?
        return not (GameBoard.MAX_COORD <= self.x_row <= GameBoard.MAX_COORD and \
                    GameBoard.MAX_COORD <= self.y_col <= GameBoard.MAX_COORD)


class BattleShip:
    """The battleship itself.
    """
    def __init__(self, head, size, orientation) -> None:
        """
        Args:
            size (int): [the length of the ship: 1 three-cell, 2 two-cells, 4 one-cell ships in the flotilla]
            head (Cell): [the coords of the nose of the ship]
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
    
    @property
    def is_hit(self):
        return any(self.hit)
    
    def create_ship(self) -> list:
        self.ship_cells = []
        length = self.size
        """
        Returns:
            list: [cells on the board occupied by the ship]
        """
        ship_cell = Cell(self.head[0], self.head[1])
        ship_cell.status = 'Occupied'
        while length >= self.size:
            self.ship_cells.append(repr(ship_cell))
            ship_cell.status = 'Occupied'
            
            length -= 1
            
            
            # прописать клетки вокруг contour_cell = Cell(self.head[0], self.head[1])
            
            






aigb = GameBoard()
hugb = GameBoard()

aigb.create_board()
hugb.create_board()
x = Cell(2,3)
x.status = "Hit"
aigb.print_board()
hugb.print_board()
