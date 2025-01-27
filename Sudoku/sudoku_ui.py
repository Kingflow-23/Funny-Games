import sys
import copy
import random
import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 720, 720
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE
LINE_WIDTH = 2
FONT = pygame.font.SysFont("Arial", 40)
VICTORY_FONT = pygame.font.SysFont("Arial", 40)
INVALID_FONT = pygame.font.SysFont("Arial", 40)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (0, 0, 0)
SELECTED_COLOR = (173, 216, 230)  # Light Blue
HIGHLIGHT_COLOR = (255, 223, 186)  # Light Yellow
INVALID_COLOR = (255, 100, 100)  # Red for invalid input
INPUT_COLOR = (0, 0, 255)  # Blue color for user input numbers
TEXT_COLOR = (0, 0, 0)

# Sudoku grid placeholder
board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # Empty grid
initial_board = [
    [0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)
]  # Initial numbers board for reference

# Create a window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Game")


def draw_grid():
    """
    Draws the grid on the screen. The grid consists of horizontal and vertical lines,
    with thicker lines for the 3x3 sub-grids to visually separate them.
    """
    for i in range(GRID_SIZE):
        # Draw thick lines for 3x3 sub-grids
        if i % 3 == 0:
            line_width = 4
        else:
            line_width = 1
        pygame.draw.line(
            screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), line_width
        )
        pygame.draw.line(
            screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), line_width
        )


def draw_numbers():
    """
    Draws the numbers on the grid. Numbers in the initial board are black,
    and numbers input by the player are blue.
    """
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            num = board[row][col]
            if num != 0:
                # If the number is an initial number, render it in black
                if initial_board[row][col] != 0:
                    text = FONT.render(str(num), True, BLACK)
                else:  # User-inputted number, render it in blue
                    text = FONT.render(str(num), True, INPUT_COLOR)

                # Center the text in the cell
                text_rect = text.get_rect(
                    center=(
                        col * CELL_SIZE + CELL_SIZE // 2,
                        row * CELL_SIZE + CELL_SIZE // 2,
                    )
                )
                screen.blit(text, text_rect)


def draw_selected_cell(x, y):
    """
    Highlights the selected cell by drawing a light blue rectangle around it.

    Args:
        x (int): The column index of the selected cell.
        y (int): The row index of the selected cell.
    """
    pygame.draw.rect(
        screen, SELECTED_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 4
    )


def is_valid(board, row, col, num):
    """
    Checks if placing a number in a given row and column is valid.
    A number is valid if it does not already appear in the same row, column, or 3x3 sub-grid.

    Args:
        board (list): The current state of the Sudoku grid.
        row (int): The row index of the cell to check.
        col (int): The column index of the cell to check.
        num (int): The number to check for validity.

    Returns:
        bool: True if the number is valid, False otherwise.
    """
    # Check row and column for duplicates
    for i in range(GRID_SIZE):
        if board[row][i] == num and i != col:
            return False
        if board[i][col] == num and i != row:
            return False

    # Check 3x3 sub-grid for duplicates
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num and (
                start_row + i != row and start_col + j != col
            ):
                return False
    return True


def generate_complete_board():
    """
    Generates a valid, completely filled Sudoku grid using backtracking.
    The function tries to place numbers from 1 to 9 in each empty cell. If it encounters a conflict,
    it backtracks and tries a different number until the entire grid is filled.
    """

    def backtrack(board):
        """
        The recursive backtracking helper function that tries to fill the board.

        Args:
            board (list): The current state of the Sudoku grid.

        Returns:
            bool: True if a valid solution is found, False if no valid solution exists.
        """
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] == 0:  # Find an empty cell
                    random_numbers = random.sample(
                        range(1, 10), 9
                    )  # Randomize numbers 1-9
                    for num in random_numbers:
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            if backtrack(board):
                                return True
                            board[row][col] = 0  # Backtrack if no solution is found
                    return False
        return True

    # Start the backtracking algorithm
    backtrack(board)


def remove_numbers():
    """
    Removes a random number of cells from the complete board to create a Sudoku puzzle.
    The number of cells to remove is chosen randomly between 35 and 45 to balance the difficulty.
    """
    num_cells_to_remove = random.randint(
        35, 45
    )  # Remove a random number of cells (35-45)
    cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)]
    random.shuffle(cells)

    # Set the selected cells to zero, making them empty
    for r, c in cells[:num_cells_to_remove]:
        board[r][c] = 0


def reset_board():
    """
    Resets the current board to the initial state.
    """
    global board
    board = copy.deepcopy(initial_board)


def reset_game():
    """
    Clears the entire Sudoku board by setting all cells to zero.
    This effectively resets the board to its initial empty state.
    """
    global board
    board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


def is_board_full():
    """
    Checks if the Sudoku board is completely filled with numbers.
    """
    # Check if all cells are filled
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 0:
                return False  # Not all cells are filled

    return True


def there_is_invalid_input():
    """
    Checks if there is any invalid input on the board. An input is considered invalid if:

    1. There are duplicates in the same row.
    2. There are duplicates in the same column.
    3. There are duplicates in the same 3x3 sub-grid.
    """
    # Check if the board is valid (no duplicates in rows, columns, or 3x3 sub-grids)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            num = board[row][col]
            if num != 0 and initial_board[row][col] == 0:
                if not is_valid(board, row, col, num):
                    return True  # Invalid board (duplicate detected)

    return False  # The board is valid, no duplicates


def draw_victory_message():
    """
    Draws a victory message on the screen when the game is completed successfully.
    """
    text = VICTORY_FONT.render(
        "Congratulations! You've completed the puzzle!", True, (0, 255, 0)
    )
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)


def draw_invalid_message():
    """
    Draws an invalid message on the screen when the game is completed unsuccessfully.
    """
    text = INVALID_FONT.render("Invalid inputs! Please try again.", True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)


def main():
    """
    The main game loop of the Sudoku game. It handles events, drawing, and user input.
    The grid is initialized with a valid Sudoku puzzle and displayed on the screen. Users can
    select cells and input numbers using the keyboard.
    """
    selected_row, selected_col = 0, 0
    selected_value = 0
    game_finished = False
    show_solution = False
    clock = pygame.time.Clock()

    # Generate a complete board and then remove numbers to create the puzzle
    generate_complete_board()
    global initial_board, answer_board, board
    answer_board = copy.deepcopy(board)
    remove_numbers()
    initial_board = copy.deepcopy(board)
    current_board = copy.deepcopy(board)

    while True:
        screen.fill(WHITE)
        draw_grid()
        draw_numbers()  # Draw the initials numbers in the cells

        if selected_row is not None and selected_col is not None and not game_finished:
            draw_selected_cell(selected_col, selected_row)

        # If the game is finished, draw the victory message
        if game_finished:
            if there_is_invalid_input():
                draw_invalid_message()
            else:
                draw_victory_message()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # Reset the game if 'Enter' is pressed
                    if event.key == pygame.K_RETURN:
                        reset_game()
                        generate_complete_board()
                        answer_board = copy.deepcopy(board)
                        remove_numbers()
                        initial_board = copy.deepcopy(board)
                        current_board = copy.deepcopy(board)
                        selected_row, selected_col = 0, 0
                        game_finished = False

                    # Delete the user-inputted number (using BACKSPACE)
                    if event.key == pygame.K_BACKSPACE:
                        # Only delete the number if the cell is not pre-filled
                        if initial_board[selected_row][selected_col] == 0:
                            board[selected_row][selected_col] = 0
                            current_board = copy.deepcopy(board)
                            game_finished = False

                    # Reset the board if 'r' is pressed
                    if event.key == pygame.K_r:
                        reset_board()
                        game_finished = False

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_finished:
                # Click event to select a cell
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if (
                        0 <= x < GRID_SIZE * CELL_SIZE
                        and 0 <= y < GRID_SIZE * CELL_SIZE
                    ):
                        selected_col, selected_row = x // CELL_SIZE, y // CELL_SIZE

                # Number key press event to input a number
                if event.type == pygame.KEYDOWN:

                    # Arrow key navigation
                    if event.key == pygame.K_UP:
                        selected_row = max(0, selected_row - 1)
                    elif event.key == pygame.K_DOWN:
                        selected_row = min(GRID_SIZE - 1, selected_row + 1)
                    elif event.key == pygame.K_LEFT:
                        selected_col = max(0, selected_col - 1)
                    elif event.key == pygame.K_RIGHT:
                        selected_col = min(GRID_SIZE - 1, selected_col + 1)

                    # Number input handling
                    if event.key == pygame.K_1:
                        selected_value = 1
                    elif event.key == pygame.K_2:
                        selected_value = 2
                    elif event.key == pygame.K_3:
                        selected_value = 3
                    elif event.key == pygame.K_4:
                        selected_value = 4
                    elif event.key == pygame.K_5:
                        selected_value = 5
                    elif event.key == pygame.K_6:
                        selected_value = 6
                    elif event.key == pygame.K_7:
                        selected_value = 7
                    elif event.key == pygame.K_8:
                        selected_value = 8
                    elif event.key == pygame.K_9:
                        selected_value = 9

                    if board[selected_row][selected_col] == 0:
                        if selected_value != 0:
                            board[selected_row][selected_col] = selected_value
                            current_board = copy.deepcopy(board)
                            if is_board_full():
                                game_finished = True
                        selected_value = 0
                    else:
                        selected_value = 0

                    # Show the answer board when 'S' is pressed (toggle)
                    if event.key == pygame.K_s:
                        # Toggle between showing the solution and the current puzzle
                        if show_solution:
                            board = copy.deepcopy(current_board)
                        else:
                            board = copy.deepcopy(answer_board)

                        # Toggle the show_solution flag
                        show_solution = not show_solution

                    # Delete the user-inputted number (using BACKSPACE)
                    if event.key == pygame.K_BACKSPACE:
                        # Only delete the number if the cell is not pre-filled
                        if initial_board[selected_row][selected_col] == 0:
                            board[selected_row][selected_col] = 0
                            current_board = copy.deepcopy(board)

                    # Reset the game if 'Enter' is pressed
                    if event.key == pygame.K_RETURN:
                        reset_game()
                        generate_complete_board()
                        answer_board = copy.deepcopy(board)
                        remove_numbers()
                        initial_board = copy.deepcopy(board)
                        current_board = copy.deepcopy(board)
                        selected_row, selected_col = 0, 0
                        game_finished = False

                    # Reset the board if 'r' is pressed
                    if event.key == pygame.K_r:
                        reset_board()

        clock.tick(30)  # Control the frame rate of the game


if __name__ == "__main__":
    main()
