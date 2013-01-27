#!/usr/bin/python
# -*- coding: utf-8 -*-

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from framebuffer import *

try:
	from PIL.Image import open
except ImportError, err:
	from Image import open

texes = {}

def loadTexture(string, mipmapping=False):
	h = hash(string)
	if h in texes:
		return texes[h]

	im = open(string)
	
	ix, iy, image = im.size[0], im.size[1], im.convert("RGBA").tostring("raw", "RGBA")
	
	ID = glGenTextures(1)
	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D, ID)
	glPixelStorei(GL_UNPACK_ALIGNMENT,1)
	if not mipmapping:
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP);
		glTexImage2D(GL_TEXTURE_2D, 0, 4, ix, iy, 0,GL_RGBA, GL_UNSIGNED_BYTE, image)
	else:
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_LINEAR)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP);
		gluBuild2DMipmaps(GL_TEXTURE_2D, 4, ix, iy,GL_RGBA, GL_UNSIGNED_BYTE, image)
	glBindTexture(GL_TEXTURE_2D, 0)
	texes[h] = ID
	return ID

def createFBO(w,h):
	return FrameBuffer(w,h)

def atlasUV(i,sx,sy):
	u,v = (i % sx)/float(sx), (i // sy)/float(sy)
	u2,v2 = u + 1/float(sx), v + 1/float(sy)
	u += 0.0002
	v += 0.0002
	u2 -= 0.0002
	v2 -= 0.0002
	return u,v,u2,v2
		

def glWindowPos(x,y,z=0.0,w=1.0):
	viewport = glGetIntegerv( GL_VIEWPORT )
	y = viewport[3] - y
	glPushAttrib( GL_TRANSFORM_BIT | GL_VIEWPORT_BIT )
	glMatrixMode( GL_PROJECTION )
	glPushMatrix()
	glLoadIdentity()
	glMatrixMode( GL_MODELVIEW )
	glPushMatrix()
	glLoadIdentity()
	glDepthRange( z, z )
	glViewport( int(x) - 1, int(y) - 1, 2, 2 )
	fx = x - int(x)
	fy = y - int(y)
	glRasterPos4f( fx, fy, 0.0, w )
	glPopMatrix()
	glMatrixMode( GL_PROJECTION )
	glPopMatrix()
	glPopAttrib()

def printString(x,y,string):
	glColor(1,1,1,1)
	glWindowPos(x, y + 15)
	for c in string:
		glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
