#!/usr/bin/python
# -*- coding: utf-8 -*-

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
try:
	from PIL.Image import open
except ImportError, err:
	from Image import open
import sys

from GUI.itemmenu import *
from GUI.textbox import *
from gamestate import *
from glhelper import *

class QuitGameState(GameState):

	timeToShowShowScreen = 5.0
	__backgroundImage = None
	__timeCounter = 0.0

	def __init__(self, name, gamestatemanager):
		GameState.__init__(self,name, gamestatemanager)
		self.__backgroundImage = loadTexture("Sprites/GUI/quitScreen.png")

	def update(self, delta):
		self.__timeCounter += delta
		if self.__timeCounter > self.timeToShowShowScreen:
			sys.exit()

	def display2D(self, delta):
		width = glutGet(GLUT_WINDOW_WIDTH)
		height = glutGet(GLUT_WINDOW_HEIGHT)
		glEnable(GL_BLEND)
		glEnable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D, self.__backgroundImage)
		glColor(1,1,1,1)
		glBegin(GL_QUADS)
		glTexCoord(0,0)
		glVertex(0,0,0)
		glTexCoord(1.,0)
		glVertex(width,0,0)
		glTexCoord(1.,1)
		glVertex(width,height,0)
		glTexCoord(0,1)
		glVertex(0,height,0)
		glEnd()

	def keyboard(self, key, x, y):
		GameState.keyboard(self, key, x, y)

	def keyboardup(self, key, x, y):
		GameState.keyboardup(self, key, x, y)
