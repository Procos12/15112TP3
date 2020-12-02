#Importing pygame
import pygame as pg
import random 
from Pikmin import *
class Spaceship():
#This class has all the actions of the spaceship,
#the spaceship also handles the score so the score is also handled here
    def __init__(self, coordinates, game):
    #Initializes the spacehip on the screen with a certain position
        self.image=pg.image.load("spaceship.png")
        self.rect=self.image.get_rect()
        self.rect.center=coordinates
        self.juice=0
        self.game=game

    def spawnPikmin(self):
    #This function spawns pikmin around the ship
        #Getting the location where the pikmin spawn around the ship
        xDisplacement=random.randint(-30, 30)
        yDisplacement=random.randint(-30, 30)
        if xDisplacement>0:
            spawnX=self.rect.right+xDisplacement
        else:
            spawnX=self.rect.left+xDisplacement
        if yDisplacement>0:
            spawnY=self.rect.bottom+yDisplacement
        else:
            spawnY=self.rect.top+yDisplacement
        #Creating a pikmin at that location
        Pikmin(spawnX, spawnY, self.game)

    def takeFruit(self, fruit):
    #This function takes fruit in and adds it to the player's juice
        self.juice+=fruit.getJuice()//2
        fruit.changeTask("None")

    def takeEnemy(self, enemy):
    #This function takes an enemy and spawns pikmin
    #according to how many pikmin are meant to spawn
        pikmin=enemy.getPikmin()
        self.game.removeFromList(enemy)
        for i in range(pikmin):
            self.spawnPikmin()

    def update(self):
    #Updating the sprite
    	screen=self.game.getScreen()
    	screen.blit(self.image, self.rect)

    def getCoordinates(self):#Returns the coordinates of the ship
        return self.rect.center[0], self.rect.center[1]

    def getScore(self):#Returns the score
    	return self.juice