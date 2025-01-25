# Hangman Multiplayer Game

## Overview

This Python project implements a multiplayer Hangman game. The game allows multiple players to guess words based on their lengths, with scoring based on correct and incorrect guesses. The game tracks player scores and outputs a final leaderboard showing the winner(s).

## Features
- **Word List Preprocessing**: The program loads words from a file, categorizes them by length, and stores this data in a dictionary. The dictionary is saved to a JSON file.
- **Hangman Game Logic**: Players attempt to guess a word based on its length, with a limited number of chances. Correct guesses increase the score, while incorrect guesses deduct points.
- **Multiplayer Support**: The game supports multiple players. Each player plays several rounds, and their scores are accumulated.
- **Leaderboard**: At the end of the game, the final leaderboard is displayed, showing each player's total score.

## Files in this project:
- `hangman_game.py`: The main Python script for running the Hangman game.
- `words.txt`: A text file containing a list of words (one word per line) used in the game. Words wome from [here]("https://raw.githubusercontent.com/Tom25/Hangman/master/wordlist.txt")
- `words.json`: A JSON file that stores the dictionary of word lengths and corresponding words.

## How to Play

1. **Prepare the Word List**:
   - Make sure you have a `words.txt` file with a list of words, one per line. This file will be used to create the word length dictionary.
   
2. **Run the Game**:
   - Execute the Python script to start the game. The script will ask you to input the number of players and the number of rounds per player.
   - Each player will be prompted to choose the length of the word they want to guess. The program will select a word of the specified length randomly.
   - Players have a limited number of chances to guess the word, with correct guesses earning points and wrong guesses losing points.
   
3. **Leaderboard**:
   - After all rounds have been completed, the total scores for each player will be displayed in a leaderboard.

## Installation Instructions

1. Clone or download the repository to your local machine.
2. Make sure you have Python 3.10.11 installed.
3. Ensure you have a `words.txt` file in the same directory with a list of words.
4. Run the `hangman.py` script in your terminal or command prompt.
5. Follow the prompts to play the game.

## Code Explanation

### Step 1: Word List Preprocessing
The program loads words from the `words.txt` file and stores them in a dictionary where the keys are word lengths, and the values are lists of words with that length.

### Step 2: Hangman Game Logic
The game logic handles word guessing. Players input a letter at each step and are shown the current word state. The game keeps track of correct and incorrect guesses, adjusting the score accordingly.

### Step 3: Multiplayer Game
The multiplayer feature allows multiple players to take turns guessing words. The scores for each player are tracked and displayed in a final leaderboard.

### Step 4: Saving Game Data
The dictionary of word lengths and corresponding words is saved as a `words.json` file for later use.

## Example

Here’s an example of the game flow:

Enter the number of players: 2 

Enter the number of rounds per player: 3

**--- Player 1's turn ---**

Round 1 - Player 1: 

Enter the length of the word you want to guess: 5 

You have 3 chances left. 

Current word: _ _ _ _ _ 

Enter a letter: a 

Wrong answer! 

...

Round 2 - Player 1: 

Enter the length of the word you want to guess: 4 

You have 2 chances left. 

Current word: _ _ _ _ 

Enter a letter: o 

Well done! You found a letter!

...

**--- Player 2's turn ---** 

Round 1 - Player 2: 

Enter the length of the word you want to guess: 5 

You have 3 chances left. 

Current word: _ _ _ _ _ 

Enter a letter: t 

Well done! You found a letter! 

...

--- Final Leaderboard --- 

Player 1: 5 points 

Player 2: 8 points