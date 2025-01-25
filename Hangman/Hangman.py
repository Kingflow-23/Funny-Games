import pandas as pd
import numpy as np
import json
import random

# Step 1: Load the word list from the text file and preprocess it into a dictionary
def load_words(file_path='words.txt'):
    """
    Loads words from a file and returns them as a list. Words are stripped of trailing newline characters.
    
    Args:
        file_path (str): Path to the word list file.
        
    Returns:
        list: A list of words from the file.
    """
    with open(file_path, 'r') as f:
        wordlist = [line.rstrip() for line in f.readlines()]
    return wordlist


def create_word_length_dict(wordlist):
    """
    Creates a dictionary where keys are word lengths, and values are lists of words of that length.
    
    Args:
        wordlist (list): List of words to categorize by length.
        
    Returns:
        dict: A dictionary where the keys are word lengths, and values are lists of words.
    """
    dict_len_word = {}
    for word in wordlist:
        word_len = len(word)
        if word_len not in dict_len_word:
            dict_len_word[word_len] = []
        dict_len_word[word_len].append(word)
    return dict_len_word


# Step 2: Create a JSON file that stores the dictionary of word lengths
def save_word_length_dict_to_json(dict_len_word, output_path="words.json"):
    """
    Saves the dictionary of word lengths to a JSON file.
    
    Args:
        dict_len_word (dict): A dictionary where keys are word lengths, and values are lists of words.
        output_path (str): Path to the output JSON file.
    """
    with open(output_path, "w") as f:
        json.dump(dict_len_word, f, indent=4)


# Step 3: Hangman game logic
def hangman_game(l, dict_len_word):
    """
    Main logic for the Hangman game. Players attempt to guess a word based on its length.
    
    Args:
        l (int): The length of the word the player wants to guess.
        dict_len_word (dict): A dictionary where keys are word lengths and values are word lists.
        
    Returns:
        int: The player's score after the game.
    """
    # Ensure the chosen length exists in the dictionary
    while l not in dict_len_word:
        l = int(input('Error! No words of this length. Please enter a valid word length: '))
    
    # Choose a random word of the given length
    choice_list = dict_len_word[l]
    chosen_word = random.choice(choice_list)
    
    # Initialize game variables
    score = 0
    chances = l//2 + 1 # Number of chances equals the word length
    cpt = 0  # Counter for mistakes
    guessed_word = ['_'] * l  # Word state with underscores for unguessed letters
    
    # Start the game loop
    while cpt < chances:
        if guessed_word == list(chosen_word):  # Player won
            break
        
        # Show current status
        print(f'\nYou have {chances-cpt} chances left.')
        print("Current word:", " ".join(guessed_word))
        letter = input('Enter a letter: ').lower()

        # Check if the guessed letter is in the chosen word
        if letter in chosen_word:
            # Update the guessed word and increment score
            for i in range(len(chosen_word)):
                if chosen_word[i] == letter:
                    guessed_word[i] = letter
                    score += 2  # Earn points for each correct letter
            print('Well done! You found a letter!')
        else:
            # Incorrect guess
            cpt += 1
            score -= 1  # Deduct points for incorrect guesses
            print('Wrong answer!')

    # Show final results
    print(f'\nThe word was: {chosen_word}')
    
    if guessed_word == list(chosen_word):
        print(f'Congratulations! You won with {score} points.')
    else:
        print(f'Sorry, you lost. Your score is {score} points.')

    return score


# Step 4: Function to track the scores of multiple players
def hangman_game_score(l, dict_len_word):
    """
    A variant of the Hangman game that only returns the score instead of interactive play.
    
    Args:
        l (int): The length of the word the player wants to guess.
        dict_len_word (dict): A dictionary of word lengths to word lists.
        
    Returns:
        int: The player's score after the game.
    """
    return hangman_game(l, dict_len_word)


# Step 5: Multiplayer function to manage multiple players and games
def multiplayer_hangman(nb_players, nb_words, dict_len_word):
    """
    Manages the multiplayer aspect of the Hangman game.
    
    Args:
        nb_players (int): The number of players.
        nb_words (int): The number of rounds each player will play.
        dict_len_word (dict): The dictionary of words categorized by length.
        
    Returns:
        pd.Series: A Pandas Series with player numbers as indices and total scores as values.
    """
    players_scores = []  # List to store total scores for each player
    
    # Loop through each player
    for player_num in range(1, nb_players + 1):
        print(f"\n--- Player {player_num}'s turn ---")
        total_score = 0
        
        # Loop through each round for the player
        for round_num in range(1, nb_words + 1):
            print(f"\nRound {round_num} - Player {player_num}:")
            word_length = int(input('Enter the length of the word you want to guess: '))
            total_score += hangman_game_score(word_length, dict_len_word)
        
        players_scores.append(total_score)
    
    # Create a DataFrame to summarize the scores
    players = [f"Player {i+1}" for i in range(nb_players)]
    scores_df = pd.Series(players_scores, index=players, name="Total Score")
    return scores_df


# Main program execution
if __name__ == "__main__":
    wordlist = load_words('words.txt')  # Load the words from file
    dict_len_word = create_word_length_dict(wordlist)  # Create the dictionary of word lengths
    save_word_length_dict_to_json(dict_len_word)  # Save the dictionary as a JSON file

    # Multiplayer game setup
    num_players = int(input("Enter the number of players: "))
    num_words = int(input("Enter the number of rounds per player: "))
    
    # Get the final scores for all players
    scores = multiplayer_hangman(num_players, num_words, dict_len_word)
    
    # Print the final leaderboard
    print("\n--- Final Leaderboard ---")
    print(scores)
