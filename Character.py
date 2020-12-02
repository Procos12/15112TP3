#Importing pygame
import pygame as pg

class Character():
#All of the attributes of the main character are under this class
    def __init__(self, coordinates, game):
    #Setting up an image list so images don't have to be loaded repeatedly
        self.imageList={}
        self.imageList["Right"]=pg.image.load("barbolR.png")
        self.imageList["Left"]=pg.image.load("barbolL.png")
        self.imageList["Up"]=pg.image.load("barbolU.png")
        self.imageList["Down"]=pg.image.load("barbolD.png")
        #Initial direction is facing right
        self.image=self.imageList["Down"]
        self.direction="Down"
        #Setting up the initial spawn point
        self.rect=self.image.get_rect()
        self.rect.center=coordinates
        self.game=game

    def getDirection(self):#Returns the characters direction
        return self.direction

    def changeSprite(self, direction):
    #This method changes the sprite of the character depending
    #on the direction the player wants the character to move
        self.direction=direction
        #The center is stored so the coordinates don't change
        #as the image changes
        center=self.rect.center
        #Changing the image of the sprite depending on the direction
        if direction=="Up":
            self.image=self.imageList["Up"]
        elif direction=="Down":
            self.image=self.imageList["Down"]
        elif direction=="Right":
            self.image=self.imageList["Right"]
        elif direction=="Left":
            self.image=self.imageList["Left"]
        #Rearranging the coordinates so that
        #the image is not moved after a change in direciton
        self.rect=self.image.get_rect()
        self.rect.center=center

    def move(self, direction):
    #This is method controls the movement of the main character
        #If the character's sprite is different, then the sprite changes
        #and then the character moves in the specified direction
        if direction=="right":
            if self.direction!="Right":
                self.changeSprite("Right")
            self.rect.move_ip([1, 0])
        elif direction=="left":
            if self.direction!="Left":
                self.changeSprite("Left")
            self.rect.move_ip([-1, 0])
        elif direction=="up":
            if self.direction!="Up":
                self.changeSprite("Up")
            self.rect.move_ip([0, -1])
        elif direction=="down":
            if self.direction!="Down":
                self.changeSprite("Down")
            self.rect.move_ip([0, 1])

    def update(self):#Updates the characters sprite onto the screen
    	screen=self.game.getScreen()
    	screen.blit(self.image, self.rect)

    def getCoordinates(self):#Returns the coordinate of the main character
    	return self.rect.center