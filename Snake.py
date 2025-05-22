import random
import pygame

# Initialize pygame
pygame.init()
pygame.font.init()
pygame.display.init()

# Constants
RED =(255, 0, 0)
WHITE = (255, 255, 255)  # Color for grid lines and text
GAME_WIDTH = 720 # Width of the game window
GAME_HEIGHT = 720  # Height of the game window
SNAKE_COLOUR = (0, 255, 0)  # Color of the snake
BACKGROUND_COLOUR = (0, 0, 0)  # Background color of the game
FONT = pygame.font.SysFont("monospace", 16)  # Font for displaying the score
SCORE = 0  # Initial score
IMG = pygame.image.load("apple_img.png")  # Load the apple image
GRID_SIZE = 45  # Size of each grid cell
PURPLE =(128,0,128)

# Initialize the screen
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))  # Set up the game window
pygame.display.set_caption("Snake Game")  # Set the window title
clock = pygame.time.Clock()  # Create a clock object to control game speed
running = True  # Variable to keep the game loop running

# Scale the apple image
IMG = pygame.transform.scale(IMG, (GRID_SIZE, GRID_SIZE))  # Scale the apple image to fit the grid

# Initial position of the apple
initial_apple_pos = (GRID_SIZE * 4, GRID_SIZE * 4)  # Set the initial apple position

# Initial position of the snake
snake_pos = pygame.Rect(GRID_SIZE * 3, GRID_SIZE * 3, GRID_SIZE, GRID_SIZE)  # Set the initial snake position
snake_body = [snake_pos.copy()]  # List to keep track of the snake's body segments
border = pygame.Rect(0,0,GAME_WIDTH,GAME_HEIGHT)

# Initial velocity and direction
velocity_x = GRID_SIZE  # Initial horizontal velocity of the snake
velocity_y = 0  # Initial vertical velocity of the snake
current_direction = 'RIGHT'  # Initial direction of the snake

def draw_grid():
    """
    Draw the grid on the game screen.
    """
    for x in range(0, GAME_WIDTH, GRID_SIZE):
        for y in range(0, GAME_HEIGHT, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)  # Draw the grid lines

def random_grid_position(grid_size, game_width, game_height):
    """
    Generate a random position for the apple, aligned with the grid.
    """
    grid_columns = game_width // grid_size
    grid_rows = game_height // grid_size

    x = random.randint(0, grid_columns - 1) * grid_size
    y = random.randint(0, grid_rows - 1) * grid_size

    return x, y

# Game loop
while running:
    screen.fill(BACKGROUND_COLOUR)  # Clear the screen with the background color
    draw_grid()  # Draw the grid on the screen
    screen.blit(IMG, initial_apple_pos)  # Draw the apple
    pygame.draw.rect(screen,PURPLE,border,1)

    # Scoreboard
    scoretext = FONT.render("Score = " + str(SCORE), 1, RED)  # Rasender the score text
    screen.blit(scoretext, (3, 5))  # Display the score at the top-left corner

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Check if the user wants to quit
            running = False  # Exit the game loop

    # Get the current state of keys
    keys = pygame.key.get_pressed()  # Get the current key presses

    # Change direction based on key presses
    if keys[pygame.K_w] and current_direction != 'DOWN':
        velocity_x = 0
        velocity_y = -GRID_SIZE
        current_direction = 'UP'

    if keys[pygame.K_s] and current_direction != 'UP':
        velocity_x = 0
        velocity_y = GRID_SIZE
        current_direction = 'DOWN'

    if keys[pygame.K_a] and current_direction != 'RIGHT':
        velocity_x = -GRID_SIZE
        velocity_y = 0
        current_direction = 'LEFT'

    if keys[pygame.K_d] and current_direction != 'LEFT':
        velocity_x = GRID_SIZE
        velocity_y = 0
        current_direction = 'RIGHT'

    # Update snake position based on velocity
    snake_pos.x += velocity_x
    snake_pos.y += velocity_y

    # Add the new head to the snake body
    snake_body.insert(0, snake_pos.copy())

    # Collision detection with apple
    if snake_pos.colliderect(pygame.Rect(initial_apple_pos[0], initial_apple_pos[1], GRID_SIZE, GRID_SIZE)):
        SCORE += 1
        initial_apple_pos = random_grid_position(GRID_SIZE, GAME_WIDTH, GAME_HEIGHT)  # Spawn a new apple
    else:
        snake_body.pop()  # Remove the last segment of the snake body if no collision

    if snake_pos.left < 0 or snake_pos.right > GAME_WIDTH or snake_pos.top < 0 or snake_pos.bottom > GAME_HEIGHT:
        if snake_pos.left < 0:
            snake_pos.x = GAME_WIDTH - GRID_SIZE
        if snake_pos.right > GAME_WIDTH:
            snake_pos.x = 0
        if snake_pos.top < 0:
            snake_pos.y = GAME_HEIGHT - GRID_SIZE
        if snake_pos.bottom > GAME_HEIGHT:
            snake_pos.y = 0
    # Draw the snake body
    for segment in snake_body:
        pygame.draw.rect(screen, SNAKE_COLOUR, segment)

    for collision in snake_body[1::]:
        if snake_pos.colliderect(collision):
            running =False

    pygame.display.update()  # Update the display

    clock.tick(10)  # Control the game speed

pygame.quit()  # Quit pygame when the game loop ends
