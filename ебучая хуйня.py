from random import randint


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
    MAX_COORD = 6  # Size of the game board (no more than 11 to keep it nice and tidy).

    def __init__(self, hidden=False, size=MAX_COORD):
        self.size = size
        self.hidden = hidden

        self.count = 0  # The number of ships that were sunk
        self.grid = [["o"] * size for _ in range(size)]  # The actual board grid in the console
        self.occupied = []  # List of cells either occupied by a ship or already shot at
        self.ships = []

    def __str__(self):
        res = "  "

        for j in range(Board.MAX_COORD):
            res += f"{j} "

        res += '\n'
        for i, row in enumerate(self.grid):
            res += f"{i}|" + "|".join(row) + "|\n"

        if self.hidden:  # toggles visibility of the ships on the board to the other player
            res = res.replace("■", "o")
        return res

    def off_grid(self, cell) -> bool:
        """
        Verifies that the given dot is not outside the board.
        """
        return not ((0 <= cell.x < self.size) and (0 <= cell.y < self.size))

    def stroke(self, ship, verb=False):
        """
        Creates a single-cell stroke around each ship and toggles all the board cells
        that belong to this stroke as 'occupied.'

        "verb" arg is for 'verbose' i.e. tells us if occupied property should be showed in the console.
        """
        shifts = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for cell in ship.ship_body:
            for dx, dy in shifts:
                current = Dot(cell.x + dx, cell.y + dy)
                if not (self.off_grid(current)) and current not in self.occupied:
                    if verb:
                        self.grid[current.x][current.y] = "."
                    self.occupied.append(current)

    def place_ship(self, ship):

        for cell in ship.ship_body:
            if self.off_grid(cell) or cell in self.occupied:
                raise BoardWrongShipException()
        for cell in ship.ship_body:
            self.grid[cell.x][cell.y] = "■"
            self.occupied.append(cell)

        self.ships.append(ship)
        self.stroke(ship)

    def shot(self, cell) -> bool:
        """
        Make a shot at a ship.
        """
        if self.off_grid(cell):
            raise BoardOutException()
            # if the attempt is outside the board, raise the exception.

        if cell in self.occupied:
            raise BoardUsedException()
            # if this is the second shot at this cell, raise the exception.

        self.occupied.append(cell)  # add this cell to the occupied list

        for ship in self.ships:  # see if the cell belongs to a ship

            if ship.hit(cell):
                ship.hp -= 1
                self.grid[cell.x][cell.y] = "X"

                if ship.hp == 0:
                    self.count += 1

                    # if sunk, stroke the ship so we don't shoot there again
                    self.stroke(ship, verb=True)
                    print("The ship is sunk!")
                    return False
                else:
                    print("Hit!")
                    return True

        self.grid[cell.x][cell.y] = "."
        print("Miss!")
        return False

    def begin(self):
        """
        Before the actual game, we need to empty the occupied list,
        because from this point, it will be used to store the cells
        where the player made their shots.
        """
        self.occupied = []

    def game_over(self) -> bool:
        """
        Defeat if all ships got sunk.
        """
        return self.count == len(self.ships)


class Player:

    def __init__(self, board, opponent):
        self.board = board
        self.opponent = opponent

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.opponent.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):

    def ask(self) -> Dot:
        cell = Dot(randint(0, Board.MAX_COORD), randint(0, Board.MAX_COORD))
        print(f"AI's move: {cell.x + 1} {cell.y + 1}")
        return cell


class Human(Player):

    def ask(self) -> Dot:
        """
        The human player makes their move.
        """
        while True:
            move = input("Your move: ").split()

            if len(move) != 2:
                print(" Enter both coordinates! ")
                continue

            x, y = move

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Coordinates must be numbers! ")
                continue

            x, y = int(x), int(y)

            return Dot(x, y)
            # return Dot(x - 1, y - 1)


class Game:

    def __init__(self, size=Board.MAX_COORD):
        self.size = size
        human = self.forced_gen_ships()
        computer = self.forced_gen_ships()
        computer.hidden = True

        self.ai = AI(computer, human)
        self.human = Human(human, computer)

    def forced_gen_ships(self) -> Board:
        """
        Keeps generating a random board until success.
        """
        board = None
        while board is None:
            board = self.gen_ships()
        return board

    def gen_ships(self) -> Board:
        lengths = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for counter in lengths:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(counter, Dot(randint(0, self.size), randint(0, self.size)), randint(0, 1))
                try:
                    board.place_ship(ship)
                    # if ships placement succeeded, leave the while loop
                    break
                except BoardWrongShipException:
                    # in case of failure, keep trying
                    pass
        board.begin()
        return board

    @staticmethod
    def hello():
        print("-------------------")
        print("  Welcome to the   ")
        print("    BattleShips    ")
        print("-------------------")
        print("  When making your ")
        print(" move, first enter ")
        print(" row, then column. ")
        print("-------------------")

    def game_loop(self):
        move_num = 0
        while True:
            print("-" * 20)
            print("Human Player's board:")
            print(self.human.board)
            print("-" * 20)
            print("AI Player's board:")
            print(self.ai.board)

            if move_num % 2 == 0:
                print("-" * 20)
                print("Your move, Human!")
                repeat = self.human.move()
            else:
                print("-" * 20)
                print("AI's move.")
                repeat = self.ai.move()

            if repeat:  # when the opponent's ship is hit, another move is granted.
                move_num -= 1

            if self.ai.board.game_over:
                print("-" * 20)
                print("Human Player won!")
                break

            if self.human.board.game_over:
                print("-" * 20)
                print("AI Player won!")
                break
            move_num += 1

    def start(self):
        self.hello()
        self.game_loop()


game = Game()
game.start()
