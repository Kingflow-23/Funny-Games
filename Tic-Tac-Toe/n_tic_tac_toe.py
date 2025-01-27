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
            game: Current game instance.
        """
        while True:
            try:
                print(f"🤖 : It's {self.name} turn.\n")
                print(f"🤖 : Let's place '{self.mark}' !\n")
                row = int(
                    input(f"🤖 : {self.name}, enter the row (0-{board.size-1}): ")
                )
                col = int(
                    input(f"🤖 : {self.name}, enter the column (0-{board.size-1}): ")
                )

                if board.is_move_available(row, col):
                    print(f"🤖 : {self.name} placed {self.mark} at {(row, col)}.")
                    board.update_board(row, col, self.mark)
                    break
                else:
                    print(
                        "\n❌❌ That position is already taken or out of bounds !! ❌❌\n🤖 : Try again.\n"
                    )
                    board.print_board_with_borders()
            except ValueError:
                print(
                    f"❌❌ Invalid input !! ❌❌\n🤖 : Please enter a number between 0 and {board.size-1}.\n"
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
            game: Current game instance.
        """
        print(f"🤖 : It's {self.name} turn.\n")
        print(f"🤖 : Let's place '{self.mark}' !\n")

        # Step 1: Try to win
        winning_move = self.find_winning_move(board, game)
        if winning_move:
            print(f"🤖 : {self.name} decided to attack !")
            row, col = winning_move
            print(f"🤖 : {self.name} placed {self.mark} at {(row, col)}.")
            board.update_board(row, col, self.mark)
            return

        # Step 2: Block opponent from winning
        blocking_move = self.find_blocking_move(board, game)
        if blocking_move:
            print(f"🤖 : {self.name} blocked you from winning easily !")
            row, col = blocking_move
            print(f"🤖 : {self.name} placed {self.mark} at {(row, col)}.")
            board.update_board(row, col, self.mark)
            return

        # Step 3: Block opponent's fork
        blocking_fork_move = self.find_blocking_fork_move(board, game)
        if blocking_fork_move:
            print(f"🤖 : {self.name} blocked a great move you could've done !")
            row, col = blocking_fork_move
            print(f"🤖 : {self.name} placed {self.mark} at {(row, col)}.")
            board.update_board(row, col, self.mark)
            return

        # Step 4: Try to create a fork
        fork_move = self.find_fork_move(board, game)
        if fork_move:
            print(f"🤖 : {self.name} trying a tricky move !")
            row, col = fork_move
            print(f"🤖 : {self.name} placed {self.mark} at {(row, col)}.")
            board.update_board(row, col, self.mark)
            return

        # Step 5: Play strategically (e.g., pick center, then corners)
        strategic_move = self.find_best_move(board)
        if strategic_move:
            print(f"🤖 : {self.name} did a classic, but great move !")
            row, col = strategic_move
            print(f"🤖 : {self.name} placed {self.mark} at {(row, col)}.")
            board.update_board(row, col, self.mark)
            return

    def find_winning_move(self, board: object, game: object):
        """
        Check if there's a move that would make the computer win.

        Parameters:
            board: The current game board.
            game: Current game instance.

        Returns:
            tuple: The (row, col) of the winning move or None.
        """
        return self.find_best_move_for_player(board, game, self.mark)

    def find_blocking_move(self, board: object, game: object):
        """
        Check if there's a move that would block the opponent from winning.

        Parameters:
            board: The current game board.
            game: Current game instance.

        Returns:
            tuple: The (row, col) of the blocking move or None.
        """
        opponent_mark = "O" if self.mark == "X" else "X"
        return self.find_best_move_for_player(board, game, opponent_mark)

    def find_best_move_for_player(self, board: object, game: object, player_mark: str):
        """
        Check all possible winning conditions and find the best move for a player.

        Parameters:
            board: The current game board.
            game: Current game instance.
            player_mark: The player's mark ('X' or 'O').

        Returns:
            tuple: The (row, col) for the best move or None.
        """
        for condition in game.generate_winning_conditions():
            line = [board.board[pos] for pos in condition]
            if line.count(player_mark) == (game.n - 1) and line.count(" ") == 1:
                empty_spot = condition[line.index(" ")]
                return empty_spot
        return None

    def find_fork_move(self, board: object, game: object):
        """
        Check if there's a move that would create a fork for the computer player.

        Parameters:
            board: The current game board.
            game: Current game instance.

        Returns:
            tuple: The (row, col) of the fork move or None.
        """
        for move in board.available_moves[:]:
            row, col = move

            # Step 1: Temporarily place the computer's mark
            board.update_board(row, col, self.mark)

            # Step 2: Check how many winning paths are available after this move
            winning_paths = self.count_winning_paths(board, game, self.mark)

            # Step 3: If this move creates a fork, undo the move and return it
            if winning_paths >= 2:
                board.update_board(row, col, " ", is_undo=True)
                return row, col

            # Step 4: If not a fork, still undo the move
            board.update_board(row, col, " ", is_undo=True)

        return None

    def find_blocking_fork_move(self, board: object, game: object):
        """
        Check if the opponent can create a fork and block it.

        Parameters:
            board: The current game board.
            game: Current game instance.

        Returns:
            tuple: The (row, col) to block the fork or None if no fork is detected.
        """
        opponent_mark = "O" if self.mark == "X" else "X"

        for move in board.available_moves[:]:
            row, col = move

            # Step 1: Simulate opponent's move
            board.update_board(row, col, opponent_mark)

            # Step 2: Check if this move creates a fork for the opponent
            opponent_winning_paths = self.count_winning_paths(
                board, game, opponent_mark
            )
            if opponent_winning_paths >= 2:
                # Undo the move and return this move to block the fork
                board.update_board(row, col, " ", is_undo=True)
                return row, col

            # Step 3: Undo the move if it doesn't create a fork
            board.update_board(row, col, " ", is_undo=True)

        return None

    def count_winning_paths(self, board: object, game: object, player_mark: str):
        """
        Count how many winning paths are available for the player after a hypothetical move.

        Parameters:
            board: The current game board.
            game: Current game instance.
            player_mark: The player's mark ('X' or 'O').

        Returns:
            int: The number of winning paths.
        """
        winning_paths = 0
        for condition in game.generate_winning_conditions():
            line = [board.board[pos] for pos in condition]
            if line.count(player_mark) == (game.n - 1) and line.count(" ") == 1:
                winning_paths += 1
        return winning_paths

    def find_best_move(self, board: object):
        """
        If no winning or blocking move, pick a strategic move.

        Parameters:
            board: The current game board.

        Returns:
            tuple: The (row, col) of the best move or None.
        """
        # Strategy: prioritize center, then corners, then edges
        center = (board.size // 2, board.size // 2)
        if center in board.available_moves:
            return center

        corners = [
            (0, 0),
            (0, board.size - 1),
            (board.size - 1, 0),
            (board.size - 1, board.size - 1),
        ]
        for corner in corners:
            if corner in board.available_moves:
                return corner

        # Otherwise, return a random available move
        return random.choice(board.available_moves)


class Board:
    """
    Defines the board characteristics.
    """

    def __init__(self):
        while True:
            try:
                self.size = int(input("🤖 : Please, enter the size of the board : "))
                if self.size > 2:
                    break
                else:
                    print(
                        "❌❌ Invalid input! Board dimensions must be at least 3x3 ❌❌\n"
                    )
            except ValueError:
                print("❌❌ Invalid input! ❌❌\n🤖 : Please enter an integer value.\n")
        self.board = np.array(
            [[" " for _ in range(self.size)] for _ in range(self.size)]
        )
        self.available_moves = list(
            (i, j) for i in range(self.size) for j in range(self.size)
        )

    def print_board_with_borders(self):
        """
        Prints a board with '|' symbols to separate columns, and '-' to separate row.
        """

        print("\n")

        # Placing "column" in the middle of the row length
        if self.size % 2 == 1:
            print(" " * (self.size // 2 * 4) + "column")
        else:
            print(" " * ((self.size // 2 * 4) - 2) + "column")

        # Removing one space between numbers to help formatting if board size too big.
        column_index = "  "
        for index in range(self.size):
            if index > 99:
                column_index += f"{index} "
            elif index > 9:
                column_index += f"{index}  "
            else:
                column_index += f"{index}   "
        print(column_index)

        print("-" * ((self.size * 4) + 1))

        for i, row in enumerate(self.board):
            # Adding | as column sep.
            if self.size % 2 == 1 and i == self.size // 2:
                print("| " + " | ".join(row) + f" | {i} row")
            else:
                print("| " + " | ".join(row) + f" | {i}")

            # Adding - as row sep.
            if self.size % 2 == 0 and i == (int(self.size / 2) - 1):
                print("-" * ((self.size * 4) + 1) + "    row")
            else:
                print("-" * ((self.size * 4) + 1))

        print("\n")

    def is_move_available(self, row: int, col: int):
        """
        Checks if the player move is available.

        Returns:
            True if the move is available else False.
        """
        return (row, col) in self.available_moves

    def update_board(self, row: int, col: int, mark: str, is_undo=False):
        """
        Update the board with the place mark, or undo the move by re-adding it to available moves.

        Parameters:
            row (int): The row number.
            col (int): The column number.
            mark (str): The mark to place ('X', 'O', or ' ').
            is_undo (bool): If True, it will undo the move and add the move back to available moves.
        """
        self.board[row, col] = mark

        if is_undo:
            # Add the move back to available_moves
            if (row, col) not in self.available_moves:
                self.available_moves.append((row, col))
        else:
            # Remove the move from available_moves
            if (row, col) in self.available_moves:
                self.available_moves.remove((row, col))


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
                if self.n >= 3 and self.n <= self.board.size:
                    break
                else:
                    print(
                        f"❌❌ Invalid input! you should pick a number greater than 2 and inferior or equal to {self.board.size} ❌❌\n"
                    )
            except ValueError:
                print("❌❌ Invalid input! ❌❌\n🤖 : Please enter an integer value.\n")
        self.winning_conditions = self.generate_winning_conditions()

    def game_opening(self):
        print(
            f"""
          {"_"*135}

          Hello Everyone !! 
          
          I'm AI KF23 🤖, your bot host for this tic-tac-toe game.
          Let me walk you through the rules ✨ :

          - First, you'll need to choose the size of the board and the number of marks you need to align to win.
            You can select any integer, but keep in mind :
                a- You only need to enter the size 'n' (not n*n ❗) with n>2.
                b- Try to avoid very large numbers to prevent formatting issues and overly long games ❗
                c-  The number of marks you need to align to win should be greater than 2 and
                    inferior or equal to the size of the board.

          - Next, you'll pick the players: either yourself or a CPU that I've trained myself 🤖.
            Trust me, my bots are REALLY tough to beat, but you're welcome to give it your best shot!

          - The first player will always use the "X" mark by default and the second one will use 'O', so choose carefully❗

          - Obviously, you can't place your mark on a spot already taken 🤖.

          - The game ends when:
                a- There's a winner (n marks aligned), or 
                b- The game ends in a tie (no more winning moves or moves available).

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
        for row in range(self.board.size):
            for col in range((self.board.size - (self.n - 1))):
                winning_conditions.append([(row, col + i) for i in range(self.n)])

        # Vertical
        for col in range(self.board.size):
            for row in range((self.board.size - (self.n - 1))):
                winning_conditions.append([(row + i, col) for i in range(self.n)])

        # Diagonal (top-left to bottom-right)
        for row in range((self.board.size - (self.n - 1))):
            for col in range((self.board.size - (self.n - 1))):
                winning_conditions.append([(row + i, col + i) for i in range(self.n)])

        # Diagonal (bottom-left to top-right)
        for row in range((self.n - 1), self.board.size):
            for col in range((self.board.size - (self.n - 1))):
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

    def check_winning(self, current_player: str):
        """
        Check at each move if there's a winner.

        Parameters:
            current_player : current player name.

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
        Set the game flow
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
