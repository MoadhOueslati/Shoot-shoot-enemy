import pygame

class Coins(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.original_image = pygame.image.load("pictures/Coin C.png")
        self.image = pygame.transform.scale(self.original_image, (13,13))
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.coin_pickup = pygame.mixer.Sound("music/coin_pickup.wav")
        self.value = 1
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    def update(self, enemy_speed, player, screen_height):
        self.rect.y += enemy_speed
        
        #collision detection
        if self.rect.colliderect(player.rect):
            self.coin_pickup.play()
            self.kill()
            player.coins += self.value
        
        #offscreen check
        if self.rect.y > screen_height:
            self.kill()
            