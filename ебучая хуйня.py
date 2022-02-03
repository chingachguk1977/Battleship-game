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

    def __init__(self, length, bow, orientation, hp) -> None:
        self.length = length
        self.bow = bow
        self.orientation = orientation
        self.hp = hp

    @property
    def ship_body(self) -> list:
        """
        Returns the list of all cells occupied by a ship
        """
        ship_cells = []
        for i in range(self.length):  # in a loop, builds a ship, marking the board dots as occupied
            current_x = self.bow.x
            current_y = self.bow.y

            if self.orientation == 'Horizontal':
                current_x += i
            elif self.orientation == 'Vertical':
                current_y += i

            ship_cells.append(Dot(current_x, current_y))

        return ship_cells  # a list with cells' coordinates occupied by the constructed ship

    def hit(self, shot) -> bool:
        """
        Returns whether or not a ship was hit by a shot (if a shot landed on a cell occupied by a ship)
        """
        return shot in self.ship_body


class Board:

    def __init__(self, hidden=False, size=6):
        self.size = size
        self.hidden = hidden

        self.count = 0  # The number of ships that were sunk
        self.grid = [["≋"] * size for _ in range(size)]  # The actual board grid in the console
        self.busy = []  # List of cells either occupied by a ship or already tried
        self.ships = []

    def __str__(self):
        res = ""
        print("  1 2 3 4 5 6")
        for i, row in enumerate(self.grid):
            res += f"{i + 1}|" + "|".join(row) + "|\n"

        if self.hidden:
            res = res.replace("■", "O")
        return res


b = Board()
print(b)