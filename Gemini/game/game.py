import random

class TicTacToe:
    """
    A class to represent and manage a game of Tic-Tac-Toe.
    """
    def __init__(self):
        """
        Initializes the Tic-Tac-Toe game.
        """
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.player_symbol = 'X'
        self.computer_symbol = 'O'
        self.current_winner = None

    def print_board(self):
        """
        Prints the current state of the board.
        """
        for row in self.board:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        """
        Prints the board with numbers to show players the cell mapping.
        """
        number_board = [[str(i) for i in range(j * 3 + 1, j * 3 + 4)] for j in range(3)]
        print("Board Positions:")
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def get_available_moves(self):
        """
        Returns a list of available moves as (row, col) tuples.
        """
        return [(r, c) for r, row in enumerate(self.board) for c, spot in enumerate(row) if spot == ' ']

    def has_empty_squares(self):
        """
        Checks if there are any empty squares left on the board.
        """
        return ' ' in [spot for row in self.board for spot in row]

    def make_move(self, square, symbol):
        """
        Makes a move on the board if the square is available.

        Args:
            square (tuple): A (row, col) tuple for the move.
            symbol (str): The player's symbol ('X' or 'O').

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        row, col = square
        if self.board[row][col] == ' ':
            self.board[row][col] = symbol
            if self.check_winner(square, symbol):
                self.current_winner = symbol
            return True
        return False

    def check_winner(self, square, symbol):
        """
        Checks if the recent move resulted in a win.

        Args:
            square (tuple): The (row, col) of the last move.
            symbol (str): The symbol of the player who made the move.

        Returns:
            bool: True if the player has won, False otherwise.
        """
        row, col = square

        # Check row
        if all([spot == symbol for spot in self.board[row]]):
            return True

        # Check column
        if all([self.board[r][col] == symbol for r in range(3)]):
            return True

        # Check diagonals (only if move is on a diagonal)
        if row == col:
            # Top-left to bottom-right diagonal
            if all([self.board[i][i] == symbol for i in range(3)]):
                return True
        if row + col == 2:
            # Top-right to bottom-left diagonal
            if all([self.board[i][2 - i] == symbol for i in range(3)]):
                return True

        return False

def play():
    """
    Function to run a game (for testing purposes).
    This will not be used when importing the class as a module.
    """
    game = TicTacToe()
    game.print_board_nums()

    while game.has_empty_squares() and not game.current_winner:
        game.print_board()
        # Example of making a random move for 'X'
        move = random.choice(game.get_available_moves())
        game.make_move(move, 'X')

    game.print_board()
    if game.current_winner:
        print(f"Player {game.current_winner} wins!")
    else:
        print("It's a tie!")

if __name__ == '__main__':
    play()
