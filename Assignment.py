import pygame
import random
import cv2
import numpy as np

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 400, 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BASKET_WIDTH, BASKET_HEIGHT = 60, 20
OBJECT_SIZE = 20
OBJECT_FALL_SPEED = 5
BASKET_SPEED = 10

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Catch the Falling Objects')

# Define the Basket class
class Basket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BASKET_WIDTH, BASKET_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT - BASKET_HEIGHT

    def move(self, dx):
        self.rect.x += dx
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > WIDTH - BASKET_WIDTH:
            self.rect.x = WIDTH - BASKET_WIDTH

# Define the FallingObject class
class FallingObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((OBJECT_SIZE, OBJECT_SIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - OBJECT_SIZE)
        self.rect.y = -OBJECT_SIZE

    def fall(self):
        self.rect.y += OBJECT_FALL_SPEED
        if self.rect.y > HEIGHT:
            self.kill()

# Create sprite groups
all_sprites = pygame.sprite.Group()
falling_objects = pygame.sprite.Group()

# Create basket
basket = Basket()
all_sprites.add(basket)

# AI Control Function
def ai_control():
    # Capture the game screen
    game_screen = pygame.surfarray.array3d(pygame.display.get_surface())
    game_screen = np.transpose(game_screen, (1, 0, 2))  # Convert to (height, width, channels)
    gray = cv2.cvtColor(game_screen, cv2.COLOR_RGB2GRAY)

    # Thresholding and object detection
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any falling object is detected
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if y > HEIGHT // 2:  # If object is in the lower half of the screen
            if x < basket.rect.x:
                basket.move(-BASKET_SPEED)
            elif x + w > basket.rect.x + BASKET_WIDTH:
                basket.move(BASKET_SPEED)

# Game loop
running = True
clock = pygame.time.Clock()
score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement (manual control disabled for AI)
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_LEFT]:
    #     basket.move(-BASKET_SPEED)
    # if keys[pygame.K_RIGHT]:
    #     basket.move(BASKET_SPEED)

    # AI control
    ai_control()

    # Create new falling objects
    if random.randint(1, 20) == 1:
        obj = FallingObject()
        all_sprites.add(obj)
        falling_objects.add(obj)

    # Update object positions
    for obj in falling_objects:
        obj.fall()

    # Check for collisions
    for obj in falling_objects:
        if pygame.sprite.collide_rect(basket, obj):
            obj.kill()
            score += 1

    # Draw everything
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Display the score
    font = pygame.font.SysFont(None, 36)
    text = font.render(f'Score: {score}', True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

pygame.quit()


