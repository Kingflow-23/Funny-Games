# Sudoku Game

This is a Python-based **Sudoku Game** developed using the **Pygame library**. The game allows users to play Sudoku, input numbers, delete numbers, and check for a valid solution. It features randomly generated Sudoku puzzles and a user-friendly interface.

---

## Features

- **Dynamic Puzzle Generation**:
  - The game generates a complete valid Sudoku grid.
  - A random number of cells (between 35 to 45) are removed to create a puzzle.

- **User Interaction**:
  - Click to select cells.
  - Input numbers (1-9) using the keyboard.
  - Delete numbers using the **Backspace** key.

- **Validation**:
  - Checks if the Sudoku puzzle is solved correctly.
  - Displays a victory message for successful completion.
  - Shows an invalid input message if the solution is incorrect.

- **Reset Options**:
  - Reset the current board to its initial state by pressing **'R'**.
  - Restart the game with a new puzzle by pressing **'Enter'**.

- **Show Solution**:
  - Toggle between the current board and the solution by pressing **'S'**.

- **Keyboard Navigation**:
  - Use arrow keys (**Up, Down, Left, Right**) to navigate between cells.

---

## How to Run

1. **Install Python**: Ensure Python 3.8+ is installed on your system.
2. **Install Pygame**: Install the Pygame library by running:

   ```bash
   pip install pygame
   ```
3. Run the Game: 
    ```bash
    python sudoku_ui.py
    ```

## Controls

| Key            | Action                                     |
|-----------------|-------------------------------------------|
| Mouse Click     | Select a cell.                           |
| Arrow Keys      | Move between cells.                      |
| 1-9             | Input a number in the selected cell.     |
| Backspace       | Delete the number from the selected cell. |
| Enter           | Restart the game with a new puzzle.      |
| R               | Reset the board to its initial state.    |
| S               | Toggle between the solution and puzzle.  |

---

## Game Rules

1. Each row, column, and 3x3 sub-grid must contain all numbers from 1 to 9 without repetition.
2. Pre-filled numbers cannot be changed by the user.
3. The game is won when all cells are correctly filled.

---

## Victory and Error Messages

- **Victory Message**:
  - Displays "Congratulations! You've completed the puzzle!" when the game is successfully completed.
  
- **Invalid Input Message**:
  - Displays "Invalid inputs! Please try again." if the puzzle is filled incorrectly.

---

## Dependencies

- **Python 3.8+** I used Python 3.10.11 for this project.
- **Pygame**

Install dependencies using:
```bash
pip install -r requirements.txt
```
