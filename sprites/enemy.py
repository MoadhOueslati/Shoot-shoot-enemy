import pygame
import random
import math

from sprites.bullet import Bullet
from sprites.healthbar import HealthBar
from sprites.coins import Coins
from sprites.explosion import Explosion
from sprites.shotgunBullet import ShotgunBullet
from sprites.particles import Particle


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type , pos_x , pos_y, speed, shooting_delay):
        super().__init__()
        self.enemy_type = enemy_type
        self.original_image = self.enemy_type["image"]
        self.image = pygame.transform.scale(self.original_image, (35,35))
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.hp = HealthBar(self.image.get_width() * 2, 8)
        self.health = 100
        self.speed = speed
        self.bullet_speed = 10
        self.bullet_type = self.enemy_type["bullet_type"]
        self.bullet_color = self.enemy_type["bullet_color"]
        self.last_shot = pygame.time.get_ticks()
        self.shooting_delay = shooting_delay  # not used yet
        self.shoot_music = pygame.mixer.Sound("music/enemy_shoot.wav")
        self.hit_music = pygame.mixer.Sound("music/enemy_hit.wav")
        self.explosion_music = pygame.mixer.Sound("music/enemy_explosion.wav")

    def update(self, surface):
        self.rect.y += self.speed
        self.hp.draw(self.rect.x - 20, self.rect.y - 10, surface, self.health)

    def shoot(self):
        self.shoot_music.play()
        if self.bullet_type == "pistol":
            bullet_x = self.rect.centerx
            bullet_y = self.rect.centery
            bullet = Bullet(bullet_x, bullet_y, self.bullet_speed, "enemy_bullet", self.bullet_color)
            return bullet
        if self.bullet_type == "shotgun":
            bullets = []
            num_bullets = self.enemy_type["num_bullets"]
            spread_angle = num_bullets * 3
            angle_increment = spread_angle / (num_bullets - 1)

            for i in range(num_bullets):
                bullet_x = self.rect.centerx
                bullet_y = self.rect.centery
                angle = math.radians(spread_angle // 2 - i * angle_increment) + math.pi/2
                bullet = ShotgunBullet(bullet_x, bullet_y, self.bullet_speed * math.cos(angle), self.bullet_speed * math.sin(angle), "enemy_bullet", self.bullet_color)
                bullets.append(bullet)
            return bullets

    def drop_coin(self, coin_group):
        coin_amount = random.randint(0, 5)
        for _ in range(coin_amount):
            coin_pos_x = self.rect.centerx + random.randint(-20,20)
            coin_pos_y = self.rect.centery + random.randint(-20,20)
            coins = Coins(coin_pos_x, coin_pos_y)
            coin_group.add(coins)

    def get_damage(self, player, coin_group, explosion_group, particles_group):
        # if self.health > 0 :
        # for _ in range(20):
        #     particle = Particle(self.rect.centerx, self.rect.centery + 10)
        #     particles_group.add(particle)

        self.hit_music.play()
        self.health -= 30
        if self.health <= 0:
            self.kill()
            self.drop_coin(coin_group)
            self.explosion_music.play()
            for _ in range(20):
                particle = Particle(self.rect.centerx, self.rect.centery + 10, color=self.enemy_type["color"])
                particles_group.add(particle)

            # explosion = Explosion(self.rect.centerx, self.rect.centery)
            # explosion_group.add(explosion)
            player.kills += 1
    
    
            
        