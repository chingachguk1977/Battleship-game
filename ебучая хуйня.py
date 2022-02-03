class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Your shot will land outside the board!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "You've already shot here!"


class BoardWrongShipException(BoardException):
    """
    This exception happens when the placement of a ship does not conform
    with the rules of the game (partially or entirely outside the board,
    or too close to another ship that had already been placed.

    Has no console representation, used internally.)
    """
    pass


class Dot:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return f"Dot({self.x}, {self.y})"


class Ship:

    def __init__(self, length, bow, orientation) -> None:
        self.length = length
        self.bow = bow
        self.orientation = orientation

    @property
    def ship_body(self) -> list:
        """
        Returns the list of all cells occupied by a ship
        """
        ship_cells = []
        for i in range(self.length):  # in a loop, builds a ship, marking the board dots as occupied
            current_x = self.bow.x
            current_y = self.bow.y

            if self.orientation == 'Vert':
                current_x += i
            elif self.orientation == 'Hor':
                current_y += i

            ship_cells.append(Dot(current_x, current_y))

        return ship_cells  # a list with cells' coordinates occupied by the constructed ship

    def hit(self, shot) -> bool:
        """
        Returns whether or not a ship was hit by a shot (if a shot landed on a cell occupied by a ship)
        """
        return shot in self.ship_body


class Board:
    MAX_COORD = 6

    def __init__(self, hidden=False, size=MAX_COORD):
        self.size = size
        self.hidden = hidden

        self.count = 0  # The number of ships that were sunk
        self.grid = [["o"] * size for _ in range(size)]  # The actual board grid in the console
        self.occupied = []  # List of cells either occupied by a ship or already shot at
        self.ships = []

    def __str__(self):
        res = ""
        res += "  1 2 3 4 5 6\n"
        for i, row in enumerate(self.grid):
            res += f"{i + 1}|" + "|".join(row) + "|\n"

        if self.hidden:  # toggles visibility of the ships on the board to the other player
            res = res.replace("█", "o")
        return res

    def off_grid(self, dot) -> bool:
        """
        Verifies that the given dot is not outside the board.
        """
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def stroke(self, ship, verb=False):
        """
        Creates a single-cell stroke around each ship and toggles all the board cells
        that belong to this stroke as 'occupied.'

        "verb" arg is for 'verbose' i.e. tells us if occupied property should be showed in the console.
        """
        shifts = [
            (-1, -1), (-1, 0), (-1, 1),
            (0,  -1), (0,  0), (0,  1),
            (1,  -1), (1,  0), (1,  1)
        ]

        for cell in ship.ship_body:
            for dx, dy in shifts:
                cur = Dot(cell.x + dx, cell.y + dy)
                if not(self.off_grid(cur)) and cur not in self.occupied:
                    if verb:
                        self.grid[cur.x][cur.y] = "."
                    self.occupied.append(cur)

    def place_ship(self, ship):

        for cell in ship.ship_body:
            if self.off_grid(cell) or cell in self.occupied:
                raise BoardWrongShipException()
        for cell in ship.ship_body:
            self.grid[cell.x][cell.y] = "■"
            self.occupied.append(cell)

        self.ships.append(ship)
        self.stroke(ship)


b = Board()
b.place_ship(Ship(3, Dot(0, 2), 'Vert'))
b.stroke(Ship(3, Dot(0, 2), 'Vert'))
print(b)
