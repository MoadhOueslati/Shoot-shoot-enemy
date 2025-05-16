import pygame
from colors import COLORS

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, speed, owner, bullet_color):
        super().__init__()
        self.image = pygame.Surface((10, 15))
        self.image.fill(getattr(COLORS, bullet_color.upper()))
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.pos_x = pos_x
        self.owner = owner
        self.speed = speed

    def update(self):
        self.rect.y += self.speed


