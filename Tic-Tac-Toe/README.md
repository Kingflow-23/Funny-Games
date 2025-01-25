# Tic-Tac-Toe Game

Welcome to the **Tic-Tac-Toe** game! This is a Python-based implementation of the classic game, allowing human players to compete against each other or challenge an AI opponent.

---

## Features

- **Dynamic Board Size**: Customize the board size to your liking (minimum size: 3x3).
- **Flexible Win Conditions**: Choose the number of marks (n) required to win.
- **Human vs Human**: Play against a friend.
- **Human vs AI**: Test your skills against a challenging AI.
- **Smart AI**: The computer player can block, attack, and even strategize to create or prevent forks.
- **Interactive Gameplay**: Intuitive prompts for entering moves and detailed feedback.

---

## Getting Started

### Prerequisites
Make sure you have **Python 3.x** installed on your system. You can check your Python version using:

```bash
python --version
```

or

```bash
python3 --version
```

### Installation
1. Clone this repository or download the game file.
   ```bash
   git clone https://github.com/Kingflow-23/Funny-Games.git
   cd Tic-Tac-Toe
   ```

2. Run the game using Python:
   ```bash
   python n_tic_tac_toe.py
   ```

   If you are using Python 3, use:
   ```bash
   python3 n_tic_tac_toe.py
   ```

3. Run the game UI using Python:
   ```bash
   python n_tic_tac_toe.ui
   ```

   If you are using Python 3, use:
   ```bash
   python3 n_tic_tac_toe.ui
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

🤖 : Please, enter the size of the board : 3
🤖 : Please, enter the number of marks you need to align to win : 3
🤖 : Please enter 'cpu' if you want a computer to place 'X' : h
🤖 : Please, X player, enter your name : Alice
🤖 : Please enter 'cpu' if you want a computer to place 'O' : cpu
🤖 : Please, enter a name for computer O player : AI_O

🤖 : Players are ready! Let's start the game 🎉

     column
   0   1   2
 -------------
 |   |   |   | 0
 -------------
 |   |   |   | 1 row
 -------------
 |   |   |   | 2
 -------------

🤖 : It's Alice's turn.
🤖 : Let's place 'X'!
🤖 : Alice, enter the row (0-2): 1
🤖 : Alice, enter the column (0-2): 1

🤖 : AI_O placed O at (0, 0).

...

```

### Ending the Game:
```
🤖 : Congratulations Alice, you win! ✨
🤖 : Do you want to play again? (y/n): n
🤖 : Thanks for playing! Goodbye!
```

---

## Project Structure

```
.
├── n_tic_tac_toe.ui        # User interface code
├── n_tic_tac_toe.py        # Main game file
├── README.md               # Documentation
```

---

## Future Improvements

- **Enhanced AI**: Implement a minimax algorithm for unbeatable gameplay.
- **Customizable Symbols**: Allow players to choose custom symbols.
- **Graphical Interface**: Develop a GUI for a more user-friendly experience.
- **Save and Load Games**: Add functionality to save and resume games.

---

## Contributing

Contributions are welcome! If you have suggestions or find bugs, feel free to open an issue or submit a pull request.
