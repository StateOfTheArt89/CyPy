#!/usr/bin/python
# -*- coding: utf-8 -*-

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import sys

class GameState(object):

	keys = {}
	specialkeys = {}
	mouseL = False
	mouseR = False
	mouseM = False

	def __init__(self, name, gamestatemanager):
		self._name = name
		self._gamestatemanager = gamestatemanager

	def display2D(self, delta):
		pass

	def display3D(self, delta):
		pass
	
	def update(self, delta):
		#Spiellogik
		pass

	def start(self):
		for c in range(0,256):
			self.keys[chr(c)] = False
		for c in range(0,256):
			self.specialkeys[c] = False

	def stop(self):
		#GameState stoppen
		pass

	def mouse(self, x, y):
		pass

	def mouseClick(self, button, state, x, y):
		if button ==  GLUT_LEFT_BUTTON:
			self.mouseL = True if state == GLUT_DOWN else False
		elif button == GLUT_MIDDLE_BUTTON:
			self.mouseM = True if state == GLUT_DOWN else False
		elif button == GLUT_RIGHT_BUTTON:
			self.mouseR = True if state == GLUT_DOWN else False

		pass

	def keyboard(self, key, x, y):
		self.keys[key] = True

	def keyboardup(self, key, x, y):
		self.keys[key] = False

	def special(self, key2, x, y):
		pass

	def specialup(self, key2, x, y):
		pass

	def resize(self, width, height):
		pass
