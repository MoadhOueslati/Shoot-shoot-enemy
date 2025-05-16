import pygame
import random
import math

from utils import *
from colors import COLORS
from enemy_types import ENEMIES_TYPE

from sprites.player import Player
from sprites.enemy import Enemy 
from sprites.potion import Potions

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.current_timer = pygame.time.get_ticks()
        self.timer = pygame.time.get_ticks()
        self.count_timer = 1
        self.TIMER_INTERVAL = 1000
        
        self.FPS = 60
        self.game_over = False

        self.width = 600
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Shoot shoot enemy")
        # Load the icon
        icon = pygame.image.load("pictures/player.png")  
        # Set the icon
        pygame.display.set_icon(icon)
        
        #background music
        pygame.mixer.init()
        pygame.mixer.music.load("music/Space Race.ogg")

        #font setup
        pygame.font.init()
        self.font = pygame.font.SysFont("Roboto", 40)

        #level change interval
        self.level_interval = 20

        #bottom screen 
        self.bottom_surface_height = 100
        self.bottom_surface = pygame.Surface((self.width, self.bottom_surface_height))
        #upper screen
        self.upper_surface_height = self.height - self.bottom_surface_height
        self.upper_surface = pygame.Surface((self.width, self.upper_surface_height))

        # Background Setup
        self.bg = pygame.image.load("pictures/space_bg.png").convert()
        self.bg_height = self.bg.get_height()
        self.bg_rect = self.bg.get_rect()
        self.tiles = math.ceil(self.upper_surface_height / self.bg_height) + 1
        self.scroll = 0

        #player setup
        self.player = Player(self.width // 2, self.upper_surface_height - 30)
        #player kills
        self.kills_text = self.font.render(f"Kills : {self.player.kills}", True, COLORS.WHITE)

        # self.enemies = [self.ENEMIES_TYPE["orange"]]  dont think i need this
        self.enemy_group = pygame.sprite.Group()
        # self.enemy_amount = 2  dont think i need it 

        #bullet setup
        self.bullet_group = pygame.sprite.Group()

        #potions setup 
        self.POTIONS_TYPE = {
            "pistol" : pygame.image.load("pictures/gun1.png"),
            "heal" : pygame.image.load("pictures/heal.png"),
            "shoes" : pygame.image.load("pictures/shoes.png"),
            "gun_speed" : pygame.image.load("pictures/gun_speed.png")
        }
        self.potion_group = pygame.sprite.Group()
        self.potion_count = 2

        #coins setup
        self.coin_group = pygame.sprite.Group()

        #explosion setup
        self.explosion_group = pygame.sprite.Group()

        #particles damage setup
        self.particles_group = pygame.sprite.Group()


        self.game_state = "menu"
        self.menu_text = self.font.render("Press R to start", True, COLORS.WHITE)
        self.menu_text_rect = self.menu_text.get_rect(center=(self.width//2 , self.height//2))


    def start(self):
        pygame.init()

        while not self.game_over:
            self.current_timer = pygame.time.get_ticks()
            self.handle_events()
            if self.game_state == "menu":
                self.show_menu()
            elif self.game_state == "gameplay":
                self.update()
                self.screens_update()

            self.clock.tick(self.FPS)
        
        pygame.quit()
    
    def start_gameplay(self):
        pygame.mixer.music.stop()
        self.game_state = "gameplay"
        self.player = Player(self.width // 2, self.upper_surface_height - 30)
        self.count_timer = 1
        self.timer = pygame.time.get_ticks()
        self.enemy_amount = 2
        self.enemies = [ENEMIES_TYPE["orange"]]
        self.enemy_group.empty()
        self.potion_group.empty()
        self.coin_group.empty()
        self.bullet_group.empty()
        self.explosion_group.empty()
        self.particles_group.empty()
    
    def show_menu(self):
        self.screen.fill(COLORS.BLACK)
        self.screen.blit(self.menu_text, self.menu_text_rect)
        self.kills_rect = self.kills_text.get_rect(center = (self.width//2, self.height//2 + 50))
        self.screen.blit(self.kills_text, self.kills_rect)
        if not pygame.mixer.music.get_busy():  # Check if the music is not already playing
            pygame.mixer.music.play(-1)
        pygame.display.update()


    def update(self):
        if not self.player.alive:
            self.game_state = "menu"
            return
        #enemy shooting
        for enemy in self.enemy_group:
            #shooting cooldown
            if self.current_timer - enemy.last_shot > enemy.shooting_delay:
                bullet = enemy.shoot()
                self.bullet_group.add(bullet)
                enemy.last_shot = self.current_timer
            
            #enemy offscreen check
            if enemy.rect.y > self.upper_surface_height:
                enemy.kill()
            

        #spawn enemy horde 
        if len(self.enemy_group) == 0:            
            self.spawn_enemies()
        

        #bullet offscreen check
        for bullet in self.bullet_group:
            if bullet.owner == "player_bullet" and bullet.rect.y < 50:
                bullet.kill()

        #update timer
        if self.current_timer - self.timer > self.TIMER_INTERVAL:
            self.count_timer += 1
            self.timer = self.current_timer

            #increase level realtive to time
            if self.count_timer % self.level_interval == 0 :
                self.increase_level()


        self.bullet_group.update()
        self.collision_detect()
    
    def screens_update(self):
        #surface windows color

        self.upper_surface.fill(COLORS.BLACK)
        self.bottom_surface.fill(COLORS.BLACK)

        for i in range(0, self.tiles):
            self.upper_surface.blit(self.bg, (0, i * self.bg_height + self.scroll))

        self.scroll -= 5

        if abs(self.scroll) > self.bg_height:
            self.scroll = 0

        # Draw the border on the upper surface
        border_color = COLORS.WHITE
        border_thickness = 2
        pygame.draw.rect(self.bottom_surface, border_color, (0, 0, self.width, border_thickness))


        #draw bullet 
        self.bullet_group.draw(self.upper_surface)

        #draw player related 
        if self.player.alive:
            self.upper_surface.blit(self.player.image, self.player.rect)
            self.player.update(self.bullet_group, self.upper_surface, self.width)


        #draw enemies related
        self.enemy_group.draw(self.upper_surface)
        self.enemy_group.update(self.upper_surface)

        #draw potion related
        self.potion_group.draw(self.upper_surface)
        self.potion_group.update(self.upper_surface_height)

        #draw coins related
        self.coin_group.draw(self.upper_surface)
        self.coin_group.update(3 ,self.player, self.upper_surface_height)

        #draw explosion related
        self.explosion_group.draw(self.upper_surface)
        self.explosion_group.update()

        #draw particles damage related
        self.particles_group.draw(self.upper_surface)
        self.particles_group.update()

        #draw coins text & icon
        self.coins_text = self.font.render(f"x{self.player.coins}", True, COLORS.WHITE)
        self.bottom_surface.blit(self.coins_text, (self.bottom_surface.get_width() - self.coins_text.get_width() - 30, 40))
        self.original_coin_image = pygame.image.load("pictures/Coin C.png")
        self.coin_image = pygame.transform.scale(self.original_coin_image, (40,40))
        self.bottom_surface.blit(self.coin_image, (self.bottom_surface.get_width() - self.coins_text.get_width() - 80, 30))

        #draw kills text
        self.kills_text = self.font.render(f"Kills : {self.player.kills}", True, COLORS.WHITE)
        self.kills_rect = self.kills_text.get_rect(center = (self.kills_text.get_width() - 20, self.bottom_surface_height//2))
        self.bottom_surface.blit(self.kills_text, self.kills_rect)

        #draw timer text
        self.timer_text = self.font.render(f"{format_timer(self.count_timer)}", True, COLORS.WHITE)
        self.timer_text_rect = self.timer_text.get_rect(center= (self.bottom_surface.get_width()//2, self.bottom_surface_height//2))
        self.bottom_surface.blit(self.timer_text, self.timer_text_rect)

        # upper & bottom window draw
        self.screen.blit(self.upper_surface, (0, 0))
        self.screen.blit(self.bottom_surface, (0, self.height - self.bottom_surface_height))


        pygame.display.update()


    def collision_detect(self):
        # Enemy friendly fire check
        enemy_collisions = pygame.sprite.groupcollide(self.enemy_group, self.bullet_group, False, False)
        for enemy, bullet_list in enemy_collisions.items():
            hit_by_player_bullet = False
            for bullet in bullet_list:
                if bullet.owner == "player_bullet":
                    if not hit_by_player_bullet:
                        # Damage enemy only if not already hit by a player's bullet
                        enemy.get_damage(self.player, self.coin_group, self.explosion_group, self.particles_group)
                        hit_by_player_bullet = True
                    bullet.kill()


        if self.player.alive:
            player_collisions = pygame.sprite.spritecollide(self.player, self.bullet_group, False)
            for bullet in player_collisions:
                if bullet.owner == "enemy_bullet":
                    #damage player and kill enemy's bullet if player hit by enemy
                    self.player.get_damage()
                    bullet.kill()

        
    def spawn_enemies(self):
        for _ in range(self.enemy_amount):
            enemy_type = random.choice(self.enemies)
            enemy_shooting_delay = random.randint(enemy_type["shooting_delay"][0], enemy_type["shooting_delay"][1])
            enemy = Enemy(enemy_type, random.randint(50, self.width - 50), -random.randint(0,200), round(random.uniform(1, 2), 1), enemy_shooting_delay)
            self.enemy_group.add(enemy)

    def drop_potions(self):
        for _ in range(self.potion_count):
            potion_name = random.choice(list(self.POTIONS_TYPE.keys()))
            potion = Potions(potion_name, self.POTIONS_TYPE[potion_name], random.randint(50, self.width - 50), -random.randint(0,200), 2, self.player)
            self.potion_group.add(potion)


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN:
                if self.game_state == "menu" and event.key == pygame.K_r:
                    self.start_gameplay()
                
                
    def increase_level(self):
        #increase enemy amount
        self.enemy_amount += random.choice([1,2])

        if self.count_timer == self.level_interval * 1:
            self.enemies.append(ENEMIES_TYPE["red"])
        elif self.count_timer == self.level_interval * 2:
            self.enemies.append(ENEMIES_TYPE["yellow"])
        elif self.count_timer == self.level_interval * 3:
            self.enemies.append(ENEMIES_TYPE["blue"])
        elif self.count_timer == self.level_interval * 4:
            self.enemies.append(ENEMIES_TYPE["pink"])

        #potion drop
        self.drop_potions()

        
game = Game()
game.start()