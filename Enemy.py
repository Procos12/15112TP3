import pygame as pg
import random
class Enemy():
#This class handles enemies and their actions
    def __init__(self, image, coordinates, ship, game):
    #Initializing the enemy object
        self.image=pg.image.load(image)
        self.rect=self.image.get_rect()
        self.rect.center=coordinates
        self.ship=ship
        self.shipX, self.shipY=ship.getCoordinates()
        self.health=100
        self.pikmin=3
        self.pikminCarriers=[]
        self.detectedPikmin=[]
        self.hostilePikmin=[]
        self.task="Walk"
        self.game=game
        self.game.addToList(self)
        self.getWalkLoop()

    def getWalkLoop(self):
    #This function gets loop along which the enemy will walk along
        #Getting the direction of 
        directionList=["Right", "Left", "Up", "Down"]
        self.directionList=[]
        x, y=self.rect.center
        if x<720:
            self.directionList.append("Right")
        else:
            self.directionList.append("Left")
        if y<360:
            self.directionList.append("Up")
        else:
            self.directionList.append("Down")
        for i in directionList:
            if i not in self.directionList:
                self.directionList.append(i)
        #Returns the boundaries in which the enemy walks
        self.lBoundary, self.rBoundary=max(20, x-50), min(1240, x+50)
        self.uBoundary, self.dBoundary=max(20, y-50), min(680, y+50)
        self.currentDirection=0

    def getClicked(self, mouseX, mouseY):
    #Checks if the enemy was clicked on or not
        right, left=self.rect.right, self.rect.left
        top, bottom=self.rect.top, self.rect.bottom
        if mouseX<right and mouseX>left:
            if mouseY<bottom and mouseY>top:
                return True
        return False

    def getTask(self):#Returns the task of the enemy
        return self.task

    def getPikmin(self):
    #Returns how many pikmin should spawn after the ship takes in
    #the enemy
        return self.pikmin

    def getCoordinates(self):
        return self.rect.center

    def getHealth(self):#Returns the health of the enemy
        return self.health

    def move(self):
    #This function is used for the motion of the enemy
        direction=self.directionList[self.currentDirection]
        x, y=self.getCoordinates()
        if direction=="Down" and y<self.dBoundary:
            self.rect.move_ip([0,1])
        elif direction=="Up" and y>self.uBoundary:
            self.rect.move_ip([0,-1])
        elif direction=="Right" and x<self.rBoundary:
            self.rect.move_ip([1,0])
        elif direction=="Left" and x>self.lBoundary:
            self.rect.move_ip([-1,0])
        else:
            self.currentDirection+=1
            #Changing the direction when a boundary is reached
            if self.currentDirection==len(self.directionList):
                self.currentDirection=0

    def getPikmin(self):
    #Returns the number of pikmin that spawn when the enemy
    #is taken into the ship
        return self.pikmin

    def getPickLocation(self):
    #This method is used to determine where the pikmin
    #can interact with the enemy
        pickups=[]
        #Pikmin can interact with the enemy from the four corners of the enemy
        topleft, topright=self.rect.topleft, self.rect.topright
        bottomright, bottomleft=self.rect.bottomleft, self.rect.bottomright
        pickups.append(topleft)
        pickups.append(topright)
        pickups.append(bottomright)
        pickups.append(bottomleft)
        return random.choice(pickups)

    def attackPikmin(self):
    #This function hurts pikmin when they are in range
    #and takes damage from hostile pikmin in range
        x, y=self.getCoordinates()
        for i in self.game.getPikList():
            if i.getDistance(x, y, False)<30:
                if i.getTask()=="Attack":
                    self.health-=5
                i.takeDamage(2)

    def getTargetPikmin(self):
    #This function updates the targeted pikmin the enemy should
    #follow
        x, y=self.getCoordinates()
        for i in self.game.getPikList():
            if i.getDistance(x, y, False)<130:
                if i.getTask()=="Attack" and i not in self.hostilePikmin:
                    self.hostilePikmin.append(i)
                elif i not in self.detectedPikmin:
                    self.detectedPikmin.append(i)
        #The loops below remove a pikmin from the lists if they have died
        #or broke any of the criteria of their respective lists
        for i in self.detectedPikmin:
            if i.getDistance(x, y, False)>130 or i.getHealth()<=0 or i.getTask()=="Attack":
                self.detectedPikmin.remove(i)
        for i in self.hostilePikmin:
            if i.getDistance(x, y, False)>130 or i.getHealth()<=0 or i.getTask()!="Attack":
                self.hostilePikmin.remove(i)
        if len(self.hostilePikmin)>0 or len(self.detectedPikmin)>0:
        	self.task="Target"
        	if self.health<=0:
        		self.getPikCarriers()
        else:
        	if self.task=="Target":
        		self.task="Walk"
        		self.getWalkLoop()

    def getPikCarriers(self):
    #This function is used to check whether or not pikmin are
    #currently carrrying the enemy
        x, y=self.getCoordinates()
        for i in self.hostilePikmin:
            if i.getDistance(x, y, False)<30 and i not in self.pikminCarriers:
                self.pikminCarriers.append(i)

    def fightPikmin(self):
    #This function is used to go towards the pikmin that are attacking
        x, y=self.getCoordinates()
        if len(self.hostilePikmin)>0:
            pikmin=self.hostilePikmin[0]
        else:
            pikmin=self.detectedPikmin[0]
        pikX, pikY=pikmin.getCoordinates()
        if x<pikX:
            self.rect.move_ip([1, 0])
        if x>pikX:
            self.rect.move_ip([-1, 0])
        if y<pikY:
            self.rect.move_ip([0, 1])
        if y>pikY:
            self.rect.move_ip([0, -1])

    def goToShip(self):
    #This method is used to move the enemy to the ship
        if self.task!="toShip":
        	self.task="toShip"
        x, y=self.getCoordinates()
        if len(self.pikminCarriers)>=self.pikmin:
            if x<self.shipX:
                self.rect.move_ip([1, 0])
            if x>self.shipX:
                self.rect.move_ip([-1, 0])
            if y<self.shipY:
                self.rect.move_ip([0, 1])
            if y>self.shipY:
                self.rect.move_ip([0, -1])
            #If the enemy reaches the ship, then take it in
            if x==self.shipX and y==self.shipY:
                self.ship.takeEnemy(self)
            #In case a pikmin dies while carrying the enemy
            for i in self.pikminCarriers:
                if i not in self.game.getPikList():
                    self.pikminList.remove(i)
                    self.task="Wait"

    def update(self):#Updating the sprite
    	screen=self.game.getScreen()
    	self.getTargetPikmin()
    	if self.health>0:
    		self.attackPikmin()
    	else:
    		self.task="toShip"
    	screen.blit(self.image, self.rect)