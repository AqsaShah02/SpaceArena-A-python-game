import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60
SHIP_SPEED = 5 
SCROLL_SPEED = 15  
STAR_SCORE = 15  # Points for collecting stars
ALIEN_PENALTY = 50  # Points deducted for touching aliens
BLACK_HOLE_PENALTY = 1000  # Penalty for colliding with the black hole

# Font for displaying text
font = pygame.font.Font(None, 72)  # Larger font size for splash screen
score_font = pygame.font.Font(None, 36)  # Font for scoreboard
score = 0
font = pygame.font.Font(None, 36)
score = 0

# Function to update the scoreboard
def update_scoreboard():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (100, 100))

# Function to display splash screen
def show_splash_screen():
    splash_text = font.render("WELCOME TO SPACE ARENA", True, WHITE)
    text_rect = splash_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(splash_text, text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)  # Display splash screen for 3 seconds

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Explorer")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)  # Transparent color

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

# Create background stars and comets
background_stars = []
for _ in range(300):
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    size = random.randint(1, 3)
    background_stars.append((x, y, size))

# Load star collectible image
star_image = pygame.image.load("star.png")
star_image = pygame.transform.scale(star_image, (20, 20))  # Adjust star size

# Create collectibles (stars)
stars = []
for planet in planets:
    for _ in range(30):  # Adjust the number of stars per planet as needed
        x = random.randint(planet["rect"].left, planet["rect"].right)
        y = random.randint(planet["rect"].top, planet["rect"].bottom)
        stars.append({"image": star_image, "rect": star_image.get_rect(center=(x, y))})

# Load alien images and create aliens with different sizes and speeds
alien_images = [
    pygame.transform.scale(pygame.image.load("alien1.png"), (60, 60)),
    pygame.transform.scale(pygame.image.load("alien2.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load("alien3.png"), (100, 100)),
]

# Create aliens
aliens = []
for _ in range(10):  # Adjust the number of aliens as needed
    x = random.randint(0, SCREEN_WIDTH - 100)  # Ensure within screen width
    y = random.randint(0, SCREEN_HEIGHT - 100)  # Ensure within screen height
    image = random.choice(alien_images)
    dx = random.randint(-3, 3)
    dy = random.randint(-3, 3)
    aliens.append({"image": image, "rect": image.get_rect(center=(x, y)), "dx": dx, "dy": dy})

# Load black hole image and position it
blackhole_image = pygame.image.load("blackhole.png")
blackhole_image = pygame.transform.scale(blackhole_image, (1000, 1000))  # Adjust black hole size
blackhole_rect = blackhole_image.get_rect(center=(SCREEN_WIDTH // 2, -1500))  # Position above Earth

# Clock
clock = pygame.time.Clock()

# Main loop flag
running = True

# Key holding flags
move_left = False
move_right = False
move_up = False
move_down = False

# Function to move the screen smoothly
def move_screen(dx, dy):
    for star in stars:
        star["rect"].centerx -= dx
        star["rect"].centery -= dy

    for planet in planets:
        planet["rect"].centerx -= dx
        planet["rect"].centery -= dy

    for alien in aliens:
        alien["rect"].centerx += alien["dx"]
        alien["rect"].centery += alien["dy"]

    # Move black hole
    blackhole_rect.centery -= dy

# Function to handle collisions with stars, aliens, and black hole
def handle_collisions():
    global score
    for star in stars:
        if spaceship_rect.colliderect(star["rect"]):
            score += STAR_SCORE
            # Respawn star at a new random location
            star["rect"].x = random.randint(0, SCREEN_WIDTH)
            star["rect"].y = random.randint(0, SCREEN_HEIGHT)

    for alien in aliens:
        if spaceship_rect.colliderect(alien["rect"]):
            score -= ALIEN_PENALTY
            # Respawn alien at a new random location
            alien["rect"].x = random.randint(0, SCREEN_WIDTH - 100)
            alien["rect"].y = random.randint(0, SCREEN_HEIGHT - 100)
            alien["dx"] = random.randint(-3, 3)
            alien["dy"] = random.randint(-3, 3)

    # Check collision with black hole
    if spaceship_rect.colliderect(blackhole_rect):
        score -= BLACK_HOLE_PENALTY
        # Respawn black hole at a new random location
        blackhole_rect.x = random.randint(0, SCREEN_WIDTH)
        blackhole_rect.y = random.randint(-1500, -1000)

# Display splash screen
show_splash_screen()

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

    # Handle collisions with stars, aliens, and black hole
    handle_collisions()

    # Fill the screen with black (space)
    screen.fill(BLACK)

    # Draw background stars and comets
    for star in background_stars:
        pygame.draw.circle(screen, WHITE, (star[0], star[1]), star[2])

    # Draw stars
    for star in stars:
        screen.blit(star["image"], star["rect"])

    # Draw planets
    for planet in planets:
        screen.blit(planet["image"], planet["rect"])

    # Draw aliens
    for alien in aliens:
        screen.blit(alien["image"], alien["rect"])

    # Draw black hole
    screen.blit(blackhole_image, blackhole_rect)

    # Draw spaceship
    screen.blit(spaceship, spaceship_rect)

    # Draw scoreboard (fixed position top-left)
    score_text = font.render(f"Score: {score}", True, WHITE, TRANSPARENT)
    screen.blit(score_text, (20, 20))

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
