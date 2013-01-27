#!/usr/bin/python
# -*- coding: utf-8 -*-

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from control import *
from button import *

class ToolTip(Control):

	__itemIcon = None
	__text = ""

	def __init__(self,x,y,text):
		Control.__init__(self,x,y,150,150,"Sprites/GUI/tooltip.png")
		self.__text = text

	def display2D(self, delta):
		if self._isEnabled and self._isVisible:
			self.drawBackground()