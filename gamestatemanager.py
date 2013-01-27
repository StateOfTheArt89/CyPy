#!/usr/bin/python
# -*- coding: utf-8 -*-

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from pybass.pybass import *
try:
	from PIL.Image import open
except ImportError, err:
	from Image import open
import sys

from GameStates.introgamestate import *
from GameStates.quitgamestate import QuitGameState
from GameStates.ingamestate import InGameState
from GameStates.menugamestate import MenuGameState

class GameStateManager(object):

	NONE = "NONE"
	INTRO = "INTRO"
	MENU = "MENU"
	INGAME = "INGAME"
	QUIT = "QUIT"
	__updateDelay = True
	__game = None

	allStates = (MENU, INGAME, QUIT)

	def __init__(self, game, initialState):
		#Alle GameState initialisieren
		self._currentState = initialState
		self._statesDict = {}
		self.__game = game
		inGameState = InGameState("InGame",self)
		menuGameState = MenuGameState("Menu",self)
		introGameState = IntroGameState("Intro",self)
		quitGameState = QuitGameState("Quit",self)
		self._statesDict[GameStateManager.INGAME] = inGameState
		self._statesDict[GameStateManager.MENU] = menuGameState
		self._statesDict[GameStateManager.INTRO] = introGameState
		self._statesDict[GameStateManager.QUIT] = quitGameState
		#...weitere States

		self.changeGameState(initialState)

	def getHealth(self):
		try:
			return self._statesDict[GameStateManager.INGAME].getHealth()
		except:
			return 1.0

	def getGame(self):
		return self.__game

	def display3D(self, delta):
		currentStateObj = self._statesDict[self._currentState]
		currentStateObj.display3D(delta)

	def display2D(self, delta):
		currentStateObj = self._statesDict[self._currentState]
		currentStateObj.display2D(delta)
		self.__renderDelay = False


	def update(self, delta):
		if self.__updateDelay:
			self.__updateDelay = False
			return
		currentStateObj = self._statesDict[self._currentState]
		currentStateObj.update(delta)

	def getCurrentGameState(self):
		return self._statesDict[self._currentState]

	def changeGameState(self, newState):
		self._statesDict[self._currentState].stop()
		self._currentState = newState
		self.__updateDelay = True

		currentStateObj = self._statesDict[self._currentState]
		glutMouseFunc(currentStateObj.mouseClick)
		glutPassiveMotionFunc(currentStateObj.mouse)
		glutMotionFunc(currentStateObj.mouse)

		glutSpecialFunc(currentStateObj.special)
		glutSpecialUpFunc(currentStateObj.specialup)
		glutKeyboardFunc(currentStateObj.keyboard)
		glutKeyboardUpFunc(currentStateObj.keyboardup)

		self._statesDict[self._currentState].start()
