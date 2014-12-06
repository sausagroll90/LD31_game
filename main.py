import pygame
import math

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
projectile1 = pygame.image.load("Tower_Ball.png")
projectile2 = pygame.image.load("Tower_Ball 2.png")

ballist = []
class Ball(object):
	def __init__(self, startpos):
		self.xpos = startpos[0]
		self.ypos = startpos[1]
		self.direction = pygame.math.Vector2(5, 0)
		self.angle = 0
	
	def update(self):
		self.direction.from_polar((5, 0))
		self.direction.rotate_ip(((math.atan2(self.ypos - (geoffrey.ypos + 10), self.xpos - (geoffrey.xpos + 10))) / math.pi) * 180 + 180)
		self.angle = self.direction.as_polar()[1]
		self.xpos += self.direction.x
		self.ypos += self.direction.y

class Tower(object):
	def __init__(self):
		self.reload = 0
		self.placed = False
		self.xpos = 0
		self.ypos = 0
	
	def place(self):
		self.placed = True
	
	def update(self):
		if self.placed == False:
			self.xpos = pygame.mouse.get_pos()[0] - 20
			self.ypos = pygame.mouse.get_pos()[1] - 20
		for enemy in enemylist:
			if math.hypot(math.fabs(self.xpos - enemy.xpos), (self.ypos - enemy.ypos)) < 120:
				if self.reload == 0:
					ballist.append(Ball([self.xpos + 20, self.ypos + 20]))
					self.reload = 60
				else:
					self.reload -= 1

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
enemylist = [geoffrey]

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_t:
				if len(towerlist) == 0:
					towerlist.append(Tower())
				elif towerlist[-1].placed == True:
					towerlist.append(Tower())
		if event.type == pygame.MOUSEBUTTONDOWN:
			if not len(towerlist) == 0:
				towerlist[-1].place()
				
	geoffrey.move()
	
	for tower in towerlist:
		tower.update()
	
	for ball in ballist:
		ball.update()
	
	screen.fill((255, 255, 255))
	
	screen.blit(map, (0, 10))
	screen.blit(geoffrey.imgc, (geoffrey.xpos, geoffrey.ypos))
	for tower in towerlist:
		screen.blit(towerimg, (tower.xpos, tower.ypos))
	for ball in ballist:
		screen.blit(pygame.transform.rotate(projectile1, ball.angle * -1), (ball.xpos, ball.ypos))
	pygame.display.flip()
	
	clock.tick(60)

pygame.quit()