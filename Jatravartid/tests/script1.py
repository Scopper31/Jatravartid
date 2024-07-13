# -*- coding: utf-8 -*-
#напиши консольную игру flappy bird

import pygame
import random
import time
import os

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define some dimensions
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512

# Define the bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        # Set the bird's color, width, and height
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

        # Set the bird's initial position
        self.rect.x = 50
        self.rect.y = 250

        # Set the bird's velocity
        self.velocity = 0

    # Update the bird's position
    def update(self):
        # Apply gravity
        self.velocity += 0.5
        self.rect.y += self.velocity

        # Check for collisions with the ground
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

# Define the pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        # Set the pipe's color, width, and height
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

        # Set the pipe's initial position
        self.rect.x = SCREEN_WIDTH
        self.rect.y = 0

        # Set the pipe's velocity
        self.velocity = -2

        self.passed = False  # Flag to track if the bird has passed this pipe

    # Update the pipe's position
    def update(self):
        # Move the pipe to the left
        self.rect.x += self.velocity

        # Remove the pipe if it goes off screen
        if self.rect.right < 0:
            self.kill()

# Define a function to check for collisions
def check_collisions(bird, pipes):
    # Check for collisions with the pipes
    for pipe in pipes:
        if bird.rect.colliderect(pipe.rect):
            return True

    # Check for collisions with the ground
    if bird.rect.bottom >= SCREEN_HEIGHT:
        return True

    # No collisions detected
    return False

# Define a function to update the score
def update_score(bird, pipes, score):
    # Check if the bird has passed through a pipe
    for pipe in pipes:
        if pipe.rect.right < bird.rect.left and not pipe.passed:
            score += 1
            pipe.passed = True
    return score

# Define a function to display the score
def display_score(score):
    # Create a font object
    font = pygame.font.Font(None, 36)

    # Render the score text
    text = font.render("Score: " + str(score), True, WHITE)

    # Display the score text
    screen.blit(text, [10, 10])

# Initialize Pygame
pygame.init()

# Set the screen dimensions
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Set the title of the window
pygame.display.set_caption("Flappy Bird")

# Create a bird object
bird = Bird(RED, 20, 20)

# Create a group to hold the pipes
pipes = pygame.sprite.Group()

# Initialize the score
score = 0

# Pipe properties
pipe_width = 80
pipe_height = 400
pipe_gap = 200

# Pipe movement speed
pipe_speed = 5

# Pipe generation timer
pipe_timer = 0

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Jump when space is pressed
                bird.velocity = -10  # Negative velocity for upward jump

    # Update the bird's position
    bird.update()

    # Update the pipes
    pipes.update()

    # Generate new pipes at random intervals
    pipe_timer += 1
    if pipe_timer >= 100:  # Generate a new pipe every 100 frames
        # Generate random gap size
        gap_size = random.randint(150, 250)

        # Calculate pipe positions
        top_pipe_height = random.randint(100, SCREEN_HEIGHT - gap_size - 100)
        bottom_pipe_height = SCREEN_HEIGHT - top_pipe_height - gap_size

        # Create pipe objects
        top_pipe = Pipe(GREEN, pipe_width, top_pipe_height)
        bottom_pipe = Pipe(GREEN, pipe_width, bottom_pipe_height)

        # Set the position of the pipes
        top_pipe.rect.y = 0
        bottom_pipe.rect.y = top_pipe_height + pipe_gap

        # Add the pipes to the group
        pipes.add(top_pipe, bottom_pipe)
        pipe_timer = 0

    # Check for collisions
    if check_collisions(bird, pipes):
        # Stop the game
        running = False

    # Update the score
    score = update_score(bird, pipes, score)

    # Display the score
    display_score(score)

    # Fill the screen with black
    screen.fill(BLACK)

    # Draw the bird
    screen.blit(bird.image, bird.rect)

    # Draw the pipes
    pipes.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()

# Console-based Flappy Bird
# Define ASCII characters for game elements
BIRD = "@"
PIPE = "|"
GROUND = "-"
SKY = " "

# Game variables
bird_x = 5
bird_y = 5
pipe_x = 20
pipe_y = 10
pipe_gap = 5
score = 0

# Game loop
def game_loop():
    global bird_y, pipe_x, score

    while True:
        # Clear the console screen
        os.system("cls" if os.name == "nt" else "clear")

        # Update game state
        bird_y -= 1
        pipe_x -= 1

        # Check for collision with ground
        if bird_y <= 0:
            game_over()
            break

        # Check for collision with pipes
        if pipe_x == bird_x and (bird_y <= pipe_y or bird_y >= pipe_y + pipe_gap):
            game_over()
            break

        # Increment score when bird passes a pipe
        if pipe_x == bird_x - 1:
            score += 1

        # Render the game
        render_game()

        # Sleep for a short duration
        time.sleep(0.1)

# Function to render the game
def render_game():
    # Create a game board
    board = [[" " for _ in range(20)] for _ in range(15)]

    # Draw the bird
    board[bird_y][bird_x] = BIRD

    # Draw the pipes
    for i in range(pipe_y):
        board[i][pipe_x] = PIPE
    for i in range(pipe_y + pipe_gap, 15):
        board[i][pipe_x] = PIPE

    # Draw the ground
    for i in range(14, 15):
        for j in range(20):
            board[i][j] = GROUND

    # Print the game board
    for row in board:
        print("".join(row))

    # Display score
    print(f"Score: {score}")

# Function to display game over message
def game_over():
    print("Game Over!")
    print(f"Final Score: {score}")

# Start the game loop
game_loop()
