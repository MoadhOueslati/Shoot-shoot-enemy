import pygame
import math
from sprites.bullet import Bullet
from sprites.healthbar import HealthBar
from sprites.shotgunBullet import ShotgunBullet

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.alive = True
        self.original_image = pygame.image.load("pictures/player.png")
        self.image = pygame.transform.scale(self.original_image, (40, 40))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.speed = 4
        self.bullet_speed = 10
        self.hp = HealthBar(self.width * 2, 10)
        self.health = 100
        self.kills = 0
        self.coins = 0
        self.bullet_type = 'pistol'
        self.bullet_color = "white"
        
        self.last_shot = pygame.time.get_ticks()
        self.shooting_interval = 300
        self.shoot_sound = pygame.mixer.Sound("music/player_shoot.wav")
        self.hit_sound = pygame.mixer.Sound("music/player_hit.wav")

    def shoot(self):
        if self.bullet_type == "pistol":
            bullet_x = self.rect.centerx
            bullet_y = self.rect.centery
            bullet = Bullet(bullet_x, bullet_y, -self.bullet_speed, "player_bullet", self.bullet_color)
            return bullet
        
        elif self.bullet_type == "shotgun":
            bullets = []
            num_bullets = 6
            spread_angle = 18
            angle_increment = spread_angle / (num_bullets - 1)

            for i in range(num_bullets):
                bullet_x = self.rect.centerx
                bullet_y = self.rect.centery
                angle = math.radians(spread_angle // 2 - i * angle_increment) - math.pi/2
                bullet = ShotgunBullet(bullet_x, bullet_y, self.bullet_speed * math.cos(angle), self.bullet_speed * math.sin(angle), "player_bullet", self.bullet_color)
                bullets.append(bullet)
            return bullets

  
    def update(self, bullet_group, surface, screen_width):
        self.hp.draw(self.rect.x - 20, self.rect.y - 10, surface, self.health)
        if self.alive:            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] and self.rect.x + self.width < screen_width - 30:
                self.rect.x += self.speed
            if keys[pygame.K_LEFT] and self.rect.x > 30:
                self.rect.x -= self.speed
            if keys[pygame.K_SPACE]:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_shot > self.shooting_interval:
                    bullet = self.shoot()
                    bullet_group.add(bullet)
                    self.last_shot = current_time
                    self.shoot_sound.play()

    def get_damage(self):
        self.hit_sound.play()
        self.health -= 5
        if self.health <= 0:
            self.alive = False
    
    def use_potion(self, name):
        if name == "heal":
            if self.health < 100:
                self.health = 100
        
        elif name == "shoes":
            if self.speed < 10:
                self.speed += 1
            
        elif name == "pistol":
            self.bullet_type = "shotgun"

        elif name == "gun_speed":
            if self.shooting_interval > 80:
                self.shooting_interval -= 30

 