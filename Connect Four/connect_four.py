import random
import numpy as np


class Player:
    """
    Defines the player characteristics and abilities.
    """

    def __init__(self, mark: str):
        self.name = input(f"🤖 : Please, {mark} player, enter your name : ")
        self.name = f"Player_{mark}" if not (self.name) else self.name
        self.mark = mark

    def move(self, board: object, game: object):
        """
        Asks the player to move from row, column and checks if move is available.

        Parameters:
            board: From Board class, the board on which we play.
            game: Current game instance (needed for winning condition checks).
        """
        while True:
            try:
                print(f"🤖 : It's {self.name} turn.\n")
                print(f"🤖 : Let's place '{self.mark}' !\n")

                col = int(
                    input(f"🤖 : {self.name}, enter the column (0-{board.column-1}): ")
                )
                if not (0 <= col <= board.column - 1):
                    raise ValueError

                if board.is_move_available(col):
                    board.update_board(col, self.mark)
                    break
                else:
                    print(
                        f"\n❌❌ Column {col} is full !! ❌❌\n🤖 : Please choose another column.\n"
                    )
                    board.print_board_with_borders()
            except ValueError:
                print(
                    f"❌❌ Invalid input !! ❌❌\n🤖 : Please enter numbers between 0 and {board.column-1}.\n"
                )
                board.print_board_with_borders()


class ComputerPlayer(Player):
    """
    Defines the characteristics and abilities for a computer player.
    """

    def __init__(self, mark: str):
        self.name = input(f"🤖 : Please, enter a name for computer {mark} player : ")
        self.name = f"Computer_{mark}" if not (self.name) else self.name
        self.mark = mark

    def move(self, board: object, game: object):
        """
        Makes the computer player move intelligently by evaluating the board.

        Parameters:
            board: From Board class, the board on which we play.
            game: Current game instance (if needed for more advanced strategies).
        """
        print(f"🤖 : It's computer {self.name} turn.\n")
        print(f"🤖 : Let's place '{self.mark}' !\n")

        # Step 1: Try to win
        winning_move = self.find_winning_move(board, game)
        if winning_move:
            col = winning_move
            board.update_board(col, self.mark)
            return

        # Step 2: Block opponent from winning
        blocking_move = self.find_blocking_move(board, game)
        if blocking_move:
            col = blocking_move
            board.update_board(col, self.mark)
            return

        # Step 3: Play strategically (e.g., pick center, then corners)
        strategic_move = self.find_best_move(board, game)
        if strategic_move != None:
            col = strategic_move
            board.update_board(col, self.mark)
            return

    def find_winning_move(self, board: object, game: object):
        """
        Check if there's a move that would make the computer win.

        Parameters:
            board: The current game board.
            game: Current game instance (if needed for more advanced strategies).

        Returns:
            int: The col of the winning move or None.
        """
        return self.find_best_move_for_player(board, game, self.mark)

    def find_blocking_move(self, board: object, game: object):
        """
        Check if there's a move that would block the opponent from winning.

        Parameters:
            board: The current game board.
            game: Current game instance (if needed for more advanced strategies).

        Returns:
            int: The col of the blocking move or None.
        """
        opponent_mark = "O" if self.mark == "X" else "X"
        return self.find_best_move_for_player(board, game, opponent_mark)

    def find_best_move_for_player(self, board: object, game: object, player_mark: str):
        """
        Check all possible winning conditions and find the best move for a player.

        Parameters:
            board: The current game board.
            game: Current game instance (if needed for more advanced strategies).
            player_mark: The player's mark ('X' or 'O').

        Returns:
            int: The (row, col) for the best move or None.
        """
        for condition in game.generate_winning_conditions():
            line = [board.board[pos] for pos in condition]
            if line.count(player_mark) == game.n - 1 and line.count(" ") == 1:
                col = condition[line.index(" ")][1]
                row = condition[line.index(" ")][0]
                # Check if all positions below the intended row are filled (i.e., not empty)
                if all(
                    board.board[i, col] != " " for i in range(board.row - 1, row, -1)
                ):
                    return col
        return None

    def find_best_move(self, board: object, game: object):
        """
        If no winning or blocking move, pick a strategic move.

        Parameters:
            board: The current game board.
            game: Current game instance (if needed for more advanced strategies).

        Returns:
            int: The col of the best move.
        """
        # Strategy: prioritize center, then corners, then random.
        center = board.column // 2
        if board.is_move_available(center):
            return center

        corners = [0, board.column - 1]
        for corner in corners:
            if board.is_move_available(corner):
                return corner

        # Otherwise, return a random available move
        available_columns = [
            col for col in range(board.column) if board.is_move_available(col)
        ]
        if available_columns:
            return random.choice(available_columns)
        return None


class Board:
    """
    Defines the board characteristics.
    """

    def __init__(self):
        while True:
            try:
                self.row = int(
                    input("🤖 : Please, enter the number of rows of the board : ")
                )
                self.column = int(
                    input("🤖 : Please, enter the rumber of columns of the board : ")
                )
                if self.row > 4 and self.column > 4:
                    break
                else:
                    print(
                        "❌❌ Invalid input! Board dimensions must be at least 5x5 ❌❌\n"
                    )
            except ValueError:
                print("❌❌ Invalid input! ❌❌\n🤖 : Please enter an integer value.\n")
        self.board = np.array(
            [[" " for _ in range(self.column)] for _ in range(self.row)]
        )
        self.available_moves = self.get_available_moves()

    def get_available_moves(self):
        """
        Returns a list of column indices where a move can be made.
        """
        return [col for col in range(self.column) if self.is_move_available(col)]

    def print_board_with_borders(self):
        """
        Prints a board with '|' symbols to separate columns, and '-' to separate row.
        """
        print("\n")

        # Placing "column" in the middle of the row length
        if self.column % 2 == 1:
            print(" " * (self.column // 2 * 4) + "column")
        else:
            print(" " * ((self.column // 2 * 4) - 2) + "column")

        # Removing one space between numbers to help formatting if board size too big.
        column_index = "  "
        for index in range(self.column):
            if index > 99:
                column_index += f"{index} "
            elif index > 9:
                column_index += f"{index}  "
            else:
                column_index += f"{index}   "
        print(column_index)

        print("-" * ((self.column * 4) + 1))

        for _, row in enumerate(self.board):
            # Adding | as column sep.
            print("| " + " | ".join(row) + f" |")
            print("-" * ((self.column * 4) + 1))

        print("\n")

    def is_move_available(self, col: int):
        """
        Checks if the player move is available.

        Returns:
            True if the move is available else False.
        """
        return self.board[0][col] == " "

    def update_board(self, col: int, mark: str):
        """
        Updates the board with the player's mark in the specified column.
        The mark will be placed in the lowest available row of the column.
        """
        for row in range(self.row - 1, -1, -1):
            if self.board[row][col] == " ":
                self.board[row][col] = mark
                self.available_moves = self.get_available_moves()
                break


class Game:
    """
    Defines the game flow.
    """

    def __init__(self):
        self.game_opening()
        self.board = Board()
        while True:
            try:
                self.n = int(
                    input(
                        "🤖 : Please, enter the number of marks you need to align to win : "
                    )
                )
                if self.n >= 3 and self.n <= self.board.row:
                    break
                else:
                    print(
                        f"❌❌ Invalid input! you should pick a number greater than 3 and inferior or equal to {self.board.row} ❌❌\n"
                    )
            except ValueError:
                print("❌❌ Invalid input! ❌❌\n🤖 : Please enter an integer value.\n")
        self.winning_conditions = self.generate_winning_conditions()

    def game_opening(self):
        print(
            f"""
          {"_"*135}

          Hello Everyone !! 

          I'm AI KF23 🤖, your bot host for this connect-4 game.
          Let me walk you through the rules ✨ :

          - First, you'll need to choose the size of the board (number of rows and columns).
            You can select any integer, but keep in mind :
                a- Rows and columns length should be greater than 4 ❗
                b- Try to avoid very large numbers to prevent formatting issues and overly long games ❗

          - Right after you'll have to select the number of marks you need to align to win.
                - Remember to keep your number between 3 and number of rows - 1 ❗❗          

          - Next, you'll pick the players: either yourself or a CPU that I've trained myself 🤖.
            Trust me, my bots are REALLY tough to beat, but you're welcome to give it your best shot!

          - The first player will always use the "X" mark by default and the second one will use 'O', so choose carefully❗

          - To place your mark you'll need to choose the column index and your mark will fall down to an available place.
                - Obviously, if the column is full you can't place anymore marks.

          - The game ends when:
                a- There's a winner (n marks aligned), or 
                b- The game ends in a tie (no more winning moves).

          ✨ **Get ready to test your strategy and luck!** ✨ 
          Whether you're going solo, teaming up, or competing against the AI, let's see who dominates the board 🏆!

          Let's dive in !
          {"_"*135}
        """
        )

    def generate_winning_conditions(self):
        """
        Get all winning conditions.

        Returns
            winning_conditions (list): list of all winning conditions.
        """
        winning_conditions = []

        # Horizontal
        for row in range(self.board.row):
            for col in range((self.board.column - (self.n - 1))):
                winning_conditions.append([(row, col + i) for i in range(self.n)])

        # Vertical
        for col in range(self.board.column):
            for row in range((self.board.row - (self.n - 1))):
                winning_conditions.append([(row + i, col) for i in range(self.n)])

        # Diagonal (top-left to bottom-right)
        for row in range((self.board.row - (self.n - 1))):
            for col in range((self.board.column - (self.n - 1))):
                winning_conditions.append([(row + i, col + i) for i in range(self.n)])

        # Diagonal (bottom-left to top-right)
        for row in range((self.n - 1), self.board.row):
            for col in range((self.board.column - (self.n - 1))):
                winning_conditions.append([(row - i, col + i) for i in range(self.n)])

        return winning_conditions

    def update_winning_conditions(self):
        """
        Updates the list of possible winning conditions by removing impossible ones.
        A condition is impossible if both 'X' and 'O' are present in the same line.
        """
        new_conditions = []
        for condition in self.winning_conditions:
            line = [self.board.board[row, col] for row, col in condition]
            if not (
                "X" in line and "O" in line
            ):  # Both players' marks make the condition impossible
                new_conditions.append(condition)
        self.winning_conditions = new_conditions

    def check_winning(self, current_player):
        """
        Check at each move if there's a winner.

        Returns:
            True: If there's a winning condition matched else False.
        """
        for condition in self.winning_conditions:
            marks = [self.board.board[row, col] for row, col in condition]
            if marks == ["X"] * (self.n) or marks == ["O"] * (self.n):
                print(
                    f"🤖 : A winning position for {current_player} has been found at position : {condition}."
                )
                return True

        return False

    def is_tie(self):
        """
        Define if there's a tie.

        Returns:
            True: If the board is full else False.
        """
        return len(self.board.available_moves) == 0 or len(self.winning_conditions) == 0
    
    def restart_game(self):
        """
        Ask the players if they want to restart the game.
        Resets the game if they choose to continue.
        """
        while True:
            response = input("🤖 : Do you want to play again? (y/n): ").lower().strip()
            if response == "y":
                print("🤖 : Starting a new game!\n")
                self.__init__()
                self.play()
                break
            elif response == "n":
                print("\n🤖 : Thanks for playing! Goodbye!")
                break
            else:
                print("❌❌ Invalid input! ❌❌\n🤖 : Please enter 'y' or 'n'.")

    def play(self):
        """
        Set the game flow.
        """
        info_X = input(
            "🤖 : Please enter 'cpu' if you want a computer to place 'X' : "
        ).lower()
        player_X = ComputerPlayer("X") if info_X == "cpu" else Player("X")

        info_O = input(
            "🤖 : Please enter 'cpu' if you want a computer to place 'O' : "
        ).lower()
        player_O = ComputerPlayer("O") if info_O == "cpu" else Player("O")

        current_player = player_X

        while True:
            self.board.print_board_with_borders()
            current_player.move(self.board, self)

            self.update_winning_conditions()

            if self.check_winning(current_player.name):
                self.board.print_board_with_borders()
                print(f"🤖 : Congratulations {current_player.name}, you win! ✨")
                break

            if self.is_tie():
                self.board.print_board_with_borders()
                print("🤖 : It's a tie !")
                break

            # Switch players
            current_player = player_O if current_player == player_X else player_X

        self.restart_game()


if __name__ == "__main__":
    game = Game()
    game.play()
