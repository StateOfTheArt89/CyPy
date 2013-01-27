from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from io import *

class BasicShader(object):

	def __init__(self):
		self.__vertex = compileShader(open(string).read(),GL_VERTEX_SHADER)
		self.__fragment = 0
		self.__program = 0

	def loadVertexShader(self, string):
		self.__vertex = compileShader(open(string).read(),GL_VERTEX_SHADER)

	def loadFragmentShader(self, string):
		self.__fragment = compileShader(open(string).read(),GL_FRAGMENT_SHADER)

	def compileShader(self):
		self.__shader = compileProgram(self.__vertex,self.__fragment)

	def bind(self):
		glUseProgram(self.__program)