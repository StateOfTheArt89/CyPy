#!/usr/bin/python
# -*- coding: utf-8 -*-

from control import *
from glhelper import *

class ActionBarItem(Control):

	_background = None
	_realWidth = 0
	_realHeight = 0
	_realX = 0
	_realY = 0
	_actionKey = ""

	_isActionKeyPressed = False
	_isPressedCoolDown = 0.15

	def __init__(self,x,y,width,height,background,actionKey=""):
		Control.__init__(self,x,y,width,height,background)
		self._realHeight = height
		self._realWidth = width
		self._realX = x
		self._realY = y
		self._actionKey = actionKey

	def update(self, delta):
		if self._isActionKeyPressed:
			self._isPressedCoolDown -= delta
			if self._isPressedCoolDown < 0:
				self._isActionKeyPressed = False

	def keyboardup(self, key, x, y):
		if key == self._actionKey:
			if self._actionOnPress is not None and self._actionArgs is not None:
				args = self._actionArgs
				self._actionOnPress(*args)
			self._isActionKeyPressed = True
			self._isPressedCoolDown = 0.15

	def display2D(self, delta):
		#Eindrück-Effekt
		if self._isPressed or self._isActionKeyPressed:
			self._width = self._realWidth - 4
			self._height = self._realHeight - 4
			self._x = self._realX + 2
			self._y = self._realY + 2
		else:
			self._width = self._realWidth
			self._height = self._realHeight
			self._x = self._realX
			self._y = self._realY
		self.drawBackground()