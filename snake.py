import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Display dimensions
WIDTH = 800
HEIGHT = 600

# Snake block size
BLOCK_SIZE = 20

# Initialize display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock to control game speed
clock = pygame.time.Clock()

# Font for displaying score
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def display_score(score):
    """Display the current score."""
    value = score_font.render("Your Score: " + str(score), True, YELLOW)
    screen.blit(value, [10, 10])

def draw_snake(block_size, snake_list):
    """Draw the snake on the screen."""
    for block in snake_list:
        pygame.draw.rect(screen, GREEN, [block[0], block[1], block_size, block_size])

def display_message(msg, color):
    """Display a message on the screen."""
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [WIDTH / 6, HEIGHT / 3])

def game_loop():
    """Main game loop."""
    game_over = False
    game_close = False

    # Initial snake position and movement
    x = WIDTH / 2
    y = HEIGHT / 2
    x_change = 0
    y_change = 0

    # Snake body
    snake_list = []
    snake_length = 1

    # Food position
    food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    # Special food (reward)
    special_food_x = -1
    special_food_y = -1
    special_food_active = False

    # Obstacles
    obstacles = [
        (200, 200),
        (400, 400),
        (600, 100),
    ]

    # Score
    score = 0

    while not game_over:
        while game_close:
            screen.fill(BLUE)
            display_message("You Lost! Press Q-Quit or C-Play Again", RED)
            display_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = BLOCK_SIZE
                    x_change = 0

        # Check if snake hits the wall
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        x += x_change
        y += y_change
        screen.fill(BLACK)

        # Draw food
        pygame.draw.rect(screen, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])

        # Draw special food (if active)
        if special_food_active:
            pygame.draw.rect(screen, YELLOW, [special_food_x, special_food_y, BLOCK_SIZE, BLOCK_SIZE])

        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.rect(screen, WHITE, [obstacle[0], obstacle[1], BLOCK_SIZE, BLOCK_SIZE])

        # Snake head
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check if snake collides with itself
        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        # Check if snake collides with obstacles
        for obstacle in obstacles:
            if x == obstacle[0] and y == obstacle[1]:
                game_close = True

        draw_snake(BLOCK_SIZE, snake_list)
        display_score(score)

        pygame.display.update()

        # Check if snake eats food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            snake_length += 1
            score += 1

            # Activate special food randomly
            if random.randint(1, 10) == 1:
                special_food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
                special_food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
                special_food_active = True

        # Check if snake eats special food
        if special_food_active and x == special_food_x and y == special_food_y:
            score += 5
            special_food_active = False

        clock.tick(15)

    pygame.quit()
    quit()

# Start the game
game_loop()
