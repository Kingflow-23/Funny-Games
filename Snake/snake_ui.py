import pygame
import random

# Initialize pygame
pygame.init()

# Set up the game window
width = 600
height = 400
game_window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Set up the clock and font
clock = pygame.time.Clock()
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def Your_score(score):
    """
    Display the current score on the screen.

    Parameters:
        score (int): The score to display.
    """
    value = score_font.render("Score: " + str(score), True, black)
    game_window.blit(value, [0, 0])

def our_snake(snake_block, snake_List):
    """
    Draw the snake on the screen.

    Parameters:
        snake_block (int): The size of each block that makes up the snake.
        snake_List (list): A list containing the positions of the snake's body parts.
    """
    for x in snake_List:
        pygame.draw.rect(game_window, green, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    """
    Display a message on the screen.

    Parameters:
        msg (str): The message to display.
        color (tuple): The color of the text.
    """
    mesg = font_style.render(msg, True, color)
    game_window.blit(mesg, [width / 8, height / 3])

def gameLoop():
    """
    Main game loop that handles game logic, input, and rendering.
    """
    game_over = False
    game_close = False

    # Initial snake settings
    x1 = width / 2
    y1 = height / 2
    x1_change = 0
    y1_change = 0

    snake_block = 10
    snake_speed = 15

    snake_List = []
    Length_of_snake = 1

    # Create food
    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close:
            game_window.fill(blue)
            message("You Lost! Press Enter to Again or Return Quit", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():   
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_RETURN:
                        gameLoop()

        # Handling user input for snake movement
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        # Check if the snake hits the boundaries
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        game_window.fill(blue)

        # Draw food and snake
        pygame.draw.rect(game_window, white, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Check if the snake bites itself
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # Update the snake and score
        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)

        pygame.display.update()

        # Check if the snake eats the food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()

if __name__ == "__main__":
    gameLoop()
