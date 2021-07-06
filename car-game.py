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
pygame.mixer.music.load('assets/audio/background.ogg')
pygame.mixer.music.play(-1)

game_over_music = 'assets/audio/game-over.ogg'
explosion_song = 'assets/audio/explosion.ogg'

SCREEN = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
pygame.display.set_caption("Cars - obstáculos")

BACKGROUND = pygame.image.load('assets/background.png')

EXPLOSION_IMAGE = pygame.image.load('assets/explosion.png').convert_alpha()
EXPLOSION_IMAGE = pygame.transform.scale(EXPLOSION_IMAGE, (100, 200))

PLAYER_IMAGE = 'assets/car2.png'
AMBULANCE_IMAGE = 'assets/amb.png'
COP_IMAGE = 'assets/cop.png'
WHITE_CAR_IMAGE = 'assets/car3.png'

player_group = pygame.sprite.Group()

################################### OBJETOS ##################################

class Player(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load(PLAYER_IMAGE).convert_alpha()

		self.mask = pygame.mask.from_surface(self.image)

		self.rect = self.image.get_rect()

	def moveRight(self, pixels):
		self.rect[0] += pixels

	def moveLeft(self, pixels):
		self.rect[0] -= pixels

	def moveUp(self, pixels):
		self.rect[1] -= pixels

	def moveDown(self, pixels):
		self.rect[1] += pixels

	def draw(self, surface):
		surface.blit(self.image, (self.rect[0], self.rect[1]))

class Enemy(pygame.sprite.Sprite):
	def __init__(self, img):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load(img).convert_alpha()

		self.mask = pygame.mask.from_surface(self.image)

		self.rect = self.image.get_rect()

		self.rect[0] = random.choice(RANDOM_X)
		self.rect[1] = random.randint(700, 1500)

	def moveY(self):

		if True:
			self.rect[1] -= GAME_SPEED
		if self.rect[1] < -230:
			self.rect[0] = random.choice(RANDOM_X)
			self.rect[1] = random.randint(700, 1500)

			self.update()
			self.draw(SCREEN)

	def draw(self, surface):
		surface.blit(self.image, (self.rect[0], self.rect[1]))

################################################################################

player = Player()

ambulance = Enemy(AMBULANCE_IMAGE)
cop = Enemy(COP_IMAGE)
car_b = Enemy(WHITE_CAR_IMAGE)

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

Running = True

while Running:

	clock = pygame.time.Clock()
	clock.tick(60)

	keys = pygame.key.get_pressed()

	for event in pygame.event.get():
		if event.type == QUIT:
			Running = False
			keys = pygame.key.get_pressed()

	if keys[pygame.K_a] and player.rect[0] > 110:
		player.moveLeft(5)
	if keys[pygame.K_d] and player.rect[0] < 620:
		player.moveRight(5)
	if keys[pygame.K_w] and player.rect[1] > -95:
		player.moveUp(5)
	if keys[pygame.K_s] and player.rect[1] < 370:
		player.moveDown(5)

	collide = (
		pygame.sprite.collide_mask(player, ambulance)
		or pygame.sprite.collide_mask(player, cop)
		or pygame.sprite.collide_mask(player, car_b)
	)

	if collide:
		SCREEN.blit(BACKGROUND, (0, 0))
		pygame.display.flip()
		SCREEN.blit(EXPLOSION_IMAGE, (player.rect[0] + 50, player.rect[1] + 50))
		pygame.display.flip()
		pygame.mixer.music.stop()
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

	ambulance.moveY()
	cop.moveY()
	car_b.moveY()

	pygame.display.flip()

if __name__ == '__main__':
	pygame.init()
	pygame.quit()
	sys.exit()