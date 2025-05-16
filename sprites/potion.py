import pygame

class Potions(pygame.sprite.Sprite):
    def __init__(self, name, image, pos_x, pos_y, speed, target):
        super().__init__()
        self.name = name
        self.target = target
        self.original_image = image
        self.image = pygame.transform.scale(self.original_image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.speed = speed
        self.use_potion = pygame.mixer.Sound("music/potion_use.wav")


    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, screen_height):
        self.rect.y += self.speed

        #collisions detection 
        if self.rect.colliderect(self.target.rect):
            self.use_potion.play()
            self.kill()
            self.target.use_potion(self.name)
        
        #offscreen check
        if self.rect.y > screen_height:
            self.kill()

        