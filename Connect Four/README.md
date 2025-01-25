# Connect-4 Game

Welcome to **Connect-4**, an interactive Python-based implementation of the classic strategy game! 🎮

## Features

- **Customizable board dimensions:** Choose your own board size (minimum 5x5).
- **Dynamic win conditions:** Specify the number of marks needed in a row to win.
- **Player modes:** Play against another person or challenge a CPU.
- **Intelligent AI:** Computer players employ smart strategies to give you a tough challenge.
- **Restart options:** Easily play multiple rounds without restarting the program.

## How to Play

1. **Set Up the Game:**
   - Run the script: `python connect_four.py`.
   - Input the board dimensions (rows and columns must be at least 5).
   - Specify the number of marks (≥3) needed to win.

2. **Choose Players:**
   - You can choose to play as a human (`Player`) or let the CPU (`ComputerPlayer`) control the pieces.
   - Players are assigned "X" and "O" as their marks.

3. **Gameplay:**
   - Players take turns selecting a column to drop their mark.
   - The first player to align the specified number of marks wins (horizontally, vertically, or diagonally).
   - If no moves remain and no winner emerges, the game ends in a tie.

4. **Restart or Exit:**
   - After a match, you'll be prompted to start a new game or quit.

## Code Overview

- **`Game` class:** Handles the game flow, including setup, turns, and win/tie conditions.
- **`Board` class:** Manages the board's state and validates moves.
- **`Player` class:** Represents human players, facilitating their moves.
- **`ComputerPlayer` class:** Implements intelligent decision-making for AI players.

## Requirements

- Python 3.x
- Libraries: `numpy`

## Running the Game

1. Clone the repository:
   ```bash
   git clone https://github.com/Kingflow-23/Funny-Games.git
   cd "Connect Four"
   ```

2. Run the game using Python:
   ```bash
   python connect_four.py
   ```

   If you are using Python 3, use:
   ```bash
   python3 connect_four.py
   ```

---

## How to Play

1. **Setup the Board**:
   - Choose the size of the board (e.g., 3 for a 3x3 board).
   - Specify the number of marks (n) required to win (e.g., 3 for a traditional win condition).

2. **Choose Players**:
   - Select whether Player X and Player O are human or AI.

3. **Take Turns**:
   - Players will take turns placing their marks (X or O) on the board by entering the row and column indices.

4. **Win/Tie Conditions**:
   - The game ends when a player aligns the required number of marks or if no moves are left (tie).

5. **Replay Option**:
   - After the game ends, you'll be asked if you'd like to play again.

---

## Example Gameplay

### Starting the Game:
```
"""Game opening"""

🤖 : Please, enter the number of rows of the board: 6
🤖 : Please, enter the number of columns of the board: 7
🤖 : Please, enter the number of marks you need to align to win: 4
🤖 : Please enter 'cpu' if you want a computer to place 'X': cpu
🤖 : Please enter 'cpu' if you want a computer to place 'O':
🤖 : It's Computer_X's turn.
🤖 : Let's place 'X'!
...
```

## Future Improvements

- **Enhanced AI**: Implement a minimax algorithm for unbeatable gameplay.
- **Customizable Symbols**: Allow players to choose custom symbols.
- **Graphical Interface**: Develop a GUI for a more user-friendly experience.
- **Save and Load Games**: Add functionality to save and resume games.

---

## Contributing

Contributions are welcome! If you have suggestions or find bugs, feel free to open an issue or submit a pull request.
