import pygame

pygame.init()

size = (1000, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("candyfloss tower defense")
clock = pygame.time.Clock()

done = False

map = pygame.image.load("Simple Map.png")
towerimg = pygame.image.load("Tower.png")
geoffreyimg1 = pygame.image.load("Geoffrey.png")
geoffreyimg2 = pygame.transform.rotate(geoffreyimg1, -90)
geoffreyimg3 = pygame.transform.rotate(geoffreyimg1, 180)
geoffreyimg4 = pygame.transform.rotate(geoffreyimg1, 90)

class Tower(object):
	def __init__(self, range, countdown, type):
		self.range = range
		self.countdown = countdown
		self.type = type
		self.placed = False
		self.xpos = 0
		self.ypos = 0
	
	def place(self):
		self.placed = True
	
	def check(self):
		if self.placed == False:
			self.xpos = pygame.mouse.get_pos()[0] - 20
			self.ypos = pygame.mouse.get_pos()[1] - 20

class Enemy(object):
	def __init__(self, type, imgr, imgd, imgl, imgu):
		self.type = type
		self.imgr = imgr
		self.imgd = imgd
		self.imgl = imgl
		self.imgu = imgu
	
	def startup(self):
		self.xpos = 10
		self.ypos = 16
		self.countdown1 = 311
		self.countdown2 = 502
		self.countdown3 = 275
		self.countdown4 = 504
		self.countdown5 = 291
		self.countdown6 = 500
		self.imgc = self.imgr
	
	def move(self):
		if self.countdown1 != 0:
			self.countdown1 -= 1
			self.xpos += 1
			self.imgc = self.imgr
		elif self.countdown2 != 0:
			self.countdown2 -= 1
			self.ypos += 1
			self.imgc = self.imgd
		elif self.countdown3 != 0:
			self.countdown3 -= 1
			self.xpos += 1
			self.imgc = self.imgr
		elif self.countdown4 != 0:
			self.countdown4 -= 1
			self.ypos -= 1
			self.imgc = self.imgu
		elif self.countdown5 != 0:
			self.countdown5 -= 1
			self.xpos += 1
			self.imgc = self.imgr
		elif self.countdown6 != 0:
			self.countdown6 -= 1
			self.ypos += 1
			self.imgc = self.imgd

geoffrey = Enemy("geoffrey", geoffreyimg1, geoffreyimg2, geoffreyimg3, geoffreyimg4)
geoffrey.startup()

towerlist = []

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_t:
				if len(towerlist) == 0:
					towerlist.append(Tower(200, 60, "basic"))
				elif towerlist[-1].placed == True:
					towerlist.append(Tower(200, 60, "basic"))
		if event.type == pygame.MOUSEBUTTONDOWN:
			if not len(towerlist) == 0:
				towerlist[-1].place()
				
	geoffrey.move()
	for tower in towerlist:
		tower.check()
	
	screen.fill((255, 255, 255))
	
	screen.blit(map, (0, 10))
	screen.blit(geoffrey.imgc, (geoffrey.xpos, geoffrey.ypos))
	for tower in towerlist:
		screen.blit(towerimg, (tower.xpos, tower.ypos))
	pygame.display.flip()
	
	clock.tick(60)

pygame.quit()