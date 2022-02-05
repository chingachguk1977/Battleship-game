from random import randint


class Dot:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return f"Dot({self.x}, {self.y})"


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


class Ship:

    def __init__(self, length, bow, orientation) -> None:
        self.length = self.hp = length
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

            if self.orientation == 0:  # 'Hor':
                current_x += i
            elif self.orientation == 1:  # 'Vert':
                current_y += i

            ship_cells.append(Dot(current_x, current_y))

        return ship_cells  # a list with cells' coordinates occupied by the constructed ship

    def hit(self, shot) -> bool:
        """
        Returns whether or not a ship was hit by a shot (if a shot landed on a cell occupied by a ship)
        """
        return shot in self.ship_body


class Board:
    MAX_COORD = 10  # Size of the game board (no more than 11 to keep it nice and tidy).
    BLUE = "\033[34m"
    RED = "\033[31m"
    ORIGIN_COLOR = "\033[0m"

    def __init__(self, hidden=False, size=MAX_COORD):
        self.size = size
        self.hidden = hidden

        self.sunk_ships = 0  # The number of ships that were sunk
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
            for _ in range(len(self.ships)):
                res = res.replace("■", Board.ORIGIN_COLOR + "o")
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

        "verb" arg is for 'verbose' i.e. toggles the visibility of occupied property.
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
                        self.grid[current.x][current.y] = Board.ORIGIN_COLOR + "."
                    self.occupied.append(current)

    def place_ship(self, ship):
        for cell in ship.ship_body:
            if self.off_grid(cell) or cell in self.occupied:
                raise BoardWrongShipException()
        for cell in ship.ship_body:
            self.grid[cell.x][cell.y] = Board.BLUE + "■" + Board.ORIGIN_COLOR
            self.occupied.append(cell)

        self.ships.append(ship)
        self.stroke(ship)

    def shot(self, cell) -> bool:
        """
        Make a shot at a ship and returns yes/no to the 'Player.move" method.
        """
        if self.off_grid(cell):
            raise BoardOutException()
            # if the attempt is outside the board, raise the exception.

        if cell in self.occupied:
            raise BoardUsedException()
            # if this is the second shot at this cell, raise the exception.

        self.occupied.append(cell)  # add this cell to the occupied list

        for ship in self.ships:  # see if the cell belongs to a ship
            if cell in ship.ship_body:
                ship.hp -= 1
                self.grid[cell.x][cell.y] = Board.RED + "X" + Board.ORIGIN_COLOR

                if ship.hp == 0:
                    self.sunk_ships += 1

                    # if sunk, stroke the ship so we don't shoot there again
                    self.stroke(ship, verb=True)
                    print("The ship is sunk!")
                    return True
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

    @property
    def game_over(self) -> bool:
        """
        Defeat if all ships got sunk.
        """
        return self.sunk_ships == len(self.ships)


class Player:

    def __init__(self, board, opponent):
        self.board = board
        self.opponent = opponent

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()  # asks Player for input of coords to shoot
                repeat = self.opponent.shot(target)  # receives hit/miss from Board.shot
                return repeat  # if hit/sunk, grants another move
            except BoardException as e:
                print(e)


class AI(Player):

    def ask(self) -> Dot:
        cell = Dot(randint(0, Board.MAX_COORD - 1), randint(0, Board.MAX_COORD - 1))
        # print(f"AI's move: {cell.x + 1} {cell.y + 1}")
        return cell  # returns coords of the attempted shot


class Human(Player):

    def ask(self) -> Dot:
        """
        The human player makes their move.
        """
        while True:
            move = input("Coordinates to shoot? ").split()

            if len(move) != 2:
                print(" Enter both coordinates! ")
                continue

            x, y = move

            if (not x.isdigit()) or (not y.isdigit()):
                print(" Coordinates must be numbers! ")
                continue

            x, y = int(x), int(y)

            return Dot(x, y)  # returns coords of the attempted shot


class Game:

    def __init__(self):
        self.size = Board.MAX_COORD
        human = self.forced_gen_ships()
        computer = self.forced_gen_ships()
        computer.hidden = True  # Whether we want to hide AI's board to the Human

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
        """
        The number and length of ships is determined by the board dimensions
        and are randomized: fewer ships that are bigger & more smaller ships.
        """
        lengths = list([4]*randint(0, Board.MAX_COORD // 4) \
                    + [3]*randint(1, Board.MAX_COORD // 3) \
                        + [2]*randint(2, Board.MAX_COORD // 2) \
                            + [1]*randint(3, Board.MAX_COORD // 2 + 1))
        board = Board()
        attempts = 0
        for counter in lengths:
            """
            counter defines the length and hp of each ship as given in the lengths list above.
            """
            while True:
                attempts += 1
                if attempts > 1000:
                    return None
                ship = Ship(counter, Dot(randint(0, self.size), randint(0, self.size)), randint(0, 1))
                try:
                    board.place_ship(ship)
                    """
                    if the ship's placement succeeded, leave the while loop
                    and switch to the next ship.
                    """
                    break
                except BoardWrongShipException:
                    """
                    in case of failure, keep trying (resume the while loop)
                    """
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
            print("-" * (Board.MAX_COORD * 3 + 3))
            print("Human Player's board:")
            print(self.human.board)
            print("-" * (Board.MAX_COORD * 3 + 3))
            print("AI Player's board:")
            print(self.ai.board)

            if move_num % 2 == 0:
                print("-" * (Board.MAX_COORD * 3 + 3))
                print("Your move, Human!")
                repeat = self.human.move()
            else:
                print("-" * (Board.MAX_COORD * 3 + 3))
                print("AI's move.")
                repeat = self.ai.move()

            if repeat:  # when the opponent's ship is hit, another move is granted.
                move_num -= 1

            if self.ai.board.game_over:
                print("-" * (Board.MAX_COORD * 3 + 3))
                print()
                print("AI's flotilla destroyed! You won, Human!")
                print(self.ai.board)
                break

            if self.human.board.game_over:
                print("-" * (Board.MAX_COORD * 3 + 3))
                print("AI has killed all humans!")
                print(self.human.board)
                break
            move_num += 1

    def start(self):
        self.hello()
        self.game_loop()


game = Game()
game.start()
