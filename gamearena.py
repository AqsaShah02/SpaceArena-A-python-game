import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60
SHIP_SPEED = 15  # Adjust spaceship speed
SCROLL_SPEED = 15  # Speed of smooth scrolling

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Explorer")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Load spaceship image
spaceship = pygame.image.load("spaceship.png")
spaceship = pygame.transform.scale(spaceship, (80, 80))  # Adjust spaceship size
spaceship_rect = spaceship.get_rect()
spaceship_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Load planet images and set initial positions based on scaled distances
initial_planet_positions = [
    {"name": "mercury", "image": "mercury.png", "distance": 50, "size": 500},
    {"name": "venus", "image": "venus.png", "distance": 100, "size": 800},
    {"name": "earth", "image": "earth.png", "distance": 150, "size": 900},
    {"name": "mars", "image": "mars.png", "distance": 200, "size": 600},
    {"name": "jupiter", "image": "jupiter.png", "distance": 300, "size": 1600},
    {"name": "saturn", "image": "saturn.png", "distance": 400, "size": 1400},
    {"name": "uranus", "image": "uranus.png", "distance": 500, "size": 1000},
    {"name": "neptune", "image": "neptune.png", "distance": 600, "size": 1000},
    {"name": "pluto", "image": "pluto.png", "distance": 700, "size": 500},
]

# Adjust planet positions based on initial distances
planets = []
for idx, planet_data in enumerate(initial_planet_positions):
    x_pos = sum(p["distance"] for p in initial_planet_positions[:idx]) + (idx * SCREEN_WIDTH // 2)
    y_pos = SCREEN_HEIGHT // 2
    planet_image = pygame.image.load(planet_data["image"])
    planet_image = pygame.transform.scale(planet_image, (planet_data["size"], planet_data["size"]))
    planet_rect = planet_image.get_rect(center=(x_pos, y_pos))
    planets.append({"image": planet_image, "rect": planet_rect})

# Create background stars
stars = []
for _ in range(200):
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    stars.append((x, y))

# Function to move the screen smoothly
def move_screen(dx, dy):
    for planet in planets:
        planet["rect"].x -= dx
        planet["rect"].y -= dy

# Clock
clock = pygame.time.Clock()

# Main loop flag
running = True

# Key holding flags
move_left = False
move_right = False
move_up = False
move_down = False

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT:
                move_left = True
            elif event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_UP:
                move_up = True
            elif event.key == pygame.K_DOWN:
                move_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False
            elif event.key == pygame.K_UP:
                move_up = False
            elif event.key == pygame.K_DOWN:
                move_down = False

    # Smooth scrolling based on key holding
    scroll_dx = SCROLL_SPEED if move_right else -SCROLL_SPEED if move_left else 0
    scroll_dy = SCROLL_SPEED if move_down else -SCROLL_SPEED if move_up else 0
    move_screen(scroll_dx, scroll_dy)

    # Update spaceship position based on key presses
    if move_left and spaceship_rect.left > 0:
        spaceship_rect.x -= SHIP_SPEED
    if move_right and spaceship_rect.right < SCREEN_WIDTH:
        spaceship_rect.x += SHIP_SPEED
    if move_up and spaceship_rect.top > 0:
        spaceship_rect.y -= SHIP_SPEED
    if move_down and spaceship_rect.bottom < SCREEN_HEIGHT:
        spaceship_rect.y += SHIP_SPEED

    # Ensure spaceship stays within screen boundaries
    spaceship_rect.clamp_ip(screen.get_rect())

    # Fill the screen with black (space)
    screen.fill(BLACK)

    # Draw stars
    for star in stars:
        pygame.draw.circle(screen, WHITE, star, 2)

    # Draw planets
    for planet in planets:
        screen.blit(planet["image"], planet["rect"])

    # Draw spaceship
    screen.blit(spaceship, spaceship_rect)

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
