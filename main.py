import pygame

pygame.init()

size = (1000, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("candyfloss tower defense")
clock = pygame.time.Clock()

done = False

class Tower(object):
	def __init__(self, range, countdown, type):
		self.range = range
		self.countdown = countdown
		self.type = type

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

	screen.fill((255, 255, 255))
	
	pygame.display.flip()
	
	clock.tick(60)

pygame.quit()