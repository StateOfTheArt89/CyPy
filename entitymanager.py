#!/usr/bin/python
# -*- coding: utf-8 -*-

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from entity import Entity

class EntityManager(object):
	__entities = []
	__focus = None
	__game = None
	TALKDISTANCE = 1.0

	def __init__(self, game):
		self.__entities = []
		self.__focus = None
		self.__game = game


	def createEntity(self, receipe):
		e = Entity(self.__game,receipe)
		self.__entities.append(e)
		return e

	def setFocus(self, entity):
		self.__focus = entity

	def getFocus(self):
		return self.__focus

	def getEntities(self):
		return self.__entities

	def display3D(self, delta,pazz="default"):
		for e in self.__entities:
			e.display3D(delta,pazz)

	def update(self, delta):
		self.__entities = [item for item in self.__entities if not item.canBeRemoved()]

		for e in self.__entities:
			e.update(delta)

	def mouse(self, x, y):
		if self.__focus != None:
			self.__focus.call("onMouseMove",x,y)

	def mouseClick(self, button, state, x, y):
		if self.__focus != None:
			if state == GLUT_DOWN:
				return self.__focus.call("onMouseDown",button,x,y)
			elif state == GLUT_UP:
				return self.__focus.call("onMouseUp",button,x,y)
		return False

	def keyboard(self, key, x, y):
		if self.__focus != None:
			if key == ' ':
				for e in self.__entities:
					if (e.getPosition() - self.__focus.getPosition()).length < self.TALKDISTANCE:
						e.call("onSpace",self.__focus)
			self.__focus.call("onKeyDown",key)

	def keyboardup(self, key, x, y):
		if self.__focus != None:
			self.__focus.call("onKeyUp",key)

	def special(self, key, x, y):
		if self.__focus != None:
			self.__focus.call("onSpecialDown",key)

	def specialup(self, key, x, y):
		if self.__focus != None:
			self.__focus.call("onSpecialUp",key)