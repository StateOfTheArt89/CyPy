#!/usr/bin/python
# -*- coding: utf-8 -*-

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from pybass.pybass import *

import gamestatemanager as gs

class Game(object):
	height = 576
	width = 1024
	_delta = 0.

	def __init__(self):
		# INIT SOUND
		result = BASS_Init(-1, 44100, 0, 0, 0)
		if not result:
			bass_error_code = BASS_ErrorGetCode()
			if bass_error_code != BASS_ERROR_ALREADY:
				print 'BASS_Init error', get_error_description(bass_error_code)

		self.fovto = 44.
		self.fov = 44.

		# INIT GLUT
		glutInit(sys.argv)
		glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)

		glutInitWindowSize(self.width,self.height)
		glutCreateWindow("CyPy v1.00")
		if not glUseProgram:
			print 'Missing Shader Objects!'
			sys.exit(1)
		glutReshapeFunc(self.resize)
		glutDisplayFunc(self.display)
		glutIdleFunc(self.display)

		glClearColor(0.,0.,0.,0.)
		glShadeModel(GL_SMOOTH)
		glEnable(GL_CULL_FACE)
		glEnable(GL_DEPTH_TEST)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)



		self._gamestatemanager = gs.GameStateManager(game=self,initialState=gs.GameStateManager.MENU)

		glutMainLoop()

	def getGameStateManager(self):
		return self._gamestatemanager

	def display(self):
		startTime = glutGet(GLUT_ELAPSED_TIME); 
		self._gamestatemanager.update(self._delta)

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glPushMatrix()
		glLoadIdentity()
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		self.fovto = 44 * (0.5 + 0.5 * (self._gamestatemanager.getHealth()))
		self.fov += (self.fovto - self.fov)*0.1
		gluPerspective(self.fov,self.width/float(self.height),1.0,40.0)
		glMatrixMode(GL_MODELVIEW)

		glTranslate(0,0,-10)
		
		self._gamestatemanager.display3D(self._delta)

		glPopMatrix()
		glMatrixMode(GL_PROJECTION)
		glPushMatrix()
		glLoadIdentity()
		gluOrtho2D(0,self.width,self.height,0)
		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		glLoadIdentity()
		glDisable(GL_CULL_FACE)
		glDepthMask(GL_FALSE)
		self._gamestatemanager.display2D(self._delta)
		glDepthMask(GL_TRUE)
		glEnable(GL_CULL_FACE)
		glMatrixMode(GL_PROJECTION)
		glPopMatrix()
		glMatrixMode(GL_MODELVIEW)
		glPopMatrix()

		glutSwapBuffers()
		self._delta = (glutGet(GLUT_ELAPSED_TIME) - startTime) / 1000.

	def resize(self, width, height):
		self.width = width
		self.height = height
		glViewport(0,0,width,height)
		

if __name__ == '__main__': Game()