# -*- coding: utf-8 -*-
#������ flappy bird �� pygame

import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 288
screen_height = 512
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Game title
pygame.display.set_caption("Flappy Bird")

# Load bird images (replace with your own images)
bird_images = [pygame.image.load("images/bird1.png").convert_alpha(),
               pygame.image.load("images/bird2.png").convert_alpha(),
               pygame.image.load("images/bird3.png").convert_alpha()]

# Bird class (Programmer 2)
class Bird:
    def __init__(self):
        self.x = 50
        self.y = screen_height // 2
        self.velocity = 0
        self.gravity = 0.25
        self.flap_strength = -5
        self.image_index = 0
        self.image = bird_images[self.image_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        # Update velocity due to gravity
        self.velocity += self.gravity
        self.y += self.velocity

        # Flap animation
        self.image_index = (self.image_index + 1) % len(bird_images)
        self.image = bird_images[self.image_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def flap(self):
        self.velocity = self.flap_strength

# Pipe class (Programmer 3)
class Pipe:
    def __init__(self, top_pipe_height, bottom_pipe_height, x):
        self.top_pipe_height = top_pipe_height
        self.bottom_pipe_height = bottom_pipe_height
        self.x = x
        self.width = 52
        self.speed = -2  # Negative for leftward movement
        self.passed = False

        # Load pipe images (replace with your own images)
        self.top_pipe_image = pygame.image.load("images/top_pipe.png").convert_alpha()
        self.bottom_pipe_image = pygame.image.load("images/bottom_pipe.png").convert_alpha()

        self.top_pipe_rect = self.top_pipe_image.get_rect(topleft=(self.x, -self.top_pipe_height))
        self.bottom_pipe_rect = self.bottom_pipe_image.get_rect(bottomleft=(self.x, screen_height + self.bottom_pipe_height))

    def update(self):
        self.x += self.speed
        self.top_pipe_rect.x = self.x
        self.bottom_pipe_rect.x = self.x

    def check_passed(self, bird_x):
        return bird_x > self.x + self.width

    def check_collision(self, bird_x, bird_y, bird_radius):
        # Check collision with top pipe
        if bird_y - bird_radius < 0 - self.top_pipe_height:
            return True

        # Check collision with bottom pipe
        if bird_y + bird_radius > screen_height - self.bottom_pipe_height:
            return True

        # Check collision with pipe sides
        if bird_x - bird_radius < self.x and bird_x + bird_radius > self.x + self.width:
            return True

        return False

# Create bird and pipe objects
bird = Bird()
pipes = []

# Game variables
score = 0
game_over = False
clock = pygame.time.Clock()

# Game loop (Programmer 4)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.flap()

    # Update bird
    bird.update()

    # Handle pipe creation
    if len(pipes) == 0 or pipes[-1].x < screen_width // 2:
        top_pipe_height = random.randint(100, 300)
        bottom_pipe_height = screen_height - top_pipe_height - 150
        pipes.append(Pipe(top_pipe_height, bottom_pipe_height, screen_width))

    # Update and remove off-screen pipes
    for pipe in pipes:
        pipe.update()
        if pipe.x < -pipe.width:
            pipes.remove(pipe)

    # Check for collisions
    if bird.rect.bottom >= screen_height:
        game_over = True

    for pipe in pipes:
        if bird.rect.colliderect(pipe.top_pipe_rect) or bird.rect.colliderect(pipe.bottom_pipe_rect):
            game_over = True

    # Check if bird passes through pipe
    for pipe in pipes:
        if not pipe.passed and pipe.x < bird.x and not game_over:
            pipe.passed = True
            score += 1

    # Draw background (replace with your background image)
    screen.fill((135, 206, 250))

    # Draw pipes
    for pipe in pipes:
        screen.blit(pipe.top_pipe_image, pipe.top_pipe_rect)
        screen.blit(pipe.bottom_pipe_image, pipe.bottom_pipe_rect)

    # Draw bird
    screen.blit(bird.image, bird.rect)

    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, black)
    screen.blit(score_text, (10, 10))

    # Display game over screen
    if game_over:
        game_over_text = font.render("Game Over", True, black)
        final_score_text = font.render(f"Final Score: {score}", True, black)
        screen.blit(game_over_text, (screen_width // 2 - 60, screen_height // 2 - 30))
        screen.blit(final_score_text, (screen_width // 2 - 60, screen_height // 2 + 10))

        # Restart logic
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird = Bird()
                pipes = []
                score = 0
                game_over = False

    # Update display
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
