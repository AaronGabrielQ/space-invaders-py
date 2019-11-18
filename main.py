import pygame
import random
import math
from pygame import mixer


# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load("background.png")

# Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 500
player_changeX = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemy_changeX = []
enemy_changeY = []
enemy_qty = 6

for i in range(enemy_qty):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(0,150))
    enemy_changeX.append(1.5)
    enemy_changeY.append(40)

# Bullet (Ready, Fire)
# Ready - You can't see the bullet on screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 490
bullet_changeX = 0
bullet_changeY = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over
gover_font = pygame.font.Font('freesansbold.ttf', 64)

# Functions

def showScore(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImg, (playerX, playerY))

def enemy(x, y):
    screen.blit(enemyImg[i], (enemyX[i], enemyY[i]))

def fireBullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.hypot(enemyX - bulletX, enemyY - bulletY)
    if distance < 27:
        return True
    else:
        return False

def gameOver():
    gover_text = gover_font.render("GAME OVER", True, (255,255,255))
    screen.blit(gover_text, (200, 250))

# Game Loop
running = True
while running:
    
    screen.fill((0, 0, 0))
    screen.blit(background,(0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_changeX = -2.5
            if event.key == pygame.K_RIGHT:
                player_changeX = 2.5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound("laser.wav")
                    bullet_Sound.play()
                    bulletX = playerX
                    fireBullet(playerX, bulletY)
                

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player_changeX = 0
    
    # Checking for boundaries
    playerX = playerX + player_changeX
    if playerX <= 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    # Enemy movement 
    for i in range(enemy_qty):

        if enemyY[i] > 300:
            for j in range(enemy_qty):
                enemyY[j] = 1000
            gameOver()
            break

        enemyX[i] = enemyX[i] + enemy_changeX[i]
        if enemyX[i] <= 0:
            enemy_changeX[i] = 1.5
            enemyY[i] = enemyY[i] + enemy_changeY[i]
        elif enemyX[i] > 736:
            enemy_changeX[i] = -1.5
            enemyY[i] = enemyY[i] + enemy_changeY[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound("explosion.wav")
            explosion_Sound.play()
            bulletY = 490
            bullet_state = "ready"
            score_value = score_value + 1
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(0,150)

        enemy(enemyX[i], enemyY[i])
    
    # Bullet Movement
    if bullet_state is "fire":
        bulletY = bulletY - bullet_changeY
        screen.blit(bulletImg, (bulletX, bulletY))
        if bulletY <= 0:
            bulletY = 490
            bullet_state = "ready"

    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()
