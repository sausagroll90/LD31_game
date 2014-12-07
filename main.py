import pygame
import math

pygame.init()
size = (1000, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Project Candyfloss")
clock = pygame.time.Clock()
myfont = pygame.font.SysFont("monospace", 15)

done = False
lives = 10
money = 200

map = pygame.image.load("Map.png")
towerimg = pygame.image.load("Tower.png")
notower = pygame.image.load("Cant Tower.png")
geoffreyimg1 = pygame.image.load("Geoffrey.png")
geoffreyimg2 = pygame.transform.rotate(geoffreyimg1, -90)
geoffreyimg3 = pygame.transform.rotate(geoffreyimg1, 180)
geoffreyimg4 = pygame.transform.rotate(geoffreyimg1, 90)
projectile1 = pygame.image.load("Tower_Ball.png")
projectile2 = pygame.image.load("Tower_Ball 2.png")

shoot = pygame.mixer.Sound("Pew.wav")
place = pygame.mixer.Sound("Place.wav")
hit = pygame.mixer.Sound("Hit.wav")
death = pygame.mixer.Sound("Ded.wav")

death.set_volume(0.5)
shoot.set_volume(0.6)

enemylist = []
ballist = []
trackhitboxes = [
	pygame.Rect(30, 20, 300, 10),
	pygame.Rect(330, 20, 10, 517),
	pygame.Rect(330, 527, 280, 10),
	pygame.Rect(600, 15, 10, 522),
	pygame.Rect(600, 15, 300, 10),
	pygame.Rect(890, 15, 10, 550),
	pygame.Rect(815, 458, 167, 128),
	pygame.Rect(336, 110, 99, 125),
	pygame.Rect(0, 75, 251, 520),
	pygame.Rect(907, 45, 91, 88),
	pygame.Rect(845, 238, 96, 239)
]

class Ball(object):
	def __init__(self, startpos):
		self.xpos = startpos[0]
		self.ypos = startpos[1]
		self.direction = pygame.math.Vector2(3, 0)
		self.angle = 0
		self.hitbox = pygame.Rect(self.xpos, self.ypos, 20, 20)
	
	def update(self):
		self.direction.from_polar((3, 0))
		if len(enemylist) > 0:
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
		shot = False
		self.inrange = []
		if self.placed == False:
			self.xpos = pygame.mouse.get_pos()[0] - 20
			self.ypos = pygame.mouse.get_pos()[1] - 20
		for enemy in enemylist:
			if self.placed:
				if math.hypot(math.fabs(self.xpos - enemy.xpos), (self.ypos - enemy.ypos)) < 80:
					if self.reload == 0:
						shoot.play()
						ballist.append(Ball([self.xpos + 20, self.ypos + 20]))
						self.reload = 60
		
		if self.reload > 0:
			self.reload -= 1
		self.hitbox = pygame.Rect(self.xpos, self.ypos, 40, 40)
		for tower in towerlist:
			if self.hitbox.colliderect(tower.hitbox) and tower.placed and not tower.id == self.id:
				self.imgc = notower
				self.canplace = False
				break
		else:
			for hitbox in trackhitboxes:
				if self.hitbox.colliderect(hitbox):
					self.imgc = notower
					self.canplace = False
					break
			else:
				self.imgc = towerimg
				self.canplace = True

class Enemy(object):
	def __init__(self, health):
		self.imgr = geoffreyimg1
		self.imgd = geoffreyimg2
		self.imgl = geoffreyimg3
		self.imgu = geoffreyimg4
		self.imgc = geoffreyimg1
		self.hitbox = pygame.Rect(0, 0, 20, 20)
		self.health = health
		self.xpos = 10
		self.ypos = 6
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
		else:
			global lives
			lives -= 1
			enemylist.remove(self)
		
	def update(self):
		self.hitbox = pygame.Rect(self.xpos, self.ypos, 20, 20)
		
		for ball in ballist:
			if self.hitbox.collidepoint(ball.xpos, ball.ypos):
				ballist.remove(ball)
				self.health -= 10
				hit.play()
				
		if self.health == 0:
			enemylist.remove(self)
			death.play()

class Wave(object):
	def __init__(self, enemyno, delay, health):
		self.enemyno = enemyno
		self.delay = delay
		self.countdown = 0
		self.done = False
		self.started = False
		self.health = health
	
	def update(self):
		self.started = True
		if self.enemyno != 0:
			if self.countdown == 0:
				enemylist.append(Enemy(self.health))
				self.countdown = self.delay
				self.enemyno -= 1
			else:
				self.countdown -= 1
		elif len(enemylist) == 0:
			self.done = True
			global money
			money += 100

towerlist = []

wave1 = Wave(6, 60, 30)
wave2 = Wave(12, 50, 30)
wave3 = Wave(16, 40, 30)
wave4 = Wave(20, 40, 40)
wave5 = Wave(20, 35, 50)

nextplaced_id = 1

screen.fill((255, 255, 255))
screen.blit(map, (0, 0))
pygame.display.flip()

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_t:
				if len(towerlist) == 0 and money > 0:
					towerlist.append(Tower(nextplaced_id))
					nextplaced_id += 1
					money -= 100
				elif towerlist[-1].placed == True and money > 0:
					towerlist.append(Tower(nextplaced_id))
					nextplaced_id += 1
					money -= 100
		if event.type == pygame.MOUSEBUTTONDOWN:
			if not len(towerlist) == 0:
				if towerlist[-1].canplace and not towerlist[-1].placed:
					towerlist[-1].place()
					place.play()
	
	dirtyrects = [pygame.Rect(15, 100, 100, 100)]
	
	for tower in towerlist:
		dirtyrects.append(tower.hitbox)
		tower.update()
		dirtyrects.append(tower.hitbox)
	
	for ball in ballist:
		dirtyrects.append(ball.hitbox)
		ball.update()
		dirtyrects.append(ball.hitbox)
	
	for enemy in enemylist:
		dirtyrects.append(enemy.hitbox)
		enemy.update()
		enemy.move()
		dirtyrects.append(enemy.hitbox)
	
	if wave1.done == False:
		wave1.update()
		currentwave = "1"
	elif wave2.done == False:
		wave2.update()
		currentwave = "2"
	elif wave3.done == False:
		wave3.update()
		currentwave = "3"
	elif wave4.done == False:
		wave4.update()
		currentwave = "4"
	elif wave5.done == False:
		wave5.update()
		currentwave = "5"
	
	mrd = myfont.render("Money: " + str(money), 1, (0, 0, 0))
	lrd = myfont.render("Lives: " + str(lives), 1, (0, 0, 0))
	wrd = myfont.render("Wave: " + currentwave, 1, (0, 0, 0))
		
	screen.fill((255, 255, 255))
	
	screen.blit(map, (0, 0))
	
	for enemy in enemylist:
		screen.blit(enemy.imgc, (enemy.xpos, enemy.ypos))
	for tower in towerlist:
		screen.blit(tower.imgc, (tower.xpos, tower.ypos))
	for ball in ballist:
		screen.blit(pygame.transform.rotate(projectile1, ball.angle * -1), (ball.xpos, ball.ypos))
	screen.blit(mrd, (15, 100))
	screen.blit(lrd, (15, 120))
	screen.blit(wrd, (15, 140))
	
	pygame.display.update(dirtyrects)
	
	clock.tick(60)

pygame.quit()