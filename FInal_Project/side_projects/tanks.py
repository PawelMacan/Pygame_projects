import pygame
import random
import os.path
from side_projects.maps import level

main_dir = os.path.split(os.path.abspath(__file__))[0]


class Enemy(object):

    def __init__(self, dir_x,dir_y):
        self.alive = True
        rand_loc = random.randint(0, screen_width - 64)
        rand_loc_2 = random.randint(0, screen_height - 180)

        self.rect = pygame.Rect(rand_loc, rand_loc_2, 16, 16)
        self.dir_x = dir_x
        self.dir_y = dir_y

    def move_single_axis(self):
        enemy_direction_x = 2
        self.rect.x += self.dir_x
        self.rect.y += self.dir_y

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if self.dir_x > 0:
                    self.rect.right = wall.rect.left
                if self.dir_x < 0:
                    self.rect.left = wall.rect.right
                if self.dir_y > 0:
                    self.rect.bottom = wall.rect.top
                if self.dir_y < 0:
                    self.rect.top = wall.rect.bottom

    def distroy(self):
        self.alive = False


class Player(object):
    def __init__(self):
        # pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((16, 16))
        # self.image.fill(green)
        # self.rect = self.image.get_rect()
        # self.rect.centerx = screen_width / 2
        # self.rect.bottom = screen_height /2
        # self.speedx = 5


        self.rect = pygame.Rect(32, 32, 16, 16)

        # self.speedx = 0
        # self.speedy = 0

    def move(self, direction_x, direction_y):

        if direction_x != 0:
            self.move_single_axis(direction_x, 0)
        if direction_y != 0:
            self.move_single_axis(0, direction_y)





    def move_single_axis(self, direction_x, direction_y):

        self.rect.x += direction_x
        self.rect.y += direction_y

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if direction_x > 0:
                    self.rect.right = wall.rect.left
                if direction_x < 0:
                    self.rect.left = wall.rect.right
                if direction_y > 0:
                    self.rect.bottom = wall.rect.top
                if direction_y < 0:
                    self.rect.top = wall.rect.bottom

    def shoot(self, direction_x, direction_y):
        global bulets
        bulets.append(Bulet(self.rect.x, self.rect.y, direction_x, direction_y))

    # def shoot(self):
    #     bullet = Bulet(self.rect.centerx, self.rect.top)
    #     # all_sprites.add(bullet)
    #     bulets.add(bullet)

class Bulet():
    def __init__(self, x, y, direction_x, direction_y):
        # pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((10, 20))
        # self.image.fill(green)
        # self.rect = self.image.get_rect()
        # self.rect.bottom = screen_width
        # self.rect.centerx = 0
        # self.speed = 10


        self.bulet = pygame.image.load('bulet')
        self.rect = pygame.Rect(x, y,8 ,8 )
        self.x = x
        self.y = y
        self.direction_x = direction_x
        self.direction_y = direction_y

    def update(self):
        self.rect.x += self.direction_x *5
        self.rect.y += self.direction_y *5


# Nice class to hold a wall rect
class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

def text_objects(text, color, size):
    if size == "small":
        text_surface = smallfont.render(text, True, color)
    elif size == "medium":
        text_surface = medfont.render(text, True, color)
    elif size == "large":
        text_surface = largfont.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_to_screen(msg, color, x_displace=0, size="small"):
    text_surface, text_rect = text_objects(msg, color, size)
    text_rect.center = (screen_height -450) + x_displace, (screen_width -240)
    screen.blit(text_surface, text_rect)


class dummysound:
    def play(self): pass


def load_sound(file):
    if not pygame.mixer: return dummysound()
    file = os.path.join(main_dir, 'data', file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print ('Warning, unable to load, %s' % file)
    return dummysound()


pygame.init()

pygame.display.set_caption("Tanks")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)
yelow = (255, 255, 0)

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largfont = pygame.font.SysFont("comicsansms", 75)

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))


clock = pygame.time.Clock()
walls = []  # List to hold the walls

bulets = []
player = Player()  # Create the player
enemy = Enemy(-2,0)

bulet_x = 2
bulet_y = 0

kills = 0

img_tank = pygame.image.load('tank1.png')
enem_tank_img = pygame.image.load('tank2.png')
bulet_img = pygame.image.load('pixel_bulet.png')
brick = pygame.image.load('brick.png')

enem_tank = enem_tank_img
tank = img_tank



# all_sprites = pygame.sprite.Group()
# all_sprites.add(player)
BackGround = Background('background1.png', [0, 0])

x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == "E":
            end_rect = pygame.Rect(x, y, 16, 16)
        x += 16
    y += 16
    x = 0



if pygame.mixer:
    music = os.path.join(main_dir, 'data', 'house_lo.wav')
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)


if pygame.mixer and not pygame.mixer.get_init():
    print('Warning, no sound')
    pygame.mixer = None


if pygame.mixer:
    music = os.path.join(main_dir, 'data', 'house_lo.wav')
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)
running = True
while running:
    clock.tick(32)




    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False



    # Movement

    # for event in pygame.event.get():
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_LEFT:
    #             player.move(-2, 0)
    #         if event.key == pygame.K_RIGHT:
    #             player.move(2, 0)
    #         if event.key == pygame.K_UP:
    #             player.move(0, -2)
    #         if event.key == pygame.K_DOWN:
    #             player.move(0, 2)


    key = pygame.key.get_pressed()
    direction_x = 0
    direction_y = 0
    if key[pygame.K_LEFT]:
        tank = pygame.transform.rotate(img_tank, 180)
        direction_x = -4
    if key[pygame.K_RIGHT]:
        tank = img_tank
        direction_x = 4
    if key[pygame.K_UP]:
        tank = pygame.transform.rotate(img_tank, 90)
        direction_y = -4
    if key[pygame.K_DOWN]:
        tank = pygame.transform.rotate(img_tank, 270)
        direction_y = 4

    if direction_x != 0:
        bulet_x = direction_x
        bulet_y = 0

    if direction_y != 0:
        bulet_y = direction_y
        bulet_x = 0
    player.move(direction_x, direction_y)

    if key[pygame.K_SPACE]:
        player.shoot(bulet_x, bulet_y)


    # Draw the scene
    screen.fill((0, 0, 0))
    screen.blit(BackGround.image, BackGround.rect)
    for wall in walls:
        screen.blit(brick, wall.rect)
        #pygame.draw.rect(screen, (255, 255, 255), wall.rect)
    pygame.draw.rect(screen, black, end_rect)

    #pygame.draw.rect(screen, (255, 200, 0), player.rect)

    screen.blit(tank, player.rect)


    if enemy.alive:
        screen.blit(enem_tank, enemy.rect)
        #pygame.draw.rect(screen, red, enemy.rect)
        enemy.move_single_axis()
    else:
        kills += 1
        dir_x = random.randint(-2,2)
        dir_y = random.randint(-2,2)
        enemy = Enemy(dir_x, dir_y)
        #enem_tank_img
        if dir_x < 0 :
            enem_tank = pygame.transform.rotate(enem_tank_img, 180)
        if dir_x > 0 :
            enem_tank = enem_tank_img
        if dir_y < 0 :
            enem_tank = pygame.transform.rotate(enem_tank_img, 90)
        if dir_y > 0 :
            enem_tank = pygame.transform.rotate(enem_tank_img, 270)


    # all_sprites.draw(screen)
    for bulet in bulets:
        screen.blit(bulet_img, bulet.rect)
        #pygame.draw.rect(screen, green, bulet.rect)
        bulet.update()

        if bulet.rect.x + 8 >= enemy.rect.x \
                and bulet.rect.x < enemy.rect.x + 16 \
                and bulet.rect.y + 8 >= enemy.rect.y \
                and bulet.rect.y < enemy.rect.y + 16:
            enemy.distroy()
    message_to_screen("You have kiled: ", yelow)
    message_to_screen(str(kills), yelow, 70, size="medium")
    pygame.display.flip()

if pygame.mixer:
    pygame.mixer.music.fadeout(10000)
pygame.time.wait(1000)
pygame.quit()