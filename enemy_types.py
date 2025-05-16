import pygame

ENEMIES_TYPE = {
    "orange": {"color" : "orange", "image": pygame.image.load("pictures/orange_enemy.png"), "bullet_type": "pistol", "bullet_color" : "orange", "shooting_delay" : (2000, 3000)},
    "red": {"color" : "red", "image": pygame.image.load("pictures/red_enemy.png"), "bullet_type": "pistol", "bullet_color" : "red", "shooting_delay" : (1500, 2500)},
    "yellow": {"color" : "yellow", "image": pygame.image.load("pictures/yellow_enemy.png"), "bullet_type": "pistol", "bullet_color" : "yellow", "shooting_delay" : (1000,2000)},
    "blue": {"color" : "blue", "image": pygame.image.load("pictures/blue_enemy.png"), "bullet_type": "shotgun", "num_bullets": 2, "bullet_color" : "blue", "shooting_delay" : (1500, 2500)},
    "pink": {"color" : "pink", "image": pygame.image.load("pictures/pink_enemy.png"), "bullet_type": "shotgun", "num_bullets": 4, "bullet_color" : "pink", "shooting_delay" : (2000, 2500)}
}
