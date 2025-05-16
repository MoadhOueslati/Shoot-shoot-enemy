import pygame
import random


# Define gravity parameters
GRAVITY = 0.1

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.color = color
        self.radius = 4
        self.vel_x = random.uniform(-5, 5)  # Random initial velocity in the x direction
        self.vel_y = random.uniform(-5, 5)  # Random initial velocity in the y direction
        self.lifetime = random.randint(12, 20)  # Lifetime of the particle in frames (assuming 60 FPS)
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
