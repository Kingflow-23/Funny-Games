import matplotlib.pyplot as plt
import numpy as np
import random
import time

""""
Name of the game: MindReader (Mastermind)

Rules:

Main settings:
- In this version, it's a computer trying to find the 4 digit number.
- The number guessed can't have the same number within two times.

Game settings:
- If one number in the player guess is good and at the right place in the number to guess sequence,
  a '✅' sign is displayed.
- If one number in the player guess is good but not at the right place in the number to guess sequence,
  a '⛔' sign is displayed.
- If neither of the previous conditions are matched, I'll just put a '❌' sign at the place of the wrong guess.
- There was actually no limit of attempts for the player but I'll try to implement this as a parameter.
  for players who would want it.
"""


def game_opening(name: str):
    """
    Displays an opening message for the computer.

    Parameters:
        name: The computer name.
    """

    print(
        f"""
          Hello Everyone !! 
          
          I'm AI KF23 🤖, we're here today with {name} who will try his best to beat our game.
          Let me introduce you the rules ✨:

          - At the start of the game, I generate a 4-digit number within all digits are unique, your job is to guess this number !!

          - If one number in your guess is good and at the right place in the number to guess sequence, a '✅' sign is displayed.
          - If one number in your guess is good but not at the right place in the number to guess sequence, a '⛔' sign is displayed.
          - If neither of the previous conditions are matched, I'll just put a '❌' sign at the place of the wrong guess.
          
          - To finish, I can personnally beat the game in 5 attempts in average 🤖
            but if you accept the challenge you can reduce yourself the number of attempts.
            or if you're a coward 👀, you can set the number of attempts as a negative number or 0 to play untill you find the number.

          - In this computer version of our game, it's actually interesting to set the way of thinking of the computer
            to make him able to answer correctly in the least amount of attempts.
          
          Let's all enjoy this game 🔥, feel free to play at home with your microvaves and servers.
          Now, let's all wish {name} good luck 🍀 cause it'll be needed !!
          {"_"*135}
          """
    )


def guess(previous_guess: list, choices: list, seq_answer: list):
    """
    Guess the number based on the answer of the previous iteration.

    Parameters:
        previous_guess : Previous player guess:
        choices: list of digit available.
        seq_answer: Sequence containg '✅', '⛔' or '❌' based on matching of user input with the number to guess.

    Return:
        choices: Updated list of digit available.
        player_guess: Next Player guess

    """
    player_guess = ["", "", "", ""]
    available_places = [0, 1, 2, 3]
    num_misplaced = set()

    if seq_answer == None:  # First guess case: Random guess
        while True:
            player_guess = list(str(random.randint(1000, 9999)))

            if len(player_guess) == len(set(player_guess)):  # Ensure unique digits
                break
    else:
        # Step 1: Handle ✅ case: Digit is correct and in the correct place
        for place, answer in enumerate(seq_answer):
            if answer == "✅":
                player_guess[place] = previous_guess[place]
                available_places.remove(place)              # Mark this place as filled
                if player_guess[place] in choices:
                    choices.remove(player_guess[place])   # Remove used digit from choices
                if player_guess[place] in num_misplaced:
                    num_misplaced.remove(player_guess[place])    # Remove used digit from misplace digit list

        # Debug statement to see choices after handling ✅
        # print(f"After handling '✅', choices: {choices}")

        # Step 2: Handle ⛔ case: Digit is correct but in the wrong place
        for place, answer in enumerate(seq_answer):
            if answer == "⛔":
                num_misplaced.add(previous_guess[place])

                temp_available_places = [i for i in available_places if i != place]  # Exclude the current place

                if temp_available_places:
                    new_place = random.choice(temp_available_places)    # Pick a new position
                    player_guess[new_place] = previous_guess[place]
                    available_places.remove(new_place)                  # Mark the new place as filled
                    
                if previous_guess[place] in choices:
                    choices.remove(previous_guess[place])               # Remove correct digit from choices

        # Debug statement to see choices after handling ⛔
        # print(f"After handling '⛔', choices: {choices}")

        # Step 3: Handle ❌ case: Digit is incorrect
        for place, answer in enumerate(seq_answer):
            if answer == "❌" and previous_guess[place] in choices:
                choices.remove(previous_guess[place])

        # Debug statement to see final choices after ❌ handling
        # print(f"After handling '❌', choices: {choices}")
        
        # Step 4: Fill remaining empty spots with random choices
        for place in available_places:
            if player_guess[place] == "":  # If still empty
                if not choices:  # Check if choices is empty
                    if num_misplaced:  # If num_misplaced has values, use them
                        # Filter num_misplaced to avoid those already in player_guess
                        valid_misplaced = [digit for digit in num_misplaced if digit not in player_guess]
                        
                        if valid_misplaced:
                            choices = valid_misplaced  # Use the valid misplaced digits
                        else:
                            # If no valid misplaced digits, fill with remaining digits
                            remaining_digits = [str(i) for i in range(10) if str(i) not in player_guess]
                            choices = remaining_digits
                    else:
                        # If no valid misplaced digits, fill with remaining digits
                        remaining_digits = [str(i) for i in range(10) if str(i) not in player_guess]
                        choices = remaining_digits

                # Ensure choices is not empty before trying to select a new digit
                if choices:
                    new_digit = random.choice(choices)
                    while new_digit in player_guess:  # Ensure no duplicates
                        new_digit = random.choice(choices)

                    player_guess[place] = new_digit
                    choices.remove(new_digit)  # Remove used digit from choices

    return choices, player_guess


def check_guess(seq_to_guess: list, guess: list):
    """
    Analyse the user guess to give him a feedback adapted.

    Parameters:
        seq_to_guess: The sequence to guess.
        guess: The user guess.

    Return:
        seq_answer: Sequence containing '✅', '⛔' or '❌' based on matching of user input with the number to guess.

    Raises:
        IndexError: If the player give more than a 4-digit number.
    """

    seq_answer = ["❌", "❌", "❌", "❌"]

    for place, number in enumerate(guess):
        try:
            # check appartenance
            if number in seq_to_guess:
                # check place
                if number == seq_to_guess[place]:
                    seq_answer[place] = "✅"
                else:
                    seq_answer[place] = "⛔"

        except IndexError:
            print(
                """
                You have given a number too large !! 
                Excess numbers won't be taken into account !
                """
            )

    return seq_answer


def game_ending(result: str, player_name: str, num_attempt: int, seq_to_guess: list):
    """
    Display ending message based on the result of the game.

    Parameters:
        result: Quick message to know if the user had won ('good') or lost ('bad').
        player_name: player name.
        num_attempt: Number of attempts for the game.
        seq_to_guess: Sequence to guess.
    """

    if result == "good":
        print(
            f"""
              {"_"*131}

              Well played {player_name} 🤖, you successfully guessed the number : {''.join(seq_to_guess)} in {num_attempt} attempts !! 🥂
              I'll train myself on your game to give you a harder number to guess next time.
              See you again for another exciting game ! ✨
              {"_"*131}
              """
        )
    else:
        print(
            f"""
              {"_"*131}

              I'm sorry to announce you that {player_name} wasn't able to complete the game in {num_attempt} attempts 🤖,
              The number you had to guess was : {''.join(seq_to_guess)}.
              Don't be sad, you were just a little to optimistic to try to find my number in only {num_attempt} attempts.
              Don't hesitate to try again another day but I'm not going to make the game any easier 🤖.
              That's all for today, make sure to follow our next game !! ✨
              {"_"*131}
              """
        )


def main_game(num_attempt=-1):
    """
    Main function for the game.

    Parameters:
        num_attempts (default to 5): Number of attempts. Set it to 0 or anything negative to play until the number is guessed.
    """
    previous_guess = None
    choices = list(map(str, list(range(10))))

    cpt_attempts = 0
    lasting_attempts = num_attempt

    # player_name = input("Please let me know your name 🤖: ")
    player_name = "Wolf"

    game_opening(name=player_name)

    # Check that all numbers in the number to guess are unique.
    while True:
        seq_to_guess = list(str(random.randint(1000, 9999)))

        if len(seq_to_guess) == len(set(seq_to_guess)):
            break

    print(
        f"""
          I have chosen the 4-digit number, this one will be hard to guess 🤖.
          Let's start the game !! 🔥
          {"_"*135}
          """
    )

    seq_answer = None
    start_time = time.time()

    while True:
        choices, player_guess = guess(previous_guess, choices, seq_answer)

        print(f"{player_name} tries this sequence : {player_guess}")

        player_guess = [i for i in player_guess]
        seq_answer = check_guess(seq_to_guess, player_guess)

        print(seq_answer)

        if seq_answer == ["✅", "✅", "✅", "✅"]:
            end_time = time.time()
            game_ending(
                result="good",
                player_name=player_name,
                num_attempt=cpt_attempts,
                seq_to_guess=seq_to_guess,
            )
            print(f"""
                  You took {end_time - start_time:.2f} seconds.
                  """)
            return cpt_attempts

        else:
            lasting_attempts -= 1
            cpt_attempts += 1
            previous_guess = player_guess
            if lasting_attempts == 0:
                end_time = time.time()
                game_ending(
                    result="bad",
                    player_name=player_name,
                    num_attempt=num_attempt,
                    seq_to_guess=seq_to_guess,
                )
                print(f"""
                      You took {end_time - start_time:.2f} seconds.
                      """)
        
                return cpt_attempts

        # time.sleep(0.3)


def plot_result(attempts, filename='auto_mastermind_result.png'):
    """
    Plots the histogram of the number of attempts taken to guess the correct number.

    Parameters:
        attempts (list): A list of integers representing the number of attempts.
        filename (str): The name of the file to save the plot as an image.
    """
    
    # Create a new figure with a specified size
    plt.figure(figsize=(14, 12))
    
    # Create a histogram of attempts
    plt.hist(attempts, bins=range(1, max(attempts)+2), align='left', color='skyblue', edgecolor='black')
    
    # Set the title and labels
    plt.title('Number of Attempts to Guess the Correct Number')
    plt.xlabel('Number of Attempts')
    plt.ylabel('Frequency')
    
    # Set x-ticks to show each attempt number
    plt.xticks(range(1, max(attempts) + 1))
    
    # Add grid lines for better readability
    plt.grid(axis='y', alpha=0.75)

    # Annotate the plot with the mean and median attempts
    mean_attempts = np.mean(attempts)
    median_attempts = np.median(attempts)

    plt.text(0.5, 0.95, f'Mean Attempts: {mean_attempts:.2f}', 
            transform=plt.gca().transAxes, 
            horizontalalignment='center', 
            verticalalignment='top')

    plt.text(0.5, 0.90, f'Median Attempts: {median_attempts:.2f}', 
            transform=plt.gca().transAxes, 
            horizontalalignment='center', 
            verticalalignment='top')
    
    # Save the plot to a file
    plt.savefig(filename, format='png')

    plt.close()

if __name__ == "__main__":
    # main_game()

    formatted_time = time.strftime("%Y-%m-%d_%H-%M-%S")

    num_rounds = 10000
    all_attempts = []

    for _ in range(num_rounds):
        num_attempts = main_game(num_attempt=-1)
        all_attempts.append(num_attempts) 

    plot_result(all_attempts, filename=f'auto_mastermind_result_{formatted_time}.png')