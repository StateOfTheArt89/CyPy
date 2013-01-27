#!/usr/bin/python
# -*- coding: utf-8 -*-

from actionbaritem import *

from control import *
from glhelper import *

from sound import *


''' Nicht sehr abstrahiert, sondern spezifisch für unser Spiel gebaut'''
class ActionBar(Control):

	#Gesundheit des Spielers in Prozent
	__playerHealth = 0.1

	__currentBackgroundId = 0
	__animationUp = True
	__timeCount = 0.0
	__timeOut = 0.0
	_backgrounds = []
	__heartBeatSound = None
	#Items, die anklickbar sind
	_itemSlots = [None for x in range(0,6)]
	#Definition, wo sich Boxen für Items befinden..
	#relativ zur Actionbar
	_itemsPosition = ({"x": 73, "y": 65}, {"x": 161, "y": 65}, {"x": 249, "y": 65}, {"x": 513, "y": 65},{"x": 601, "y": 65},{"x": 688, "y": 65})

	def __init__(self,x,y,width,height,actionKey=None):
		Control.__init__(self,x,y,width,height,"Sprites/GUI/Menubar1.png")
		self._backgrounds.append(loadTexture("Sprites/GUI/Menubar1.png"))
		self._backgrounds.append(loadTexture("Sprites/GUI/Menubar2.png"))
		self._backgrounds.append(loadTexture("Sprites/GUI/Menubar3.png"))
		itemPos = self.getActionBarItemPosition(0)
		newItem = ActionBarItem(itemPos[0],itemPos[1],32,32,"Sprites/GUI/icon5.png","1")
		self.addChild(newItem)
		itemPos = self.getActionBarItemPosition(1)
		newItem = ActionBarItem(itemPos[0],itemPos[1],32,32,"Sprites/GUI/icon1.png","2")
		self.addChild(newItem)
		itemPos = self.getActionBarItemPosition(2)
		newItem = ActionBarItem(itemPos[0],itemPos[1],32,32,"Sprites/GUI/icon2.png","3")
		self.addChild(newItem)
		itemPos = self.getActionBarItemPosition(3)
		newItem = ActionBarItem(itemPos[0],itemPos[1],32,32,"Sprites/GUI/icon3.png","4")
		self.addChild(newItem)
		itemPos = self.getActionBarItemPosition(4)
		newItem = ActionBarItem(itemPos[0],itemPos[1],32,32,"Sprites/GUI/icon4.png","5")
		self.addChild(newItem)
		itemPos = self.getActionBarItemPosition(5)
		newItem = ActionBarItem(itemPos[0],itemPos[1],32,32,"Sprites/GUI/icon6.png","6")
		self.addChild(newItem)
		self.__heartBeatSound = Sound("Sounds/HeartTest2.wav")

	def getActionBarItemPosition(self,id):
		x = self._itemsPosition[id]["x"] + self._x
		y = self._itemsPosition[id]["y"] + self._y
		return (x,y)

	def setPlayerHealth(self, health):
		self.__playerHealth = health

	def mouseClick(self, button, state, x, y):
		Control.mouseClick(self, button, state, x, y)
		if x > self._x and x < self._x + self._width and y > self._y+20 and y < self._y + self._height:
			return True
		return False

	def update(self, delta):
		Control.update(self, delta)
		self.__timeCount += delta
		if self.__timeCount > 0.1 + self.__timeOut:
			self.__timeCount = 0.0
			if self.__animationUp:
				self.__currentBackgroundId = self.__currentBackgroundId +1
			else:
				self.__currentBackgroundId = self.__currentBackgroundId -1
			if self.__currentBackgroundId == 0:
				self.__animationUp = True
				self.__timeOut = .8 * self.__playerHealth
			elif self.__currentBackgroundId == 2:
				self.__heartBeatSound.play()
				self.__animationUp = False
				self.__timeOut = .0
			else:
				self.__timeOut = .0
			self._background = self._backgrounds[self.__currentBackgroundId]


	def display2D(self,delta=0):
		#Actionbar zeichnen
		self.drawBackground()
		Control.display2D(self,delta)
