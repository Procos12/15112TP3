import pygame as pg
import random
class Fruit():
#This class contains all the attributes of a fruit. Fruits can be 
#taken back to the ship and are added to the juice when they are
    #This dictionary holds the different types of fruits
    #The values indicate both the juice the fruit gives and
    #how many pikmin are needed to carry the fruit
    #More fruit can be added later
    FRUITS={"apple":4, "blueberry":2}
    FRUITLIST=["apple", "blueberry"]
    def __init__(self, coordinates, ship, game):
        #Setting the image, task, and location of the fruit
        fruit=random.choice(Fruit.FRUITLIST)
        self.image=pg.image.load(fruit+".png")
        self.rect=self.image.get_rect()
        self.task="Exist"
        self.rect.center=coordinates
        self.fruit=fruit
        #Setting the juice and number of pikmin needed to carry the fruit
        self.pikmin=Fruit.FRUITS[fruit]
        self.juice=Fruit.FRUITS[fruit]
        self.pikminList=[]
        self.ship=ship
        self.game=game
        self.game.addToList(self)
        self.shipX, self.shipY=self.ship.getCoordinates()

    def getClicked(self, mouseX, mouseY):
    #Checks if the Fruit was clicked on or not
        right, left=self.rect.right, self.rect.left
        top, bottom=self.rect.top, self.rect.bottom
        if mouseX<right and mouseX>left:
            if mouseY<bottom and mouseY>top:
                return True
        return False

    def moveToShip(self):
    #This function moves the fruit to the ship with the pikmin
        #Changing the task to Move if it wasn't already that
        if self.task!="Move":
            self.task="Move"
        fruitX, fruitY=self.getCoordinates()
        if fruitX<self.shipX:
            self.rect.move_ip([1, 0])
        if fruitX>self.shipX:
            self.rect.move_ip([-1, 0])
        if fruitY<self.shipY:
            self.rect.move_ip([0, 1])
        if fruitY>self.shipY:
            self.rect.move_ip([0, -1])
        #If the fruit reaches the ship then add it to the ships juice
        if fruitX==self.shipX and fruitY==self.shipY:
            self.ship.takeFruit(self)
        #In case a pikmin dies while carrying the fruit
        for i in self.pikminList:
            if i not in self.game.getPikList():
                self.pikminList.remove(i)
                self.task="Exist"

    def addPikmin(self, pik):
    #Adds pikmin to the list of those carrying the fruit
    #Also checks if there arre enough pikmin to carry the fruit
    #and 
        if pik not in self.pikminList:
            self.pikminList.append(pik)
        if len(self.pikminList)==self.pikmin:
            self.moveToShip()

    def changeTask(self, task):
        self.task=task

    def getPikmin(self):
    #Returns the number of pikmin needed to carry the fruit
        return self.pikmin

    def getCoordinates(self):#Returns the coordinates of the object
        return self.rect.center[0], self.rect.center[1]

    def getTask(self):#Returns the task of the object
        return self.task

    def getPickLocation(self):
    #This method is used to determine where the pikmin can pick up the fruit
        pickups=[]
        topleft, topright=self.rect.topleft, self.rect.topright
        bottomright, bottomleft=self.rect.bottomleft, self.rect.bottomright
        pickups.append(topleft)
        pickups.append(topright)
        pickups.append(bottomright)
        pickups.append(bottomleft)
        return random.choice(pickups)

    def getJuice(self):#Retuns the juice of the fruit
        return self.juice

    def update(self):#Updates the fruit on the screen
    	screen=self.game.getScreen()
    	screen.blit(self.image, self.rect)