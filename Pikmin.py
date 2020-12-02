#Importing pygame
import pygame as pg
import random
class Pikmin():
#This class defines the pikmin. Pikmin can follow the character,
#attack enemies, die, spawn, take fruit and enemies back to the ship
#and do nothing.
    def __init__(self, spawnX, spawnY, game):#Fix these variables later
    #This initializes the pikmin 
        self.pikmin=pg.image.load("pikmin.png")
        self.rect=self.pikmin.get_rect()
        self.rect.center=spawnX, spawnY
        self.task="Follow"
        self.health=20
        self.target=None
        self.game=game
        self.game.addToList(self)

    def getTask(self):#Returns the task of the pikmin
        return self.task

    def getCoordinates(self):#Returns the coordinates of the pikmin
        return self.rect.center

    def getDistance(self, x, y, Command=True):
    #This method is used to check whether or not the pikmin are able
    #to go to the item the player is clicking on
        #Getting the position of the object and pikmin
        objX, objY=x, y
        pikX, pikY=self.getCoordinates()
        #If the player is commanding the pikmin, then return the 
        if Command:
            return (((pikX-objX)**2+(pikY-objY)**2)**0.5)<230
        else:
            return ((pikX-objX)**2+(pikY-objY)**2)**0.5

    def getSpacing(self, direction):
    #This gets the spacing of the pikmin from the player
        #This is the default spacing
        spacingX=random.randint(-20, 20)
        spacingY=random.randint(-20, 20)
        #Depending on the direction, either the x or y
        #spacing will decrease or increase
        if direction=="Down":
            spacingY=random.randint(-45, -15)
        if direction=="Up":
            spacingY=random.randint(15, 45)
        if direction=="Right":
            spacingX=random.randint(-45, -15)
        if direction=="Left":
            spacingX=random.randint(15, 45)
        return spacingX, spacingY

    def followCharacter(self, char):
    #Following the main character
        #Getting the pikmin's coordinates and the characters direction
        pikX, pikY=self.getCoordinates()
        direction=char.getDirection()
        #Getting the coordinates of the characters back so the pikmin follow
        if direction=="Down":
            charX, charY=char.rect.midtop[0], char.rect.midtop[1]
        if direction=="Up":
            charX, charY=char.rect.midbottom[0], char.rect.midbottom[1]
        if direction=="Right":
            charX, charY=char.rect.midleft[0], char.rect.midleft[1]
        if direction=="Left":
            charX, charY=char.rect.midright[0], char.rect.midright[1]
        #Getting the spacing and moving the pikmin accordingly
        spacingX, spacingY=self.getSpacing(direction)
        if pikX<charX+spacingX:
            self.rect.move_ip([1, 0])
        if pikX>charX+spacingX:
            self.rect.move_ip([-1, 0])
        if pikY<charY+spacingY:
            self.rect.move_ip([0, 1])
        if pikY>charY+spacingY:
            self.rect.move_ip([0, -1])

    def changeTask(self, task, obj=None):
    #This method changes the task of the pikmin
        if obj!=None:
            self.target=obj
        self.task=task

    def update(self):#Updates the sprite of the pikmin
    	screen=self.game.getScreen()
    	screen.blit(self.pikmin, self.rect)

    def takeDamage(self, damage):#Dying is just stopping the pikmin from being updated
        self.health-=damage
        if self.health<=0:
            self.game.removeFromList(self)

    def getTarget(self):#Returns the target of the pikmin
        return self.target

    def getHealth(self):#Returns the health of the pikmin
        return self.health

    def goToFruit(self, obj=None):
    #This method tells the pikmin to go to a fruit,
    #pick it up and go to the ship
        #If there is a fruit in the parameters, then set it up as a target
        if obj!=None:
            self.target=obj
        #Getting the coordinates of the pikmin and the fruit
        pikX, pikY=self.getCoordinates()
        targetX, targetY=self.target.getPickLocation()
        #Moving the pikmin towards the fruit
        if pikX<targetX:
            self.rect.move_ip([1,0])
        if pikX>targetX:
            self.rect.move_ip([-1,0])
        if pikY>targetY:
            self.rect.move_ip([0,-1])
        if pikY<targetY:
            self.rect.move_ip([0,1])
        #If the pikmin is within the range to pick the fruit up
        #then add it to the list
        if pikY<targetY+25 and pikY>targetY-25:
            if pikX<targetX+25 and pikX>targetX-25:
                self.target.addPikmin(self)
        #If the fruit is not in the level anymore
        #then just follow the main character again
        if self.target not in self.game.getFruitList():
            self.changeTask("Follow")

    def attackEnemy(self, enemy=None):
    #This method is used when attacking enemies
        #If this is the first time the function is called,
        #set up the enemy as the target
        if enemy!=None:
            self.target=enemy
        #Getting the coordinates of the pikmin and the enemy
        pikX, pikY=self.getCoordinates()
        targetX, targetY=self.target.getPickLocation()
        #Moving the pikmin towards the enemy
        if pikX<targetX:
            self.rect.move_ip([1,0])
        if pikX>targetX:
            self.rect.move_ip([-1,0])
        if pikY>targetY:
            self.rect.move_ip([0,-1])
        if pikY<targetY:
            self.rect.move_ip([0,1])
        #If the pikmin is not in the level anymore
        #then just follow the main character again
        if self.target not in self.game.getEnemyList():
            self.changeTask("Follow")