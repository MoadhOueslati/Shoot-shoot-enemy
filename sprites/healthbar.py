import pygame
from colors import COLORS


class HealthBar(pygame.sprite.Sprite):
    def __init__(self,  width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.green_rect = pygame.Rect(0, 0, self.width, self.height)
        self.red_rect = pygame.Rect(0, 0, self.width, self.height)
        self.border_rect = pygame.Rect(0, 0, self.width, self.height)
        self.max = 100
    
    def draw(self, x, y, surface, health):
        self.green_rect.bottomleft = (x, y)
        self.red_rect.bottomleft = (x, y)
        self.border_rect.bottomleft = (x, y)
        #updating green box
        self.green_rect.width = self.width * (health / 100)

        pygame.draw.rect(surface, COLORS.RED, self.red_rect)
        pygame.draw.rect(surface, COLORS.GREEN, self.green_rect)
        pygame.draw.rect(surface, COLORS.WHITE, self.border_rect, 1)
