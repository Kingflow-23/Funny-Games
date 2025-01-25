import random
import time

""""
Name of the game: Mindreader (Mastermind)

Rules:

Main settings:
- In this version, it's a player trying to find the 4 digit number.
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
    Displays an opening message for the player.

    Parameters:
        name: The player name.
    """

    print(
        f"""
          Hello Everyone !! 
          I'm AI KF23 🤖, we're here today with {name} who will try to beat our game.
          Let me introduce you the rules ✨:

          - At the start of the game, I generate a 4-digit number within all digits are unique, your job is to guess this number !!

          - If one number in your guess is good and at the right place in the number to guess sequence, a '✅' sign is displayed.
          - If one number in your guess is good but not at the right place in the number to guess sequence, a '⛔' sign is displayed.
          - If neither of the previous conditions are matched, I'll just put a '❌' sign at the place of the wrong guess.
          
          - To finish, there's actually 5 attempts for you but if you accept the challenge you can reduce yourself the number of attempts.
            or if you're a coward 👀, you can set the number of attempts as a negative number or 0 to play untill you find the number.
          
          Let's all enjoy this game 🔥, feel free to play at home with your family and friends.
          Now, let's all wish {name} good luck 🍀 cause it'll be needed !!
          {"_"*135}
          """
    )


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
            if number in seq_to_guess[:5]:
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

              Well played {player_name} 🤖, you successfully guessed the number : {''.join(seq_to_guess)} !! 🥂
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


def main_game(num_attempt=5):
    """
    Main function for the game.

    Parameters:
        num_attempts (default to 5): Number of attempts. Set it to 0 or anything negative to play until the number is guessed.
    """
    lasting_attempts = num_attempt
    player_name = input("Please let me know your name 🤖: ")
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

    start_time = time.time()

    while True:
        player_guess = [i for i in input("Please make your guess 🤖: ")]
        seq_answer = check_guess(seq_to_guess, player_guess)

        print(seq_answer)

        if seq_answer == ["✅", "✅", "✅", "✅"]:
            end_time = time.time()
            game_ending(
                result="good",
                player_name=player_name,
                num_attempt=num_attempt,
                seq_to_guess=seq_to_guess,
            )
            print(f"""
                  You took {end_time - start_time:.2f} seconds.
                  """)
            break

        else:
            lasting_attempts -= 1
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
                break


if __name__ == "__main__":
    main_game()
