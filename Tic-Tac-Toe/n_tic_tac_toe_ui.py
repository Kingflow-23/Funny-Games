import sys
import pygame
import random
import numpy as np

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
BUTTON_COLOR = (255, 255, 255)
BUTTON_HOVER_COLOR = (200, 200, 200)
TEXT_COLOR = (0, 0, 0)

# Fonts
FONT = pygame.font.Font(None, 50)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)

# Board
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# Game Mode
game_mode = None  # 'human' or 'computer'
player = 1  # Current player (1 for circle, 2 for cross)


# Functions
def draw_lines():
    """Draws the grid lines on the board."""
    # Horizontal lines
    pygame.draw.line(
        screen, LINE_COLOR, (0, HEIGHT // 3), (WIDTH, HEIGHT // 3), LINE_WIDTH
    )
    pygame.draw.line(
        screen, LINE_COLOR, (0, 2 * HEIGHT // 3), (WIDTH, 2 * HEIGHT // 3), LINE_WIDTH
    )

    # Vertical lines
    pygame.draw.line(
        screen, LINE_COLOR, (WIDTH // 3, 0), (WIDTH // 3, HEIGHT), LINE_WIDTH
    )
    pygame.draw.line(
        screen, LINE_COLOR, (2 * WIDTH // 3, 0), (2 * WIDTH // 3, HEIGHT), LINE_WIDTH
    )


def draw_figures():
    """Draws Xs and Os on the board based on the board state."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                # Draw circle
                pygame.draw.circle(
                    screen,
                    CIRCLE_COLOR,
                    (
                        int(col * WIDTH // 3 + WIDTH // 6),
                        int(row * HEIGHT // 3 + HEIGHT // 6),
                    ),
                    CIRCLE_RADIUS,
                    CIRCLE_WIDTH,
                )
            elif board[row][col] == 2:
                # Draw cross
                pygame.draw.line(
                    screen,
                    CROSS_COLOR,
                    (col * WIDTH // 3 + SPACE, row * HEIGHT // 3 + SPACE),
                    (
                        col * WIDTH // 3 + WIDTH // 3 - SPACE,
                        row * HEIGHT // 3 + HEIGHT // 3 - SPACE,
                    ),
                    CROSS_WIDTH,
                )
                pygame.draw.line(
                    screen,
                    CROSS_COLOR,
                    (col * WIDTH // 3 + SPACE, row * HEIGHT // 3 + HEIGHT // 3 - SPACE),
                    (col * WIDTH // 3 + WIDTH // 3 - SPACE, row * HEIGHT // 3 + SPACE),
                    CROSS_WIDTH,
                )


def draw_buttons():
    """Draws buttons for selecting the game mode."""
    human_button = pygame.Rect(WIDTH // 4 - 100, HEIGHT // 2 - 50, 200, 100)
    computer_button = pygame.Rect(3 * WIDTH // 4 - 100, HEIGHT // 2 - 50, 200, 100)

    # Draw human button
    pygame.draw.rect(screen, BUTTON_COLOR, human_button)
    human_text = FONT.render("Human", True, TEXT_COLOR)
    screen.blit(human_text, (human_button.x + 40, human_button.y + 25))

    # Draw computer button
    pygame.draw.rect(screen, BUTTON_COLOR, computer_button)
    computer_text = FONT.render("Computer", True, TEXT_COLOR)
    screen.blit(computer_text, (computer_button.x + 10, computer_button.y + 25))

    return human_button, computer_button


def mark_square(row, col, player):
    """Marks a square with the player's move."""
    board[row][col] = player


def available_square(row, col):
    """Checks if a square is available."""
    return board[row][col] == 0


def is_board_full():
    """Checks if the board is full."""
    return not np.any(board == 0)


def check_win(player, draw_winning_line=True):
    """Checks if the given player has won the game."""
    # Vertical win
    for col in range(BOARD_COLS):
        if (
            board[0][col] == player
            and board[1][col] == player
            and board[2][col] == player
        ):
            if draw_winning_line:
                draw_vertical_winning_line(col, player)
            return True

    # Horizontal win
    for row in range(BOARD_ROWS):
        if (
            board[row][0] == player
            and board[row][1] == player
            and board[row][2] == player
        ):
            if draw_winning_line:
                draw_horizontal_winning_line(row, player)
            return True

    # Ascending diagonal win
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        if draw_winning_line:
            draw_ascending_diagonal(player)
        return True

    # Descending diagonal win
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        if draw_winning_line:
            draw_descending_diagonal(player)
        return True

    return False


def draw_vertical_winning_line(col, player):
    """Draws a vertical line for the winning move."""
    posX = col * WIDTH // 3 + WIDTH // 6
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 15), LINE_WIDTH)


def draw_horizontal_winning_line(row, player):
    """Draws a horizontal line for the winning move."""
    posY = row * HEIGHT // 3 + HEIGHT // 6
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), LINE_WIDTH)


def draw_ascending_diagonal(player):
    """Draws a diagonal line from bottom-left to top-right for the winning move."""
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), LINE_WIDTH)


def draw_descending_diagonal(player):
    """Draws a diagonal line from top-left to bottom-right for the winning move."""
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), LINE_WIDTH)


def restart():
    """Restarts the game by resetting the board."""
    global player
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0
    player = 1


def computer_move(player):
    """
    Makes the computer player move intelligently by evaluating the board.

    Parameters:
        board: From Board class, the board on which we play.
    """
    # Step 1: Try to win
    winning_move = find_winning_move(board, player)
    if winning_move:
        row, col = winning_move
        return (row, col)

    # Step 2: Block opponent from winning
    blocking_move = find_blocking_move(board, player)
    if blocking_move:
        row, col = blocking_move
        return (row, col)

    # Step 3: Block opponent's fork
    blocking_fork_move = find_blocking_fork_move(board, player)
    if blocking_fork_move:
        row, col = blocking_fork_move
        return (row, col)

    # Step 4: Try to create a fork
    fork_move = find_fork_move(board, player)
    if fork_move:
        row, col = fork_move
        return (row, col)

    # Step 5: Play strategically (e.g., pick center, then corners)
    strategic_move = find_best_move(board)
    if strategic_move:
        row, col = strategic_move
        return (row, col)


def find_winning_move(board, player):
    """Finds a winning move for the computer player."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = player  # Simulate a move
                if check_win(player, draw_winning_line=False):
                    board[row][col] = 0
                    return (row, col)
                board[row][col] = 0
    return None


def find_blocking_move(board, player):
    """Finds a move that blocks the opponent from winning."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 3 - player  # Simulate a move
                if check_win(3 - player, draw_winning_line=False):
                    board[row][col] = 0
                    return (row, col)
                board[row][col] = 0


def check_fork(player):
    """Checks if placing a mark creates a fork for the player."""
    fork_count = 0

    # Loop through all empty squares
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:  # If the square is empty
                board[row][col] = player  # Simulate the move
                winning_lines = count_winning_lines(
                    board, player
                )  # Count possible wins
                if (
                    winning_lines > 1
                ):  # A fork occurs if two or more winning lines are created
                    fork_count += 1
                board[row][col] = 0  # Undo the move

    return fork_count > 0


def count_winning_lines(board, player):
    """Counts the number of potential winning lines for the player."""
    winning_lines = 0

    # Check rows and columns
    for i in range(BOARD_ROWS):
        if np.sum(board[i, :] == player) == 2 and np.sum(board[i, :] == 0) == 1:
            winning_lines += 1
        if np.sum(board[:, i] == player) == 2 and np.sum(board[:, i] == 0) == 1:
            winning_lines += 1

    # Check diagonals
    main_diag = [board[i, i] for i in range(BOARD_ROWS)]
    anti_diag = [board[i, BOARD_COLS - i - 1] for i in range(BOARD_ROWS)]
    if (
        np.sum(np.array(main_diag) == player) == 2
        and np.sum(np.array(main_diag) == 0) == 1
    ):
        winning_lines += 1
    if (
        np.sum(np.array(anti_diag) == player) == 2
        and np.sum(np.array(anti_diag) == 0) == 1
    ):
        winning_lines += 1

    return winning_lines


def find_blocking_fork_move(board, player):
    """Finds a move that blocks the opponent's fork."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 3 - player  # Simulate a move
                if check_fork(3 - player):
                    board[row][col] = 0
                    return (row, col)
                board[row][col] = 0
    return None


def find_fork_move(board, player):
    """Finds a move that creates a fork for the computer player."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = player  # Simulate a move
                if check_fork(player):
                    board[row][col] = 0
                    return (row, col)
                board[row][col] = 0
    return None


def find_best_move(board):
    """Finds the best move for the computer player."""
    # Play center if available
    if board[1][1] == 0:
        return (1, 1)

    # Play a corner if available
    for move in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        if board[move[0]][move[1]] == 0:
            return move

    # Play a side if available
    for move in [(0, 1), (1, 0), (1, 2), (2, 1)]:
        if board[move[0]][move[1]] == 0:
            return move


# Game loop
draw_lines()


def main():
    global player, running, game_mode
    running = True
    selecting_mode = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if selecting_mode:
                screen.fill(BG_COLOR)
                human_button, computer_button = draw_buttons()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = event.pos
                    if human_button.collidepoint(mouseX, mouseY):
                        game_mode = "human"
                        selecting_mode = False
                        screen.fill(BG_COLOR)
                        draw_lines()
                    elif computer_button.collidepoint(mouseX, mouseY):
                        game_mode = "computer"
                        selecting_mode = False
                        screen.fill(BG_COLOR)
                        draw_lines()

            elif not selecting_mode:
                if game_mode == "human":
                    if event.type == pygame.MOUSEBUTTONDOWN and not is_board_full():
                        mouseX = event.pos[0]  # X
                        mouseY = event.pos[1]  # Y

                        clicked_row = int(mouseY // (HEIGHT // 3))
                        clicked_col = int(mouseX // (WIDTH // 3))

                        if available_square(clicked_row, clicked_col):
                            mark_square(clicked_row, clicked_col, player)
                            if check_win(player):
                                pass
                            player = 3 - player  # Switch player

                        draw_figures()

                elif game_mode == "computer":
                    if (
                        player == 1
                        and event.type == pygame.MOUSEBUTTONDOWN
                        and not is_board_full()
                    ):
                        mouseX = event.pos[0]  # X
                        mouseY = event.pos[1]  # Y

                        clicked_row = int(mouseY // (HEIGHT // 3))
                        clicked_col = int(mouseX // (WIDTH // 3))

                        if available_square(clicked_row, clicked_col):
                            mark_square(clicked_row, clicked_col, player)
                            if check_win(player):
                                pass
                            player = 3 - player  # Switch player

                        draw_figures()

                    elif player == 2 and not is_board_full():
                        pygame.time.wait(500)  # Add a delay for realism
                        row, col = computer_move(player)
                        mark_square(row, col, player)
                        if check_win(player):
                            pass
                        player = 3 - player  # Switch player

                        draw_figures()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Enter key to restart
                        restart()
                    elif event.key == pygame.K_BACKSPACE:  # Backspace key to quit
                        pygame.quit()
                        quit()

            pygame.display.update()


if __name__ == "__main__":
    main()
