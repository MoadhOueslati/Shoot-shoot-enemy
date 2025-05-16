import pygame
import math
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define gravity parameters
GRAVITY = 0.1

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.color = (255, 0, 0)
        self.radius = 2
        self.vel_x = random.uniform(-5, 5)  # Random initial velocity in the x direction
        self.vel_y = random.uniform(-5, 5)  # Random initial velocity in the y direction
        self.lifetime = random.randint(2, 5)  # Lifetime of the particle in frames (assuming 60 FPS)
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        # Update the position of the particle
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.vel_y += GRAVITY  # Apply gravity to the y velocity
        self.lifetime -= 1  # Decrement the lifetime of the particle
        if self.lifetime <= 0:
            self.kill()  # Remove the particle from the sprite group when its lifetime expires

def main():
    pygame.init()

    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Particle System with Lifetime")

    # Create a sprite group to hold the particles
    all_sprites = pygame.sprite.Group()

    # Set up the clock
    clock = pygame.time.Clock()

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Create multiple particles at the position of the mouse click
                for _ in range(50):
                    particle = Particle(event.pos[0], event.pos[1])
                    all_sprites.add(particle)

        # Clear the screen
        screen.fill(BLACK)

        # Update and draw particles
        all_sprites.update()
        all_sprites.draw(screen)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()








############ Sinisuidalee ball moving right ##############

# import pygame
# import sys
# import math

# # Initialize Pygame
# pygame.init()

# # Set up the screen
# screen_width, screen_height = 800, 600
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption("Object Moving in a Sinusoidal Path")

# # Define colors
# WHITE = (255, 255, 255)
# RED = (255, 0, 0)

# # Main loop
# time = 0  # Initial time
# amplitude = 100  # Amplitude of the sinusoidal motion
# angular_frequency = 0.01  # Angular frequency of the sinusoidal motion
# phase_angle = 0  # Phase angle of the sinusoidal motion
# x = 0
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
    
#     # Clear the screen
#     screen.fill(WHITE)
    
#     # Calculate the y-coordinate using the sinusoidal function
#     y = screen_height // 2 + int(amplitude * math.sin(angular_frequency * time + phase_angle))
#     x += 1
    
#     # Draw the object (in this case, a circle)
#     radius = 20
#     pygame.draw.circle(screen, RED, (x, y), radius)
    
#     # Increment time for animation
#     time += 10  # Increment time to progress the animation
    
#     # Update the display
#     pygame.display.flip()
    
#     # Limit frame rate
#     pygame.time.Clock().tick(60)

# # Quit Pygame
# pygame.quit()
# sys.exit()





####################### UNIT CIRCLE ##########################
# import pygame
# import math

# # Initialize Pygame
# pygame.init()

# # Set the screen dimensions
# screen_width = 400
# screen_height = 400
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption("Circle and Bullet")

# # Define colors
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)

# # Define circle parameters
# circle_radius = 100
# circle_center = (screen_width // 2, screen_height // 2)

# # Define bullet parameters
# bullet_radius = 3
# bullet_angle = math.pi / 4  # Angle in radians

# # Main loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Clear the screen
#     screen.fill(WHITE)

#     # Draw the circle
#     pygame.draw.circle(screen, BLACK, circle_center, circle_radius, 2)

#     # Calculate the position of the bullet
#     bullet_x = circle_center[0] + int(circle_radius * math.cos(bullet_angle))
#     bullet_y = circle_center[1] + int(circle_radius * math.sin(bullet_angle))

#     # Draw the bullet
#     pygame.draw.circle(screen, RED, (bullet_x, bullet_y), bullet_radius)

#     # Update the display
#     pygame.display.flip()

# # Quit Pygame
# pygame.quit()
 