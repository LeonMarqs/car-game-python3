import pygame, random, sys
from pygame.locals import *

RANDOM_X = [140, 295, 440, 588] #140, 295, 440, 588

SCREEN_WIDHT = 900
SCREEN_HEIGHT = 600
GAME_SPEED = 5

X = 350
Y = 100

#max x_RIGHT = 477 max x_LEFT =  150


#X_ENEMIES = random.choice(RANDOM_X)
#Y_ENEMIES = random.randint(700, 1500)

FONT = "font/8-Bit-Madness.ttf"

pygame.init()

pygame.mixer.init()
game_over_music = 'assets/audio/game-over.mp3'
explosion_song = 'assets/audio/explosion.mp3'


SCREEN = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
pygame.display.set_caption("Cars - obstáculos")

BACKGROUND = pygame.image.load('assets/background.png')

EXPLOSION_IMAGE = pygame.image.load('assets/explosion.png').convert_alpha()
EXPLOSION_IMAGE = pygame.transform.scale(EXPLOSION_IMAGE, (100, 200))

player_group = pygame.sprite.Group()

################################### OBJETOS ##################################

class Car(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/car2.png').convert_alpha()

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

    def moveright(self, pixels):
        self.rect[0] += pixels

    def moveleft(self, pixels):
        self.rect[0] -= pixels

    def draw(self, surface):
        surface.blit(self.image, (self.rect[0], self.rect[1]))


class Amb(pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/amb.png').convert_alpha()

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        self.rect[0] = random.choice(RANDOM_X)
        self.rect[1] = random.randint(700, 1500)

    def movey(self):

        if True:
            self.rect[1] -= GAME_SPEED
            if self.rect[1] < -230:
                self.rect[0] = random.choice(RANDOM_X)
                self.rect[1] = random.randint(700, 1500)

                ambulance.update()
                ambulance.draw(SCREEN)

    def draw(self, surface):
        surface.blit(self.image, (self.rect[0], self.rect[1]))

class Cop(pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/cop.png').convert_alpha()

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        self.rect[0] = random.choice(RANDOM_X)
        self.rect[1] = random.randint(700, 1500)

    def movey(self):

        if True:
            self.rect[1] -= GAME_SPEED
            if self.rect[1] < -230:
                self.rect[0] = random.choice(RANDOM_X)
                self.rect[1] = random.randint(700, 1500)

                cop.update()
                cop.draw(SCREEN)

    def draw(self, surface):
        surface.blit(self.image, (self.rect[0], self.rect[1]))

class Car2(pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/car3.png').convert_alpha()

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        self.rect[0] = random.choice(RANDOM_X)
        self.rect[1] = random.randint(700, 1500)

    def movey(self):

        if True:
            self.rect[1] -= GAME_SPEED
            if self.rect[1] < -230:
                self.rect[0] = random.choice(RANDOM_X)
                self.rect[1] = random.randint(700, 1500)

                car_b.update()
                car_b.draw(SCREEN)

    def draw(self, surface):
        surface.blit(self.image, (self.rect[0], self.rect[1]))



################################################################################

player = Car()

ambulance = Amb()
cop = Cop()
car_b = Car2()

player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

player.rect[0] = 315
player.rect[1] = 100


enemy_group.add(ambulance)
enemy_group.add(cop)
enemy_group.add(car_b)

player_group.add(player)

white = (255, 255, 255)

def text_objects(text, font):
    textsurface = font.render(text, True, (0,0,0))
    return textsurface, textsurface.get_rect()


def Gameover():

    SCREEN.blit(pygame.image.load("assets/background.png"), (0,0))
    largeText = pygame.font.SysFont("elephant",60)
    TextSurf, TextRect = text_objects("GameOver", largeText)
    TextRect.center = ((SCREEN_WIDHT/2),(SCREEN_HEIGHT/2))
    SCREEN.blit(TextSurf, TextRect)
    pygame.display.flip()
    pygame.mixer.music.load(game_over_music)
    pygame.mixer.music.play()
    pygame.time.wait(1500)

Leonardo = True

while Leonardo:

    clock = pygame.time.Clock()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            Leonardo = False

        keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player.rect[0] > 110:
        player.moveleft(5)
    if keys[pygame.K_RIGHT] and player.rect[0] < 620:
        player.moveright(5)

    collide = (pygame.sprite.collide_mask(player, ambulance)
               or pygame.sprite.collide_mask(player, cop)
               or pygame.sprite.collide_mask(player, car_b))

    if collide:
        SCREEN.blit(BACKGROUND, (0, 0))
        pygame.display.flip()
        SCREEN.blit(EXPLOSION_IMAGE, (player.rect[0] + 50, player.rect[1] + 50))
        pygame.display.flip()
        pygame.mixer.music.load(explosion_song)
        pygame.mixer.music.play()
        pygame.time.wait(1000)
        Gameover()
        break

    player.update()
    ambulance.update()
    cop.update()
    car_b.update()

    SCREEN.blit(BACKGROUND, (0, 0))
    
    player.draw(SCREEN)
    ambulance.draw(SCREEN)
    cop.draw(SCREEN)
    car_b.draw(SCREEN)

    ambulance.movey()
    cop.movey()
    car_b.movey()


    pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    pygame.quit()
    sys.exit()