import pygame, random, sys
from pygame.locals import *
import pathlib
import time 

# Consts
RANDOM_X = [140, 295, 440, 588]

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 60

X = 350
Y = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Assets
font_name = "elephant"

PLAYER_IMAGE = pathlib.Path(__file__).parent.joinpath('assets/player.png').resolve()
PLAYER_IMAGE_SNOW = pathlib.Path(__file__).parent.joinpath('assets/player-snow.png').resolve()

AMBULANCE_IMAGE = pathlib.Path(__file__).parent.joinpath('assets/amb.png').resolve()
COP_IMAGE =  pathlib.Path(__file__).parent.joinpath('assets/cop.png').resolve()
TAXI_IMAGE = pathlib.Path(__file__).parent.joinpath('assets/taxi.png').resolve()

BACKGROUND_IMAGE = pathlib.Path(__file__).parent.joinpath('assets/background.png').resolve()
BACKGROUND_IMAGE_SNOW = pathlib.Path(__file__).parent.joinpath('assets/background-snow.png').resolve()
EXPLOSION_IMAGE = pathlib.Path(__file__).parent.joinpath('assets/explosion.png').resolve()

GAME_OVER_MUSIC =  pathlib.Path(__file__).parent.joinpath('assets/audio/game-over.ogg').resolve()
EXPLOSION_SONG = pathlib.Path(__file__).parent.joinpath('assets/audio/explosion.ogg').resolve()
BACKGROUND_MUSIC = pathlib.Path(__file__).parent.joinpath('assets/audio/background.ogg').resolve()

# Initialization
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Avoid the cars!")
clock = pygame.time.Clock()

pygame.mixer.music.load(BACKGROUND_MUSIC)
pygame.mixer.music.play(-1, 20.0)
pygame.mixer.music.pause()

# Load assets and screen
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

LOAD_EXPLOSION_IMAGE = pygame.image.load(EXPLOSION_IMAGE).convert_alpha()
LOAD_BACKGROUND = pygame.image.load(BACKGROUND_IMAGE).convert()
LOAD_BACKGROUND_SNOW = pygame.image.load(BACKGROUND_IMAGE_SNOW).convert()
LOAD_EXPLOSION_IMAGE = pygame.transform.scale(LOAD_EXPLOSION_IMAGE, (100, 200))

# Classes
class Player(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(PLAYER_IMAGE).convert_alpha()
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = self.image.get_rect()
		self.rect[0] = 315
		self.rect[1] = 100
		self.speed = 5
		self.speed_vertical = 10

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

	def update(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_a] and player.rect[0] > 110:
			self.moveLeft()
		if keys[pygame.K_d] and player.rect[0] < 620:
			self.moveRight()
		if keys[pygame.K_w] and player.rect[1] > -95:
			self.moveUp()
		if keys[pygame.K_s] and player.rect[1] < 370:
			self.moveDown()

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
		self.speed = 5

	def moveY(self):
		if True:
			self.rect[1] -= self.speed
		if self.rect[1] < -230:
			self.rect[0] = random.choice(RANDOM_X)
			self.rect[1] = random.randint(700, 1500)

			self.update()
			self.draw(SCREEN)

	def draw(self, surface):
		surface.blit(self.image, (self.rect[0], self.rect[1]))

	def update(self):
		self.moveY()

# Instances
player = Player()
player.imageUrl = PLAYER_IMAGE_SNOW

ambulance = Enemy(AMBULANCE_IMAGE)
cop = Enemy(COP_IMAGE)
taxi = Enemy(TAXI_IMAGE)

# Functions
def draw_text(surf, text, size, x, y):
	font = pygame.font.SysFont(font_name, size)
	text_surface = font.render(text, True, BLACK)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)

def show_gameover_screen():
	SCREEN.blit(LOAD_BACKGROUND, (0,0))
	draw_text(SCREEN, "CAR GAME", 80, SCREEN_WIDTH/2, SCREEN_HEIGHT/4)
	draw_text(SCREEN, "WASD keys move, Good Luck!", 42,
              SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
	draw_text(SCREEN, "Press a key to begin", 36, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				time_now = pygame.time.get_ticks()
				waiting = False
				return time_now

def snowPhase():
	SCREEN.blit(LOAD_BACKGROUND_SNOW, (0,0))
	player.changeImage(PLAYER_IMAGE_SNOW)
	enemy_group.update()

# Variables
game_speed = 5
Running = True
game_over = True
initial_time = pygame.time.get_ticks()

pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1, 20.0)
pygame.mixer.music.pause()

# Main game
while Running:
	time_now = pygame.time.get_ticks()

	if game_over:
		pygame.mixer.music.pause()
		zeroTime = show_gameover_screen()
		initial_time = zeroTime
		pygame.mixer.music.unpause()
		pygame.mixer.music.set_pos(20.0)
		game_over = False
		all_sprites = pygame.sprite.Group()
		enemy_group = pygame.sprite.Group()

		player = Player()
		ambulance = Enemy(AMBULANCE_IMAGE)
		cop = Enemy(COP_IMAGE)
		taxi = Enemy(TAXI_IMAGE)

		enemy_group.add(ambulance)
		enemy_group.add(cop)
		enemy_group.add(taxi)

		all_sprites.add(player)
		all_sprites.add(ambulance)
		all_sprites.add(cop)
		all_sprites.add(taxi)

	delta_time = time_now - initial_time

	draw_text(SCREEN, str(round(delta_time/1000)), 60, 70, 70)

	for event in pygame.event.get():
		if event.type == QUIT:
			Running = False

	clock.tick(FPS)

	all_sprites.update()

	collide = (
		pygame.sprite.collide_mask(player, ambulance)
		or pygame.sprite.collide_mask(player, cop)
		or pygame.sprite.collide_mask(player, taxi)
	)

	if collide:
		game_over = True

	pygame.display.flip()

	if(delta_time >= 15000): # After 15sec, change theme phase
		snowPhase()
	else:
		SCREEN.blit(LOAD_BACKGROUND, (0, 0))

	all_sprites.draw(SCREEN)

if __name__ == '__main__':
	pygame.init()
	pygame.quit()
	sys.exit()