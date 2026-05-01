import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


import pygame
import math
import random
from pygame import mixer
# Initialize Pygame
pygame.init()

# required for sound in  exe file created by pyinstaller
pygame.mixer.init()

# set up the display
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load(resource_path("background.jpg"))

# background sound
mixer.music.load(resource_path("background.wav"))
mixer.music.play(-1)

#TITLE AND ICON
# make caption of the window
pygame.display.set_caption("Space Invaders") 
icon = pygame.image.load(resource_path("ufo.png"))
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load(resource_path("space-invaders.png"))
player_x = 370
player_y = 480
playerx_change = 0

# enemy
enemyimg = []
enemy_x = []
enemy_y = []
enemyx_change = []
enemyy_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load(resource_path("enemy.png")))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemyx_change.append(0.3)
    enemyy_change.append(40)

#Ready - You can't see the bullet on the screen
#Fire - The bullet is currently moving
# bullet
bulletimg = pygame.image.load(resource_path("bullets.png"))
bullet_x = 0
bullet_y = 480
bulletx_change = 0
bullety_change = 0.4
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font(None, 32)
text_x = 10
text_y = 10

# Game over text
over_font = pygame.font.Font(None, 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    game_over = over_font.render("GAME OVER !!", True, (255, 255, 255))
    text_rect = game_over.get_rect(center=(400, 300))
    screen.blit(game_over, text_rect)

def player(x, y):
    screen.blit(playerimg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))

def isCollision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    if distance < 30:
        return True
    else:
        return False

# run the game loop
running = True
while running:
    #set background color
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if any keystroke is pressed, check whether it is left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerx_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound(resource_path("laser.wav"))
                    bullet_sound.play()
                    # get the current x coordinate of the spaceship
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
        # if the keystroke is released, stop the movement
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0 
    # player movement
    player_x += playerx_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    #enemy movement
    for i in range(num_of_enemies):

        # Game over

        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break
            

        enemy_x[i] += enemyx_change[i]
        if enemy_x[i] <= 0:
            if(score_value < 3):
                enemyx_change[i] = 0.2
            elif(score_value < 6):
                enemyx_change[i] = 0.35
            elif(score_value < 10):
                enemyx_change[i] = 0.5
            elif(score_value < 14):
                enemyx_change[i] = 0.6
            else:
                enemyx_change[i] = 0.8

            enemy_y[i] += enemyy_change[i]
        elif enemy_x[i] >= 736:
            if(score_value < 3):
                enemyx_change[i] = -0.2
            elif(score_value < 6):
                enemyx_change[i] = -0.35
            elif(score_value < 10):
                enemyx_change[i] = -0.5
            elif(score_value < 14):
                enemyx_change[i] = -0.6
            else:
                enemyx_change[i] = -0.8
            enemy_y[i] += enemyy_change[i]

        #collision
        collision = isCollision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound(resource_path("explosion.wav"))
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)

    #bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullety_change
    
    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()

    

pygame.quit()