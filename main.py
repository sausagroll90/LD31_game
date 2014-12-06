import pygame

pygame.init()

size = (1000, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("candyfloss tower defense")
clock = pygame.time.Clock()

done = False

map = pygame.image.load("Simple Map.png")

class Tower(object):
	def __init__(self, range, countdown, type):
		self.range = range
		self.countdown = countdown
		self.type = type

class Enemy(object):
	def __init__(self, health):
		self.health = health
	
	def startup(self):
		self.xpos = 10.0
		self.ypos = 20.0
		self.countdown1 = 250
		self.countdown2 = 500
		self.countdown3 = 250
		self.countdown4 = 500
		self.countdown5 = 250
		self.countdown6 = 500
	
	def move(self):
		if self.countdown1 != 0:
			self.countdown1 -= 1
			self.xpos += 0.5
			print(self.countdown1)
		elif self.countdown2 != 0:
			self.countdown2 -= 1
			self.ypos += 0.5
		elif self.countdown3 != 0:
			self.countdown3 -= 1
			self.xpos += 0.5
		elif self.countdown4 != 0:
			self.countdown4 -= 1
			self.ypos -= 0.5
		elif self.countdown5 != 0:
			self.countdown5 -= 1
			self.xpos += 0.5
		elif self.countdown6 != 0:
			self.countdown6 -= 1
			self.ypos += 0.5

geoffrey = Enemy(100)
geoffrey.startup()

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	
	geoffrey.move()
	
	screen.fill((255, 255, 255))
	
	screen.blit(map, (0, 10))
	
	pygame.display.flip()
	
	clock.tick(60)

pygame.quit()