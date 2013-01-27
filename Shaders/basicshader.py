#!/usr/bin/python
# -*- coding: utf-8 -*-

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from io import *
from OpenGL.GL import shaders

class BasicShader(object):
	def __init__(self):
		self.__vertex = shaders.compileShader(open("Shaders/basicvertex.vs").read(),GL_VERTEX_SHADER)
		self.__fragment = shaders.compileShader(open("Shaders/basicfragment.fs").read(),GL_FRAGMENT_SHADER)
		self.__program = shaders.compileProgram(self.__vertex,self.__fragment)

	def bind(self):
		glUseProgram(self.__program)
		glUniform1i(glGetUniformLocation(self.__program,"tex"),0)
		glUniform1i(glGetUniformLocation(self.__program,"glow"),1)

	def unbind(self):
		glUseProgram(0)