import pygame, random, sys
from pygame.locals import *
import pathlib

# Consts
RANDOM_X = [140, 295, 440, 588]

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

X = 350
Y = 100

# Assets
FONT = pathlib.Path(__file__).parent.joinpath('font/8-Bit-Madness.ttf').resolve()
WHITE = (255, 255, 255)

PLAYER_IMAGE = pathlib.Path(__file__).parent.joinpath('assets/player.png').resolve()
PLAYER_IMAGE_SNOW = pathlib.Path(__file__).parent.joinpath('assets/player-snow.png').resolve()

AMBULANCE_IMAGE = pathlib.Path(__file__).parent.joinpath('assets/amb.png').resolve()
COP_IMAGE =  pathlib.Path(__file__).parent.joinpath('assets/cop.png').resolve()
WHITE_CAR_IMAGE = pathlib.Path(__file__).parent.joinpath('assets/taxi.png').resolve()

BACKGROUND_IMAGE = pathlib.Path(__file__).parent.joinpath('assets/background.png').resolve()
BACKGROUND_IMAGE_SNOW = pathlib.Path(__file__).parent.joinpath('assets/background-snow.png').resolve()
EXPLOSION_IMAGE = pathlib.Path(__file__).parent.joinpath('assets/explosion.png').resolve()

GAME_OVER_MUSIC =  pathlib.Path(__file__).parent.joinpath('assets/audio/game-over.ogg').resolve()
EXPLOSION_SONG = pathlib.Path(__file__).parent.joinpath('assets/audio/explosion.ogg').resolve()
BACKGROUND_MUSIC = pathlib.Path(__file__).parent.joinpath('assets/audio/background.ogg').resolve()

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(BACKGROUND_MUSIC)
pygame.mixer.music.play(-1, 20.0)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Cars - obstáculos")

LOAD_EXPLOSION_IMAGE = pygame.image.load(EXPLOSION_IMAGE).convert_alpha()
LOAD_BACKGROUND = pygame.image.load(BACKGROUND_IMAGE).convert()
LOAD_BACKGROUND_SNOW = pygame.image.load(BACKGROUND_IMAGE_SNOW).convert()
LOAD_EXPLOSION_IMAGE = pygame.transform.scale(LOAD_EXPLOSION_IMAGE, (100, 200))

################################### CLASSES ##################################
class Player(pygame.sprite.Sprite):

	speed = 5
	speed_vertical = 10  # Added vertical speed variable

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load(PLAYER_IMAGE).convert_alpha()

		self.mask = pygame.mask.from_surface(self.image)

		self.rect = self.image.get_rect()

	def moveRight(self):
		self.rect[0] += self.speed

	def moveLeft(self):
		self.rect[0] -= self.speed

	def moveUp(self):
		self.rect[1] -= self.speed_vertical  # Changed vertical speed from 5 to 10, makes game-play more balanced

	def moveDown(self):
		self.rect[1] += self.speed_vertical  # Changed vertical speed from 5 to 10, makes game-play more balanced

	def changeImage(self, imageUrl):
		self.image = pygame.image.load(imageUrl).convert_alpha()
		self.mask = pygame.mask.from_surface(self.image)

	def update(self, speed):
		self.speed = speed

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
			self.rect[1] -= game_speed
		if self.rect[1] < -230:
			self.rect[0] = random.choice(RANDOM_X)
			self.rect[1] = random.randint(700, 1500)

			self.update()
			self.draw(SCREEN)

	def draw(self, surface):
		surface.blit(self.image, (self.rect[0], self.rect[1]))

	def update(self):
		self.moveY()

################################################################################

player = Player()
player.imageUrl = PLAYER_IMAGE_SNOW

ambulance = Enemy(AMBULANCE_IMAGE)
cop = Enemy(COP_IMAGE)
limousine = Enemy(WHITE_CAR_IMAGE)

enemy_group = pygame.sprite.Group()
player.rect[0] = 315
player.rect[1] = 100

enemy_group.add(ambulance)
enemy_group.add(cop)
enemy_group.add(limousine)

def text_objects(text, font):
	textsurface = font.render(text, True, (0,0,0))
	return textsurface, textsurface.get_rect()

def gameOver():
	SCREEN.blit(LOAD_BACKGROUND, (0,0))
	largeText = pygame.font.SysFont("elephant",60)
	TextSurf, TextRect = text_objects("GameOver", largeText)
	TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2))
	SCREEN.blit(TextSurf, TextRect)
	pygame.display.flip()
	pygame.mixer.music.load(GAME_OVER_MUSIC)
	pygame.mixer.music.play()
	pygame.time.wait(1500)

def timer():
	font = pygame.font.SysFont("elephant",60)
	timer = pygame.time.get_ticks()
	txt = font.render(str(round(timer/1000)), True, WHITE, (0,0,0))
	SCREEN.blit(txt, (70,70))
	return timer

def snowPhase():
		SCREEN.fill((0,0,0,0))
		SCREEN.blit(LOAD_BACKGROUND_SNOW, (0,0))
		game_speed = 9
		player.changeImage(PLAYER_IMAGE_SNOW)
		player.update(game_speed - 2)
		enemy_group.update()

Running = True
game_speed = 5
while Running:
	clock = pygame.time.Clock()
	clock.tick(60)
	time = timer()
	keys = pygame.key.get_pressed()

	for event in pygame.event.get():
		if event.type == QUIT:
			Running = False
			keys = pygame.key.get_pressed()

	if keys[pygame.K_a] and player.rect[0] > 110:
		player.moveLeft()
	if keys[pygame.K_d] and player.rect[0] < 620:
		player.moveRight()
	if keys[pygame.K_w] and player.rect[1] > -95:
		player.moveUp()
	if keys[pygame.K_s] and player.rect[1] < 370:
		player.moveDown()

	collide = (
		pygame.sprite.collide_mask(player, ambulance)
		or pygame.sprite.collide_mask(player, cop)
		or pygame.sprite.collide_mask(player, limousine)
	)

	if collide:
		SCREEN.blit(LOAD_BACKGROUND, (0, 0))
		pygame.display.flip()
		SCREEN.blit(LOAD_EXPLOSION_IMAGE, (player.rect[0] + 50, player.rect[1] + 50))
		pygame.display.flip()
		pygame.mixer.music.stop()
		pygame.mixer.music.load(EXPLOSION_SONG)
		pygame.mixer.music.play()
		pygame.time.wait(1000)
		gameOver()
		break

	pygame.display.flip()

	if(time >= 15000): # After 15sec, change theme phase
		snowPhase()
	else:
		SCREEN.blit(LOAD_BACKGROUND, (0, 0))

	player.draw(SCREEN)
	enemy_group.draw(SCREEN)

	ambulance.moveY()
	cop.moveY()
	limousine.moveY()

if __name__ == '__main__':
	pygame.init()
	pygame.quit()
	sys.exit()