#!/usr/bin/python
# -*- coding: utf-8 -*-

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from control import *
from GUI.button import *
from GUI.tooltip import *

class ItemMenu(Control):
	__buttonScrollRight = None
	__buttonScrollLeft = None

	__tooltip = None

	yOutOfSight = 600

	_isVisible = False
	_isInAnimation = False

	_realY = 0
	scrollingSpeed = 0

	def __init__(self,x,y,width,height,backgroundPath):
		Control.__init__(self,x,y,width,height,backgroundPath)
		self._realY = y
		self.__buttonScrollLeft = Button(634,470,25,25,"Sprites/GUI/ItemPfeilLinks.png","Sprites/GUI/ItemPfeilLinksPressed.png")
		self.__buttonScrollRight = Button(810,470,25,25,"Sprites/GUI/ItemPfeilRechts.png","Sprites/GUI/ItemPfeilRechtsPressed.png")
		self.addChild(self.__buttonScrollLeft)
		self.addChild(self.__buttonScrollRight)
		self.__tooltip = ToolTip(-300,-300,"bla bla")
		self.addChild(self.__tooltip)
		self.Y = 600
		self.__entity = None
		self.__mouseX = 0
		self.__mouseY = 0
		self.__draggin = None
		self._isVisible = False
		self.itemStartX = 632 + self.X
		self.itemStartY = 114 + self.Y
		self.itemBorder = 12

	def setEntity(self,ent):
		self.__entity = ent

	def hide(self):
		self._isInAnimation = True
		self.scrollingSpeed = 2
		self._isVisible = True

	def show(self):
		self._isInAnimation = True
		self.scrollingSpeed = -2
		self._isVisible = True

	def isVisible(self):
		return self._isVisible

	def update(self, delta):
		Control.update(self, delta)
		if self._isInAnimation:
			if self.scrollingSpeed < 0:
				self.Y += (self.Y - self._realY) * delta * self.scrollingSpeed
			else:
				self.Y += (self.yOutOfSight - self.Y) * delta * self.scrollingSpeed

			if self.Y <= (self._realY + 5) and self.scrollingSpeed < 0:
				self._isInAnimation = False
				self.Y = self._realY
			elif self.Y > (self.yOutOfSight - 50) and self.scrollingSpeed > 0:
				self._isVisible = False
				self._isInAnimation = False
				self.Y = self.yOutOfSight

	def keyboardup(self, key, x, y):
		Control.keyboardup(self, key, x, y)
		if key == "i":
			if self.isVisible():
				self.hide()
			else:
				self.show()

	head = (495, 123)
	lshoulder = (425, 191)
	lhand = (426, 274)
	lung = (494, 198)
	liver = (495, 260)
	lleg = (465, 358)
	rshoulder = (562, 193)
	rhand = (565, 276)
	rleg = (524, 358)

	def mouse(self,x,y):
		for element in (self.head, self.lshoulder, self.lhand, self.lung, self.liver, self.lleg, self.rshoulder, self.rhand, self.rleg):
			if x > element[0] and x < element[1]+32 and y > element[1] and y < element[1]+32:
				self.__tooltip.setPosition(x,y)
		self.__mouseX = x
		self.__mouseY = y
		Control.mouse(self,x,y)

	def mouseClick(self, button, state, x, y):
		if button == GLUT_LEFT_BUTTON:
			if state == GLUT_DOWN:
				if x > self.itemStartX and y > self.itemStartY and x < self.itemStartX + (self.itemBorder + 32) * 5 - self.itemBorder and y < self.itemStartY + (self.itemBorder + 32) * 8:
					ix = (x - self.itemStartX) // (self.itemBorder + 32)
					iy = (y - self.itemStartY) // (self.itemBorder + 32)
					i = int(iy * 5 + ix)
					if i < len(self.__entity.getInventory()):
						self.__draggin = self.__entity.getInventory()[i]
						self.__entity.getInventory().remove(self.__draggin)
				else:
					if self.__entity.lhand != None:
						p = self.lhand
						if x > p[0] and y > p[1] and x < p[0]+32 and y < p[1]+32:
							self.__draggin = self.__entity.lhand
							self.__entity.lhand = None

					if self.__entity.rhand != None:
						p = self.rhand
						if x > p[0] and y > p[1] and x < p[0]+32 and y < p[1]+32:
							self.__draggin = self.__entity.rhand
							self.__entity.rhand = None

			if state == GLUT_UP and self.__draggin != None:
			
				if self.__entity.lhand == None:
					p = self.lhand
					if x > p[0] and y > p[1] and x < p[0]+32 and y < p[1]+32:
						self.__entity.lhand = self.__draggin
						self.__draggin = None

				if self.__entity.rhand == None:
					p = self.rhand
					if x > p[0] and y > p[1] and x < p[0]+32 and y < p[1]+32:
						self.__entity.rhand = self.__draggin
						self.__draggin = None




				if self.__draggin != None:
					self.__entity.getInventory().append(self.__draggin)
					self.__draggin = None


				
				#drop
				pass
		Control.mouseClick(self, button, state, x, y)

	def display2D(self, delta):
		if self.__entity == None:
			return
		if not self._isVisible:
			return

		self.drawBackground()


		self.itemStartX = 632 + self.X
		self.itemStartY = 114 + self.Y
		self.itemBorder = 12
		glPushMatrix()
		glTranslatef(self.itemStartX,self.itemStartY,0)
		for e in self.__entity.getInventory():
			e.display2D(delta)
			glTranslatef(self.itemBorder + 32,0,0)
		glPopMatrix()

		if self.__draggin != None:
			glPushMatrix()
			glTranslatef(self.__mouseX, self.__mouseY,0)
			self.__draggin.display2D(delta)

			glPopMatrix()

		if self.__entity.lhand != None:
			glPushMatrix()
			glTranslatef(self.lhand[0],self.lhand[1]+self.Y,0)
			self.__entity.lhand.display2D(delta)

			glPopMatrix()

		if self.__entity.rhand != None:
			glPushMatrix()
			glTranslatef(self.rhand[0],self.rhand[1]+self.Y,0)
			self.__entity.rhand.display2D(delta)

			glPopMatrix()

		self.__tooltip.display2D(delta)
		Control.display2D(self, delta)
