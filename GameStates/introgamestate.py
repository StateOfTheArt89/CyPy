#!/usr/bin/python
# -*- coding: utf-8 -*-

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import sys

from conversation import Conversation, Answer
from gamestate import GameState
from GUI.textbox import TextBox

class IntroGameState(GameState):

	__textbox = None
	__gamestatemanager = None

	def __init__(self, name, gamestatemanager):
		self.__gamestatemanager = gamestatemanager
		try:
			introText = open("Text Dialogue and Intro/Story intro.txt").read()
		except:
			introText = "Langes Intro..."
		introConversation = Conversation(introText,[])
		okAnswer = Answer("Beginne dein Abenteuer...", IntroGameState.startGame, [self])
		introConversation.addAnswer(okAnswer)
		self.__textbox = TextBox(introConversation)

	def startGame(self):
		self.__gamestatemanager.changeGameState("INGAME")

	def display2D(self, delta):
		self.__textbox.display2D(delta)

	def update(self, delta):
		self.__textbox.update(delta)

	def keyboardup(self, key, x, y):
		GameState.keyboardup(self, key, x, y)
		self.__textbox.keyboardup(key, x, y)

	def mouseClick(self, button, state, x, y):
		if not self.__textbox.mouseClick(button, state, x, y):
			self.startGame()
