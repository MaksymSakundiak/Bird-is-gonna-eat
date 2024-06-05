import pygame, sys, random
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_a, K_d, K_w, K_s, K_ESCAPE, K_x, K_m

pygame.init()
mainClock = pygame.time.Clock()

# Window
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Sprites and Sounds')

# Colors
WHITE = (255, 255, 255)

# Set up block data structure
player = pygame.Rect(300, 100, 40, 40)

playerImage = pygame.image.load('bird.png')
playerStretchedImage = pygame.transform.scale(playerImage, (40, 40))
foodImage = pygame.image.load('cherry.png')
foodStretchedImage = pygame.transform.scale(foodImage, (40, 40))
foodCounter = 0
NEWFOOD = 40
FOODSIZE = 20
foods = []
for i in range(20):
    foods.append(
        pygame.Rect(random.randint(0, WINDOWWIDTH - FOODSIZE),
                    random.randint(0, WINDOWHEIGHT - FOODSIZE), FOODSIZE,
                    FOODSIZE))
moveLeft = False
moveRight = False
moveUp = False
moveDown = False
MOVESPEED = 6

# Set up the music
pickUpSound = pygame.mixer.Sound('music2.mp3')
pygame.mixer.music.load('music2.mp3')
pygame.mixer.music.play(-1, 0.0)
musicPlaying = True

# Score counter
score = 0
font = pygame.font.SysFont(None, 36)

timer = 0
timer_font = pygame.font.SysFont(None, 36)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == K_a:
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == K_d:
                moveLeft = False
                moveRight = True
            if event.key == K_UP or event.key == K_w:
                moveDown = False
                moveUp = True
            if event.key == K_DOWN or event.key == K_s:
                moveUp = False
                moveDown = True
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == K_a:
                moveLeft = False
            if event.key == K_RIGHT or event.key == K_d:
                moveRight = False
            if event.key == K_UP or event.key == K_w:
                moveUp = False
            if event.key == K_DOWN or event.key == K_s:
                moveDown = False
            if event.key == K_x:
                player.top = random.randint(0, WINDOWHEIGHT - player.height)
                player.left = random.randint(0, WINDOWWIDTH - player.width)
            if event.key == K_m:
                if musicPlaying:
                    pygame.mixer.music.stop()
                else:
                    pygame.mixer.music.play(-1, 0.0)
                musicPlaying = not musicPlaying
        if event.type == pygame.MOUSEBUTTONUP:
            foods.append(
                pygame.Rect(event.pos[0], event.pos[1], FOODSIZE, FOODSIZE))

    foodCounter += 1

    if foodCounter >= NEWFOOD:
        foodCounter = 0
        foods.append(
            pygame.Rect(random.randint(0, WINDOWWIDTH - FOODSIZE),
                        random.randint(0, WINDOWHEIGHT - FOODSIZE), FOODSIZE,
                        FOODSIZE))

    windowSurface.fill(WHITE)

    if moveDown and player.bottom < WINDOWHEIGHT:
        player.top += MOVESPEED
    if moveUp and player.top > 0:
        player.top -= MOVESPEED
    if moveLeft and player.left > 0:
        player.left -= MOVESPEED
    if moveRight and player.right < WINDOWWIDTH:
        player.right += MOVESPEED

    windowSurface.blit(playerStretchedImage, player)

    for food in foods[:]:
        if player.colliderect(food):
            foods.remove(food)
            player = pygame.Rect(player.left, player.top, player.width + 2,
                                 player.height + 2)
            playerStretchedImage = pygame.transform.scale(
                playerImage, (player.width, player.height))
            if musicPlaying:
                pickUpSound.play()
            score += 1

    for food in foods:
        windowSurface.blit(foodStretchedImage, food)

    # Display the score
    score_display = font.render('Score: {}'.format(score), True, (0, 0, 0))
    windowSurface.blit(score_display, (10, 10))

    timer += 1
    timer_display = timer_font.render('Time: {}s'.format(timer // 40), True, (0, 0, 0))
    windowSurface.blit(timer_display, (10, 40))
    pygame.display.update()

    pygame.display.update()
    mainClock.tick(40)
