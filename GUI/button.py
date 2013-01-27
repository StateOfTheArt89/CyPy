#!/usr/bin/python
# -*- coding: utf-8 -*-

from control import *
from glhelper import *

class Button(Control):

	_imageNormal = 0
	_imagePressed = 0

	_actionOnPress = 0
	_actionObject = 0

	def __init__(self,x,y,width,height,imageNormal,imagePressed):
		Control.__init__(self,x,y,width,height)
		self._imageNormal = loadTexture(imageNormal)
		self._imagePressed = loadTexture(imagePressed)

	def display2D(self,delta=0):
		glEnable(GL_TEXTURE_2D)
		if self._isPressed:
			glBindTexture(GL_TEXTURE_2D, self._imagePressed)
		else:
			glBindTexture(GL_TEXTURE_2D, self._imageNormal)
		glColor(1,1,1,1)
		glBegin(GL_QUADS)
		glTexCoord(0,1)
		glVertex(self._x,self._y + self._height,1)
		glTexCoord(1,1)
		glVertex(self._x + self._width,self._y + self._height,1)
		glTexCoord(1,0)
		glVertex(self._x + self._width,self._y,1)
		glTexCoord(0,0)
		glVertex(self._x,self._y,1)
		glEnd()


