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
notower = pygame.image.load("Cant Tower.png")
geoffreyimg1 = pygame.image.load("Geoffrey.png")
geoffreyimg2 = pygame.transform.rotate(geoffreyimg1, -90)
geoffreyimg3 = pygame.transform.rotate(geoffreyimg1, 180)
geoffreyimg4 = pygame.transform.rotate(geoffreyimg1, 90)
projectile1 = pygame.image.load("Tower_Ball.png")
projectile2 = pygame.image.load("Tower_Ball 2.png")

enemylist = []
ballist = []

class Ball(object):
	def __init__(self, startpos):
		self.xpos = startpos[0]
		self.ypos = startpos[1]
		self.direction = pygame.math.Vector2(3, 0)
		self.angle = 0
		self.hitbox = pygame.Rect(self.xpos, self.ypos, 20, 20)
	
	def update(self):
		self.direction.from_polar((3, 0))
		self.direction.rotate_ip(((math.atan2(self.ypos - (enemylist[0].ypos + 10), self.xpos - (enemylist[0].xpos + 10))) / math.pi) * 180 + 180)
		self.angle = self.direction.as_polar()[1]
		self.xpos += self.direction.x
		self.ypos += self.direction.y
		self.hitbox = pygame.Rect(self.xpos, self.ypos, 20, 20)

class Tower(object):
	def __init__(self, id):
		self.id = id
		self.reload = 0
		self.placed = False
		self.xpos = 0
		self.ypos = 0
		self.inrange = []
		self.hitbox = pygame.Rect(0, 0, 40, 40)
		self.canplace = True
	
	def place(self):
		self.placed = True
	
	def update(self):
		self.inrange = []
		if self.placed == False:
			self.xpos = pygame.mouse.get_pos()[0] - 20
			self.ypos = pygame.mouse.get_pos()[1] - 20
		for enemy in enemylist:
			if math.hypot(math.fabs(self.xpos - enemy.xpos), (self.ypos - enemy.ypos)) < 80:
				if self.reload == 0:
					ballist.append(Ball([self.xpos + 20, self.ypos + 20]))
					self.reload = 60
				else:
					self.reload -= 1
		self.hitbox = pygame.Rect(self.xpos, self.ypos, 40, 40)
		for tower in towerlist:
			if self.hitbox.colliderect(tower.hitbox) and tower.placed and not tower.id == self.id:
				self.imgc = notower
				self.canplace = False
				break
		else:
			self.imgc = towerimg
			self.canplace = True

class Enemy(object):
	def __init__(self):
		self.imgr = geoffreyimg1
		self.imgd = geoffreyimg2
		self.imgl = geoffreyimg3
		self.imgu = geoffreyimg4
		self.imgc = geoffreyimg1
		self.hitbox = pygame.Rect(0, 0, 20, 20)
		self.health = 50
		self.xpos = 10
		self.ypos = 16
		self.countdown1 = 311
		self.countdown2 = 502
		self.countdown3 = 275
		self.countdown4 = 504
		self.countdown5 = 291
		self.countdown6 = 500
	
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
		
	def update(self):
		self.hitbox = pygame.Rect(self.xpos, self.ypos, 20, 20)
		
		for ball in ballist:
			if self.hitbox.collidepoint(ball.xpos, ball.ypos):
				ballist.remove(ball)
				self.health -= 10
				
		if self.health == 0:
			enemylist.remove(self)

class Wave(object):
	def __init__(self, enemyno, delay):
		self.enemyno = enemyno
		self.delay = delay
		self.countdown = 0
	
	def update(self):
		if self.enemyno != 0:
			if self.countdown == 0:
				enemylist.append(Enemy())
				self.countdown = self.delay
				self.enemyno -= 1
			else:
				self.countdown -= 1
		
towerlist = []

wave1 = Wave(10, 60)

nextplaced_id = 1

screen.fill((255, 255, 255))
pygame.display.flip()

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_t:
				if len(towerlist) == 0:
					towerlist.append(Tower(nextplaced_id))
					nextplaced_id += 1
				elif towerlist[-1].placed == True:
					towerlist.append(Tower(nextplaced_id))
					nextplaced_id += 1
		if event.type == pygame.MOUSEBUTTONDOWN:
			if not len(towerlist) == 0:
				if towerlist[-1].canplace:
					towerlist[-1].place()
	
	dirtyrects = []
	
	for tower in towerlist:
		dirtyrects.append(tower.hitbox)
		tower.update()
	
	for ball in ballist:
		dirtyrects.append(ball.hitbox)
		ball.update()
		dirtyrects.append(ball.hitbox)
	
	for enemy in enemylist:
		dirtyrects.append(enemy.hitbox)
		enemy.update()
		enemy.move()
		dirtyrects.append(enemy.hitbox)
	
	wave1.update()
	
	screen.fill((255, 255, 255))
	
	screen.blit(map, (0, 10))
	
	for enemy in enemylist:
		screen.blit(enemy.imgc, (enemy.xpos, enemy.ypos))
	for tower in towerlist:
		screen.blit(tower.imgc, (tower.xpos, tower.ypos))
	for ball in ballist:
		screen.blit(pygame.transform.rotate(projectile1, ball.angle * -1), (ball.xpos, ball.ypos))
		
	pygame.display.update(dirtyrects)
	
	clock.tick(60)

pygame.quit()