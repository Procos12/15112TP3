#Abdulwahab Al-Rumaihi, andrewID:arumaihi
#This is the main project file
#Imports
import pygame as pg
import random
import sys
from Spaceship import *
from Character import *
from Pikmin import *
from Enemy import *
from Fruit import *

#Initializing pygame
pg.init()

class Game():
#This class controls the entire game
	def __init__(self):
	#This method initializes the game
		self.clock=pg.time.Clock()
		self.clockTick=120
		self.background=0, 0, 0
		self.display=pg.display.set_mode((1280, 720))
		self.currentScreen="Menu"
		self.pikminList=[]
		self.enemyList=[]
		self.fruitList=[]
		self.buttonDict={}
		self.font=pg.font.Font("OpenSans-Regular.ttf", 22)
		self.pikImage=pg.image.load("pikmin.png")
		self.playerImage=pg.image.load("barbolD.png")
		self.enemyImage=pg.image.load("Enemy.png")
		self.appleImage=pg.image.load("apple.png")
		self.shipImage=pg.image.load("spaceship.png")
		self.gameMode="Normal"
		self.score=0
		pg.display.set_caption("Pikmin Mini")
		self.mainLoop()

	def drawText(self, text, x, y):
	#This method draws a textbox
		textBox=self.font.render(text, True, (255, 255, 255))
		textBoxRect=textBox.get_rect()
		textBoxRect.center=(x, y)
		if text not in self.buttonDict:
			self.buttonDict[text]=textBoxRect
		self.display.blit(textBox, textBoxRect)

	def getPikList(self):#Returns the pikmin list
		return self.pikminList

	def getEnemyList(self):#Returns the enemy list
		return self.enemyList

	def getFruitList(self):#Returns the fruit list
		return self.fruitList

	def getScreen(self):#Returns the games screen
		return self.display

	def addToList(self, obj):
	#Adds an object to their respective list
		if type(obj)==Fruit:
			self.fruitList.append(obj)
		elif type(obj)==Enemy:
			self.enemyList.append(obj)
		elif type(obj)==Pikmin:
			self.pikminList.append(obj)

	def removeFromList(self, obj):
	#Removes an object from their respective list
		if type(obj)==Fruit:
			self.fruitList.remove(obj)
		elif type(obj)==Enemy:
			self.enemyList.remove(obj)
		elif type(obj)==Pikmin:
			self.pikminList.remove(obj)

	def menuEventHandler(self):
	#This handles events on the main menu
		for event in pg.event.get():
			if event.type==pg.QUIT:
				sys.exit()
			if event.type==pg.MOUSEBUTTONDOWN:
				#Getting the mouse coordinates
				mousePos=pg.mouse.get_pos()
				for i in self.buttonDict:
					#If the mouse clicked on a button then take action accordingly
					if self.buttonDict[i].collidepoint(mousePos):
						if i=="Start Game":
							self.setupGame()
							self.gameMode="Normal"
							self.currentScreen="Game"
							break
						elif i=="Help":
							self.currentScreen="Help"
							break
						elif i=="Quit":
							sys.exit()
							break
						elif i=="Start Endless Game":
							self.setupGame()
							self.gameMode="Endless"
							self.currentScreen="Game"
							break
						self.buttonDict={}

	def mainMenuDraw(self):
	#This method draws the main menu
		self.drawText("Start Game", 640, 140)
		self.drawText("Start Endless Game", 640, 240)
		self.drawText("Help", 640, 410)
		self.drawText("Quit", 640, 540)

	def helpEventHandler(self):
	#This method handles events on the help menu
		for event in pg.event.get():
			if event.type==pg.QUIT:
				sys.exit()
			if event.type==pg.MOUSEBUTTONDOWN:
				mousePos=pg.mouse.get_pos()
				for i in self.buttonDict:
					if self.buttonDict[i].collidepoint(mousePos):
						if i=="Back":
							self.currentScreen="Menu"
						self.buttonDict={}

	def helpDraw(self):
	#This method draws the help screen
		self.drawText("You are the main character. You can move using the WASD Keys.", 640, 20)
		playerRect=self.playerImage.get_rect()
		playerRect.midtop=(640, 40)
		self.display.blit(self.playerImage, playerRect)
		self.drawText("These are pikmin and they will follow you. They can attack enemies, and they can pick up dead enemies and fruit", 640, playerRect.bottom+15)
		self.drawText("and bring them back to your ship.", 640, playerRect.bottom+40)
		pikRect=self.pikImage.get_rect()
		pikRect.midtop=(640, playerRect.bottom+60)
		self.display.blit(self.pikImage, pikRect)
		self.drawText("This is your ship, it takes fruit and converts it to juice, and takes enemies and spawns pikmin in return.", 640, pikRect.bottom+20)
		shipRect=self.shipImage.get_rect()
		shipRect.midtop=(640, pikRect.bottom+40)
		self.display.blit(self.shipImage, shipRect)
		self.drawText("The main point of the game is to command pikmin to pick up as much fruit and carry it back to the ship.", 640, shipRect.bottom+15)
		self.drawText("If you run out of pikmin or cannot carry anymore fruit or enemies with your current number the game ends.", 640, shipRect.bottom+40)
		self.drawText("This is an apple and it takes 2 pikmin to carry it back to the ship.", 640, shipRect.bottom+65)
		appleRect=self.appleImage.get_rect()
		appleRect.midtop=(640, shipRect.bottom+80)
		self.display.blit(self.appleImage, appleRect)
		self.drawText("This is an enemy. Enemies can follow pikmin, and attack them. When enemies die, pikmin can collect them. ", 640, appleRect.bottom+20)
		enemyRect=self.enemyImage.get_rect()
		enemyRect.midtop=(640, appleRect.bottom+40)
		self.display.blit(self.enemyImage, enemyRect)
		self.drawText("To command pikmin you need to be close enough to either fruit or enemy, and click on them.", 640, enemyRect.bottom+20)
		self.drawText("Pikmin will do commands in a sequence then come back to following you.", 640, enemyRect.bottom+50)
		self.drawText("The score depends on the amount of fruit carried back to the ship.", 640, enemyRect.bottom+80)
		self.drawText("If a fruit needs two pikmin to carry, it will give you two points.", 640, enemyRect.bottom+110)
		self.drawText("A normal game is won by reaching a score of 20 or more.", 640, enemyRect.bottom+140)
		self.drawText("An endless game continues till you either run out of pikmin, or cannot carry anymore fruit.", 640, enemyRect.bottom+170)
		self.drawText("Any type of game can be quit by pressing the escape key. You cannot pause a game.", 640, enemyRect.bottom+200)
		self.drawText("Back", 640, 680)

	def setupGame(self):
	#This method sets up the game for the first time
		#Creating the ship and main character
		self.score=0
		self.pikminList=[]
		self.enemyList=[]
		self.fruitList=[]
		self.barbol=Character((640, 360), self)
		self.sunny=Spaceship((640, 300), self)
		#Spawning some pikmin initially for the player to control
		for i in range(8):
			self.sunny.spawnPikmin()
		quadlist=[1, 2, 3, 4]
		for j in range(4):
		#Spawning the fruit
			#Choosing a quadrant and removing it once it 
			#has been used for a fruit
			quadrant=random.choice(quadlist)
			quadlist.remove(quadrant)
			#The x and y coordinates are chosen randomly based on the quadrant
			if quadrant==1 or quadrant==3:
				spawnX=random.randint(20, 510)
				if quadrant==1:
					spawnY=random.randint(20, 230)
				else:
					spawnY=random.randint(490, 700)
			elif quadrant==2 or quadrant==4:
				spawnX=random.randint(770, 1260)
				if quadrant==2:
					spawnY=random.randint(20, 230)
				else:
					spawnY=random.randint(490, 700)
			Fruit((spawnX, spawnY), self.sunny, self)
		quadlist=[1, 2, 3, 4]
		for k in range(4):
			quadrant=random.choice(quadlist)
			quadlist.remove(quadrant)
			if quadrant==1 or quadrant==3:
				spawnX=random.randint(20, 510)
				if quadrant==1:
					spawnY=random.randint(20, 230)
				else:
					spawnY=random.randint(490, 700)
			elif quadrant==2 or quadrant==4:
				spawnX=random.randint(770, 1260)
				if quadrant==2:
					spawnY=random.randint(20, 230)
				else:
					spawnY=random.randint(490, 700)
			Enemy("Enemy.png", (spawnX, spawnY), self.sunny, self)

	def gameDraw(self):
	#This method draws the game's screen
		#Updating the pikmin, fruit and enemies
		for i in self.pikminList:
			i.update()
		for k in self.fruitList:
			k.update()
		for j in self.enemyList:
			j.update()
		#Updating the ship and main character
		self.sunny.update()
		self.barbol.update()
		#Updating the score
		self.score=self.sunny.getScore()
		self.drawText("Score: "+str(self.score), 1200, 20)
		if self.gameMode=="Normal" and self.score>=20:
			self.currentScreen="Game Over"
		if len(self.pikminList)<2:
			self.currentScreen="Game Over"

	def userInput(self):
	#This method handles user input on the game screen
		for event in pg.event.get():
			#Quitting the entire game
			if event.type==pg.QUIT:
				sys.exit()
			if event.type==pg.MOUSEBUTTONDOWN:
				#Getting the mouse position
				mouseX, mouseY=pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]
				#Checking for interactions with enemies
				for j in self.enemyList:
					if j.getClicked(mouseX, mouseY):
						for i in self.pikminList:
							#If the pikmin is following and the command distance is ok
							#then command the pikmin
							if i.getTask()=="Follow" and i.getDistance(mouseX, mouseY):
								i.attackEnemy(j)
								i.changeTask("Attack")
								break
				#Checking for interactions with fruit
				for k in self.fruitList:
					if k.getClicked(mouseX, mouseY):
						for i in self.pikminList:
							#If the pikmin is following and the command distance is ok
							#then command the pikmin
							if i.getTask()=="Follow" and i.getDistance(mouseX, mouseY):
								i.goToFruit(k)
								i.changeTask("goTo")
								break
		#Handling player movement
		self.movementHandler()

	def movementHandler(self):
	#This method handles user movement on the main screen
		movement=pg.key.get_pressed()
		if movement[pg.K_a]:
			self.barbol.move("left")
		elif movement[pg.K_d]:
			self.barbol.move("right")
		elif movement[pg.K_w]:
			self.barbol.move("up")
		elif movement[pg.K_s]:
			self.barbol.move("down")
		elif movement[pg.K_ESCAPE]:
			self.currentScreen="Game Over"

	def pikminTaskHandler(self):
	#This method handles the pikmin's tasks
		for i in self.pikminList:
			if i.getTask()=="Follow":
				i.followCharacter(self.barbol)
			elif i.getTask()=="goTo":
				i.goToFruit()
			elif i.getTask()=="Attack":
				i.attackEnemy()

	def fruitTaskHandler(self):
	#This method handles the fruit's tasks
	    for k in self.fruitList:
	        if k.getTask()=="Move":
	            k.moveToShip()
	        elif k.getTask()=="None":
	            self.fruitList.remove(k)

	def enemyTaskHandler(self):
	#This method handles the enemie's tasks
		for j in self.enemyList:
			if j.getTask()=="Walk":
				j.move()
			elif j.getTask()=="toShip":
				j.goToShip()
			elif j.getTask()=="Target":
				j.fightPikmin()

	def spawn(self, obj):
	#This method spawns new enemies or fruit
		#Getting the coordinates of the player
		x, y=self.barbol.getCoordinates()
		#Getting the player's quadrant
		if x<720:
			if y>360:
				playerQ=3
			else:
				playerQ=1
		else:
			if y>360:
				playerQ=4
			else:
				playerQ=2
		#Removing the player's quadrant from possible quadrants
		quadlist=[1,2,3,4]
		quadlist.remove(playerQ)
		quadrant=random.choice(quadlist)
		#Getting a random x and y to spawn the enemy or fruit with
		if quadrant==1 or quadrant==3:
			spawnX=random.randint(20, 510)
			if quadrant==1:
				spawnY=random.randint(20, 230)
			else:
				spawnY=random.randint(490, 720)
		else:
			spawnX=random.randint(770, 1260)
			if quadrant==2:
				spawnY=random.randint(20, 230)
			else:
				spawnY=random.randint(490, 700)
		#Spawning the enemy or fruit
		if obj=="Enemy":
			Enemy("Enemy.png", (spawnX, spawnY), self.sunny, self)
		elif obj=="Fruit":
			Fruit((spawnX, spawnY), self.sunny, self)

	def gameEventHandler(self):
	#This method handles the game's events
		#Handling user input
		self.userInput()
		#Handling tasks of other objects
		self.pikminTaskHandler()
		self.fruitTaskHandler()
		self.enemyTaskHandler()
		#Spawning enemy or fruit if an enemy or fruit is killed
		if len(self.fruitList)<4:
			self.spawn("Fruit")
		if len(self.enemyList)<4:
			self.spawn("Enemy")

	def gameOverDraw(self):
	#This method draws the game over screen
		if self.gameMode=="Normal":
			if self.score>=20:
				text="You Won!"
			else:
				text="Try Again"
			self.drawText(text, 640, 360)
		if self.gameMode=="Endless":
			if self.score<20:
				text="Loser,"
			elif self.score>30:
				text="Amazing!"
			else:
				text="Good Job!"
			self.drawText(text+" Here's your score: "+str(self.score), 640, 360)
		self.drawText("Click anywhere to continue", 640, 400)

	def gameOverEvent(self):
	#This method handles events on the game over screen
		for event in pg.event.get():
			if event.type==pg.QUIT:
				sys.exit()
			if event.type==pg.MOUSEBUTTONDOWN:
				self.currentScreen="Menu"

	def mainLoop(self):
	#This function controls the main loop of the game
		while True:
			if self.currentScreen=="Menu":
				self.mainMenuDraw()
				self.menuEventHandler()
			elif self.currentScreen=="Game":
				self.gameDraw()
				self.gameEventHandler()
			elif self.currentScreen=="Help":
				self.helpDraw()
				self.helpEventHandler()
			elif self.currentScreen=="Game Over":
				self.gameOverDraw()
				self.gameOverEvent()
			#Refreshing the screen
			pg.display.flip()
			self.display.fill(self.background)
			self.clock.tick(self.clockTick)

game=Game()