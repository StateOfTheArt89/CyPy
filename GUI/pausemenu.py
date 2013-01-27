#!/usr/bin/python
# -*- coding: utf-8 -*-

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from control import *
from button import *

class PauseMenu(Control):

	__resumeButton = None
	__exitButton = None

	__gamemanager = None

	def __init__(self,x,y,width,height,gamemanager):
		Control.__init__(self,x,y,width,height,"Sprites/GUI/IngameEscapeMenu.png")
		self.__gamemanager = gamemanager
		self.__resumeButton = Button(400,104,220,50,"Sprites/GUI/IngameEscapeMenuResume2.png","Sprites/GUI/IngameEscapeMenuResumePressed2.png")
		self.__resumeButton.setAction(PauseMenu.resumeGame,[self])
		self.addChild(self.__resumeButton)
		self.__exitButton = Button(400,284,220,50,"Sprites/GUI/IngameEscapeMenuQuit2.png","Sprites/GUI/IngameEscapeMenuQuitPressed2.png")
		self.__exitButton.setAction(PauseMenu.exitGame,[self])
		self.addChild(self.__exitButton)

	def resumeGame(self):
		self.setEnabled(False)

	def exitGame(self):
		if self.__gamemanager is not None:
			self.setEnabled(False)
			self.__gamemanager.changeGameState("MENU")


	def display2D(self, delta):
		if self._isEnabled and self._isVisible:
			self.drawBackground()
			Control.display2D(self, delta)

