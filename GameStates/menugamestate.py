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

from GUI.actionbar import *
from GUI.button import *
from GUI.textbox import *
from gamestate import *
from glhelper import *

class MenuGameState(GameState):

	__backgroundImage = None
	__logoImage = None
	__startGameButton = None
	__quitButton = None
	_gamestatemanager = None

	def __init__(self, name, gamestatemanager):
		GameState.__init__(self,name, gamestatemanager)
		self.__backgroundImage = loadTexture("Sprites/GUI/menuBackground.png")
		self.__logo = loadTexture("Sprites/GUI/LogoCyPy.png")
		self.__startGameButton = Button(416,300,192,64,"Sprites/GUI/Startbutton.png","Sprites/GUI/StartbuttonPressed.png")
		self.__quitButton = Button(416,400,192,64,"Sprites/GUI/Quitbutton.png","Sprites/GUI/QuitbuttonPressed.png")
		self.__startGameButton.setAction(MenuGameState.startGame, [self])
		self.__quitButton.setAction(MenuGameState.quitGame, [self])

	def startGame(self):
		self._gamestatemanager.changeGameState("INTRO")

	def quitGame(self):
		self._gamestatemanager.changeGameState("QUIT")

	def keyboard(self, key, x, y):
		GameState.keyboard(self, key, x, y)

	def keyboardup(self, key, x, y):
		GameState.keyboardup(self, key, x, y)

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
		#Logo
		glBindTexture(GL_TEXTURE_2D, self.__logo)
		glColor(1,1,1,1)
		glBegin(GL_QUADS)
		glTexCoord(0,0)
		glVertex(410,40,0)
		glTexCoord(1.,0)
		glVertex(613,40,0)
		glTexCoord(1.,1)
		glVertex(613,236,0)
		glTexCoord(0,1)
		glVertex(410,236,0)
		glEnd()
		#Controls
		self.__startGameButton.display2D()
		self.__quitButton.display2D()

	def mouseClick(self, button, state, x, y):
		self.__startGameButton.mouseClick(button, state, x, y)
		self.__quitButton.mouseClick(button, state, x, y)

