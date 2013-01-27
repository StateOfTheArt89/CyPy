#!/usr/bin/python
# -*- coding: utf-8 -*-

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from glhelper import *

class Control(object):
	_x = 0
	_y = 0
	_width = 0
	_height = 0
	_background = None
	_isPressed = False

	_actionOnPress = None
	_actionArgs = None

	_children = None
	_isEnabled = False
	_isVisible = False

	def __init__(self,x,y,width,height,backgroundPath=None):
		self._x = x
		self._y = y
		self._width = width
		self._height = height
		self._children = []
		self._isEnabled = True
		self._isVisible = True
		if backgroundPath is not None:
			self._background = loadTexture(backgroundPath)

	def isVisible(self):
		return self._isVisible

	def isPressed(self):
		return self._isPressed

	def setVisible(self, value):
		self._isVisible = value

	def isEnabled(self):
		return self._isEnabled

	def setEnabled(self, value):
		self._isEnabled = value

	def setPosition(self, x, y):
		xDiff = x - self._x
		yDiff = y - self._y
		self._x = x
		self._y = y
		for child in self._children:
			childX, childY = child.getPosition()
			child.setPosition(childX + xDiff, childY + yDiff)

	def getX(self):
		return self._x

	def setX(self, value):
		self.setPosition(value, self._y)

	def getY(self):
		return self._y

	def setY(self, value):
		self.setPosition(self._x, value)

	X = property(getX, setX)
	Y = property(getY, setY)

	def getPosition(self):
		return self._x, self._y

	def addChild(self, childElement):
		self._children.append(childElement)

	def removeChild(self, childElement):
		self._children.remove(childElement)

	def display2D(self, delta):
		if self._isVisible:
			for child in self._children:
				child.display2D(delta)

	def mouse(self,x,y):
		for child in self._children:
			child.mouse(x,y)

	def mouseClick(self, button, state, x, y):
		if not self._isEnabled:
			return False
		result = False
		for child in self._children:
			if child.mouseClick(button, state, x, y):
				result = True
		if x > self._x and x < self._x + self._width and y > self._y and y < self._y + self._height:
			self._isPressed = state == GLUT_DOWN
			if (not self._isPressed and self._actionOnPress is not None and self._actionArgs is not None):
				args = self._actionArgs
				self._actionOnPress(*args)
			result = True
		return result

	def keyboard(self, key, x, y):
		for child in self._children:
			child.keyboard(key, x, y)

	def keyboardup(self, key, x, y):
		for child in self._children:
			child.keyboardup(key, x, y)

	def update(self, delta):
		for child in self._children:
			child.update(delta)

	def drawBackground(self):
		#Transparenz erlauben
		glEnable(GL_BLEND)
		glEnable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D, self._background)
		glColor(1,1,1,1)
		glBegin(GL_QUADS)
		glTexCoord(0,1)
		glVertex(self._x,self._y + self._height,-0.5)
		glTexCoord(1,1)
		glVertex(self._x + self._width,self._y + self._height,-0.5)
		glTexCoord(1,0)
		glVertex(self._x + self._width,self._y,-0.5)
		glTexCoord(0,0)
		glVertex(self._x,self._y,-0.5)
		glEnd()

	def setAction(self,action, actionArgs):
		self._actionOnPress = action
		self._actionArgs = actionArgs
