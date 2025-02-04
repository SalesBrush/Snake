import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRADIENT_START = (30, 30, 30)
GRADIENT_END = (10, 10, 10)

# Display dimensions
WIDTH = 800
HEIGHT = 600

# Snake block size
BLOCK_SIZE = 20

# Initialize display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Fancy Graphics")

# Clock to control game speed
clock = pygame.time.Clock()

# Font for displaying score
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Particle class for effects
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(5, 10)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.lifetime = 30

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 1

    def draw(self):
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

# Gradient background
def draw_gradient_background():
    for y in range(HEIGHT):
        r = GRADIENT_START[0] + (GRADIENT_END[0] - GRADIENT_START[0]) * y / HEIGHT
        g = GRADIENT_START[1] + (GRADIENT_END[1] - GRADIENT_START[1]) * y / HEIGHT
        b = GRADIENT_START[2] + (GRADIENT_END[2] - GRADIENT_START[2]) * y / HEIGHT
        pygame.draw.line(screen, (int(r), int(g), int(b)), (0, y), (WIDTH, y))

# Draw rounded rectangle
def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

# Draw glowing circle
def draw_glowing_circle(x, y, radius, color):
    for i in range(3):
        glow_radius = radius + i * 3
        alpha = 100 - i * 30
        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*color, alpha), (glow_radius, glow_radius), glow_radius)
        screen.blit(glow_surface, (x - glow_radius, y - glow_radius))
    pygame.draw.circle(screen, color, (x, y), radius)

# Display score
def display_score(score):
    value = score_font.render("Your Score: " + str(score), True, YELLOW)
    screen.blit(value, [10, 10])

# Draw snake
def draw_snake(snake_list):
    for i, block in enumerate(snake_list):
        x, y = block
        if i == 0:
            # Draw snake head with glow
            draw_glowing_circle(x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2, BLOCK_SIZE // 2, GREEN)
        else:
            # Draw snake body with rounded rectangles
            draw_rounded_rect(screen, GREEN, [x, y, BLOCK_SIZE, BLOCK_SIZE], 5)

# Draw food with pulsating effect
def draw_food(x, y, pulse):
    radius = BLOCK_SIZE // 2 + int(5 * math.sin(pulse))
    draw_glowing_circle(x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2, radius, RED)

# Draw particles
def draw_particles(particles):
    for particle in particles:
        particle.update()
        particle.draw()

# Draw obstacles
def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLUE, [obstacle[0], obstacle[1], BLOCK_SIZE, BLOCK_SIZE])

# Wrap snake around the screen
def wrap_around(position):
    x, y = position
    if x >= WIDTH:
        x = 0
    elif x < 0:
        x = WIDTH - BLOCK_SIZE
    if y >= HEIGHT:
        y = 0
    elif y < 0:
        y = HEIGHT - BLOCK_SIZE
    return (x, y)

# Main game loop
def game_loop():
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

    # Particles
    particles = []

    # Pulse effect for food
    pulse = 0

    # Obstacles
    obstacles = []
    for _ in range(3):  # Initial number of obstacles
        obstacle_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        obstacle_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        obstacles.append((obstacle_x, obstacle_y))

    # Score
    score = 0

    # Game speed
    game_speed = 15

    while not game_over:
        while game_close:
            screen.fill(BLACK)
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

        # Wrap snake around the screen
        x += x_change
        y += y_change
        x, y = wrap_around((x, y))

        draw_gradient_background()

        # Draw food with pulsating effect
        draw_food(food_x, food_y, pulse)
        pulse += 0.1

        # Draw particles
        draw_particles(particles)

        # Draw obstacles
        draw_obstacles(obstacles)

        # Snake head
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check if snake collides with itself
        for i, block in enumerate(snake_list[:-1]):
            if block == snake_head:
                # Cut the snake by the amount it overlaps
                snake_list = snake_list[:i]
                snake_length = len(snake_list)
                break

        # Check if snake collides with obstacles
        for obstacle in obstacles:
            if x == obstacle[0] and y == obstacle[1]:
                game_close = True

        draw_snake(snake_list)
        display_score(score)

        pygame.display.update()

        # Check if snake eats food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            snake_length += 1
            score += 1

            # Add particles
            for _ in range(20):
                particles.append(Particle(x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2, YELLOW))

            # Increase obstacles every 100 points
            if score % 100 == 0:
                obstacle_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
                obstacle_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
                obstacles.append((obstacle_x, obstacle_y))

            # Increase speed every 1000 points
            if score % 1000 == 0:
                game_speed += 2

        clock.tick(game_speed)

    pygame.quit()
    quit()

# Start the game
game_loop()
