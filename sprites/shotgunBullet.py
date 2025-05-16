import pygame
from colors import COLORS

class ShotgunBullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, speed_x, speed_y, owner, bullet_color):
        super().__init__()
        self.image = pygame.Surface((10, 15))
        self.image.fill(getattr(COLORS, bullet_color.upper()))
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.owner = owner
        self.speed_x = speed_x
        self.speed_y = speed_y
    
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
