import pygame
import random
import math

pygame.init()

# screen
screen_size = [800, 600]
screen = pygame.display.set_mode(screen_size)

# caption, icon
pygame.display.set_caption("Space game")
icon = pygame.image.load("icone.png")
pygame.display.set_icon(icon)

# background
background = pygame.image.load("247.jpg")
background = pygame.transform.scale(background, screen_size)

# player
player = pygame.image.load("player.png")
player = pygame.transform.scale(player, (100, 100))
playerX = 370
playerY = 480
player_position_change = 0

# enemy
enemy = []
enemyX = []
enemyY = []
enemyX_position_change = []
enemyY_position_change = []
number_of_enemy = 7
for i in range(number_of_enemy):
    enemy.append(pygame.transform.scale(pygame.image.load("enemy.png"), (100, 100)))
    enemyX.append(random.randint(0, 700))
    enemyY.append(random.randint(50, 150))
    enemyX_position_change.append(3)
    enemyY_position_change.append(40)

# bullet
bullet = pygame.image.load("bullet.png")
bullet = pygame.transform.scale(bullet, (30, 30))
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 15
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font("Platinum Sign Over.ttf", 32)
textX = 10
textY = 10

# game over
over_font = pygame.font.Font("Platinum Sign.ttf", 45)

# music
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)


def player_function(x, y):
    screen.blit(player, (x, y))


def enemy_function(x, y, i):
    screen.blit(enemy[i], (x, y))


def bullet_function(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 38, y + 10))


# collision
def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((enemyX - bulletX), 2) + math.pow((enemyY - bulletY), 2))
    if distance < 27:
        return True
    else:
        return False


def show_score(x, y):
    score = font.render("SCORE - " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    over_text = over_font.render("GAME  OVER !  " , True, (255, 255, 255))
    screen.blit(over_text, (50, 250))


# game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_position_change = -5
            if event.key == pygame.K_RIGHT:
                player_position_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = pygame.mixer.Sound('bullet.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bullet_function(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_position_change = 0
    # boundaries for player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 700:
        playerX = 700

    # enemy movement
    for i in range(number_of_enemy):
        # game over
        if enemyY[i] > 400:
            game_over()
            break

        enemyX[i] += enemyX_position_change[i]
        if enemyX[i] <= 0:
            enemyX_position_change[i] = 2
            enemyY[i] += enemyY_position_change[i]
        elif enemyX[i] >= 700:
            enemyX_position_change[i] = -2
            enemyY[i] += enemyY_position_change[i]

        # collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            sound = pygame.mixer.Sound("collision_sound.wav")
            sound.play()
            bulletY = 480
            bullet_state = "ready"
            enemyX[i] = random.randint(0, 700)
            enemyY[i] = random.randint(50, 150)
            score_value += 1
        enemy_function(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        bullet_function(bulletX, bulletY)
        bulletY -= bulletY_change

    playerX += player_position_change
    player_function(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
