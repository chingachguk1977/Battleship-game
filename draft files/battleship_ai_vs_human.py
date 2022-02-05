import random


class GameBoard:
    """
    Game Board class that receives either AI board or user's board at the init
    """

    def __init__(self, board):
        self.board = board

    @staticmethod
    def get_letters2numbers():
        """
        :return: the dict for translation of column names into numbers, 
        to make it look more like a chessboard, and I want to make it 8 by 8 board.
        """
        letters2numbers = {
            'A': 0, 'B': 1, 'C': 2, 'D': 3,
            'E': 4, 'F': 5, 'G': 6, 'H': 7
        }
        return letters2numbers

    def print_board(self):
        """
        prints out the board to the console
        """
        print("  A B C D E F G H")
        print("  +-+-+-+-+-+-+-+")
        row_num = 1
        for row in self.board:
            print(f"{row_num}|{'|'.join(row)}|")
            row_num += 1


class Battleship:
    """1 корабль на 3 клетки, 2 корабля на 2 клетки, 4 корабля на одну клетку
    """

    def __init__(self, board) -> None:
        self.board = board

    def create_ships(self):
        """self here refers to the AI board

        Returns:
            [type]: [description]
        """
        for i in range(5):
            self.x_row, self.y_column = random.randint(0, 7), random.randint(0, 7)
            while self.board[self.x_row][self.y_column] == 'X':  # loops to see if something is already placed here
                self.x_row, self.y_column = random.randint(0, 7), random.randint(0, 7)  # if yes, re-randomize
            self.board[self.x_row][self.y_column] = 'X'
        return self.board

    def get_user_input(self):
        try:
            x_row = input("Enter the row of the ship: ")
            while x_row not in '12345678':  # тут надо обработку исключений поставить будет
                print("Inappropriate choice, please enter a valid row.")
                x_row = input("Enter the row of the ship: ")

            y_column = input("Enter the column letter of the ship: ").upper()
            while y_column not in 'ABCDEFGH':  # тут надо обработку исключений поставить будет
                print("Inappropriate choice, please enter a valid column.")
                y_column = input("Enter the column letter of the ship: ").upper()
            return int(x_row) - 1, GameBoard.get_letters2numbers()[y_column]  # return a tuple with coords

        except ValueError and KeyError:  # message and keep calling the same method until the input is valid
            print("Not a valid input")
            return self.get_user_input()

    def count_hit_ships(self):
        hit_ships = 0
        for row in self.board:
            for column in row:
                if column == 'X':
                    hit_ships += 1
        return hit_ships


def RunGame():
    ai_board = GameBoard([[' '] * 8 for _ in range(8)])
    guess_board = GameBoard([[' '] * 8 for _ in range(8)])

    Battleship.create_ships(ai_board)  # call for placing all the ships and store in ai_board

    turns = 10
    while turns > 0:
        GameBoard.print_board(guess_board)
        user_x_row, user_y_column = Battleship.get_user_input(object)  # getting user input where to shoot
        while guess_board.board[user_x_row][user_y_column] == '-' or \
                guess_board.board[user_x_row][user_y_column] == 'X':
            print("You've already shot these coordinates.")
            user_x_row, user_y_column = Battleship.get_user_input(object)  # retry the user input where to shoot
        if ai_board.board[user_x_row][user_y_column] == "X":
            print("You sunk one of my ships!")
            guess_board.board[user_x_row][user_y_column] = "X"  # a ship is hit/sunk and need to mark it on user's board
        else:
            print("You missed!")
            guess_board.board[user_x_row][user_y_column] = "-"  # a miss

        if Battleship.count_hit_ships == 5:
            print("All ships were sunk")
            break
        else:
            turns -= 1
            print(f"You have {turns} turns remaining.")
            if turns == 0:
                print("You ran out of turns, game over.")
                GameBoard.print_board(guess_board)
                break


if __name__ == '__main__':
    RunGame()
