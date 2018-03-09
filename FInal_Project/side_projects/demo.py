import pygame
import time
from random import randrange, randint

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

clock = pygame.time.Clock()

# utworzenie okna
display_width = 800
display_heigth = 600
gameDisplay = pygame.display.set_mode((display_width, display_heigth))
pygame.display.set_caption("Snake")

img = pygame.image.load('head.png')

pygame.display.update()

block_size = 20
FPS = 10

direction = "right"

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largfont = pygame.font.SysFont("comicsansms", 75)

# def game_intro():
#     intro = True
#
#     while intro:
#         gameDisplay.fill(white)
#         message_to_screen("Welcome to Snake", green, -100, largfont)
#
#
#     pygame.display.update()
#     clock.tick(15)

def snake(block_size, snakelist):
    if direction == 'right':
        head = pygame.transform.rotate(img, 270)

    if direction == 'left':
        head = pygame.transform.rotate(img, 90)

    if direction == 'up':
        head = img

    if direction == 'down':
        head = pygame.transform.rotate(img, 180)

    gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))

    for XnY in snakelist[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block_size, block_size])


def text_objects(text, color, size):
    if size == "small":
        text_surface = smallfont.render(text, True, color)
    elif size == "medium":
        text_surface = medfont.render(text, True, color)
    elif size == "large":
        text_surface = largfont.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_to_screen(msg, color, y_displace=0, size="small"):

    text_surface, text_rect = text_objects(msg, color, size)
    text_rect.center = (display_width / 2), (display_width / 2) + y_displace
    gameDisplay.blit(text_surface, text_rect)


def gameLoop():
    global direction
    gameExit = False
    gameOver = False

    lead_x = round((display_width / 2) / 10.0) * 10.0
    lead_y = round((display_heigth / 2) / 10.0) * 10.0
    lead_x_change = 10
    lead_y_change = 0

    x_block = display_width / block_size
    y_block = display_heigth / block_size

    randAppleX = randint(0, x_block) * block_size
    randAppleY = randint(0, y_block) * block_size

    snakelist = []
    snakeLength = 1

    while not gameExit:

        while gameOver == True:
            gameDisplay.fill(white)
            message_to_screen("Game over", red, -50, size="large")
            message_to_screen("Pres C to play again or Q to quit", black)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = False
                gameExit = True

            # Snake movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = 'left'
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction = 'right'
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = 'up'
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = 'down'
                    lead_y_change = block_size
                    lead_x_change = 0

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -10
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = 10
                elif event.key == pygame.K_UP:
                    lead_y_change = -10
                elif event.key == pygame.K_DOWN:
                    lead_y_change = 10



        # Aoutside border Game Over
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_width or lead_y < 0:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.fill(white)

        #   draw apple
        applethickness = 22
        pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, applethickness, applethickness])
        #   draw snake

        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakelist.append(snakeHead)

        if len(snakelist) > snakeLength:
            del snakelist[0]

        for eachsegment in snakelist[:-1]:
            if eachsegment == snakeHead:
                gameOver = True

        snake(block_size, snakelist)

        pygame.display.update()
        #   Genarate new apple

        # Colision
        # if lead_x >= randAppleX and lead_x <= randAppleX + applethickness:
        #     if lead_y >= randAppleY and lead_y <= randAppleY + applethickness:
        #         randAppleX = randint(0, x_block) * block_size
        #         randAppleY = randint(0, y_block) * block_size
        #         snakeLength += 1

        if lead_x > randAppleX and lead_x < randAppleX + applethickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + applethickness:
            # print("x cros over")
            if lead_y > randAppleY and lead_y < randAppleY + applethickness or lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + applethickness:
                randAppleX = randint(0, x_block) * block_size
                randAppleY = randint(0, y_block) * block_size
                snakeLength += 1

        clock.tick(FPS)

    pygame.quit()
    quit()


gameLoop()
