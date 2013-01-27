#!/usr/bin/python
# -*- coding: utf-8 -*-

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import math
from OpenGL.GL.framebufferobjects import *

class FrameBuffer(object):
	def begin(self):
		if not self.__framebuffer:
			print "ERROR: fbo not loaded"
			return

		glBindTexture(GL_TEXTURE_2D, 0);
		glDisable(GL_TEXTURE_2D);
		glBindFramebuffer(GL_FRAMEBUFFER, self.__framebuffer)
		glPushAttrib(GL_VIEWPORT_BIT)
		glViewport(0,0,int(self.__width), int(self.__height))

	def end(self):
		glPopAttrib()
		glBindFramebuffer(GL_FRAMEBUFFER, 0)

	def bind(self):		
		glColor4f(1,1,1,1)
		glEnable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D,self.__texture)


	def getWidth(self):
		return self.__width

	def getHeight(self):
		return self.__height

	def __nextpo2(self,val):
			return 2**(int(math.log(val-1, 2))+1)

	def display2D(self,delta):
		self.bind()
		glBegin(GL_QUADS)
		glTexCoord(0.,self.hs)
		glVertex(0,0,0)
		glTexCoord(self.ws,self.hs)
		glVertex(self.getWidth(),0.,0.)
		glTexCoord(self.ws,0)
		glVertex(self.getWidth(),self.getHeight(),0.)
		glTexCoord(0.,0)
		glVertex(0,self.getHeight(),0.)
		glEnd()

	def __init__(self,w,h):
		
		self.__width = w
		self.__height = h

		w = self.__nextpo2(w)
		h = self.__nextpo2(h)

		self.ws = self.__width / float(w)
		self.hs = self.__height / float(h)


		glEnable(GL_TEXTURE_2D)
		self.__texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, self.__texture)
		glPixelStorei(GL_UNPACK_ALIGNMENT,1)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
		glBindTexture(GL_TEXTURE_2D, 0)
		
		self.__framebuffer = glGenFramebuffers(1)
		glBindFramebuffer(GL_FRAMEBUFFER, self.__framebuffer)
		
		glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.__texture, 0)
		
		self.__depth_buffer = glGenRenderbuffers(1)
		glBindRenderbuffer(GL_RENDERBUFFER, self.__depth_buffer)
		glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT24, w, h,)
		
	

		glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.__depth_buffer)

		if glCheckFramebufferStatus(GL_FRAMEBUFFER) == GL_FRAMEBUFFER_COMPLETE:
			print "FBO complete"
		try:
			
			checkFramebufferStatus()
		except Exception, err:
			traceback.print_exc()
			import os
			os._exit(1)
		glBindFramebuffer(GL_FRAMEBUFFER, 0)
		glBindRenderbuffer(GL_RENDERBUFFER,0)