#!/usr/bin/python
# -*- coding: utf-8 -*-

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from Foundation.vector import *
import random
# EMIT TYPES
SHOOT = 1
EXPLOSION = 2

class ParticleEmitter(object):
	__tex_id = 0
	__position = None
	__start_velocity = None
	__particles = []
	__type = 0
	__startscale = 1.



	def __init__(self, tex_id, _type=EXPLOSION):
		self.__tex_id = tex_id
		self.__position = Vector(0,0,0)
		self.__particles = []
		self.__type = _type
		self.__startscale = 1.

	def setStartVelocity(self, velocity):
		self.__start_velocity = velocity
		

	def setPosition(self, position):
		self.__position = position

	def isDead(self):
		for p in self.__particles:
			if not p.isDead():
				return False
		return True

	def setScale(self, scale):
		self.__startscale = scale



	def emit(self, num=1,special=True):
		for i in xrange(0,num):
			p = Particle(self, self.__tex_id, self.__type)
			if self.__type == SHOOT:
				p.__position = Vector(0,0,0)
				p.setVelocity(self.__start_velocity)
				p.setScale(self.__startscale)
			elif self.__type == EXPLOSION:
				p.__position = Vector(0,0,0)
				vel = Vector(random.random() * 2. - 1., random.random() * 2. - 1.,0)
				vel = vel.normalized() * 10
				p.setVelocity(vel)
				p.setScale(self.__startscale)
				if special: 
					p.setSpecial(0 if random.randint(0,8)!=0 else 1)
				else:
					p.setSpecial(0) 
			self.__particles.append(p)
		return p

	def display3D(self, delta):
		glPushMatrix()
		glTranslate(self.__position.x,
					self.__position.y,
					self.__position.z)
		glEnable(GL_TEXTURE_2D)
		glEnable(GL_BLEND)
		glDepthMask(GL_FALSE)
		glBindTexture(GL_TEXTURE_2D,self.__tex_id)
		
		for p in self.__particles:
			p.display3D(delta)
		
		glDepthMask(GL_TRUE)
		glPopMatrix()

	def update(self, delta):
		for p in self.__particles:
			p.update(delta)


class Particle(object):

	__tex_id = 0
	__position = None
	__velocity = None
	__alpha = 1.
	__type = 0
	__special = 0
	__cumdist = 0
	__emitter = None
	__scale = 1.
	def __init__(self, emitter, tex_id, _type):
		self.__tex_id = tex_id
		self.__position = Vector(0,0,0)
		self.__velocity = Vector(0,0,0)
		self.__type = _type
		self.__emitter = emitter
		self.__scale = 1.
		self.__alpha = 1.

	def isDead(self):
		return self.__scale < 0.01 or self.__alpha < 0.01

	def setVelocity(self, vel):
		self.__velocity = vel

	def setScale(self, scale):
		self.__scale = scale

	def setSpecial(self, val):
		self.__special = val

	def display3D(self, delta):
		scale = self.__scale
		
		if self.isDead():
			return

		x = self.__position.x
		y = self.__position.y 
		z = self.__position.z
		glPushMatrix()
		glBegin(GL_QUADS)
		glColor(1,1,1,self.__alpha)
		glTexCoord(0,0)
		glVertex(-scale + x, -scale + y, z)
		glTexCoord(1,0)
		glVertex( scale + x, -scale + y, z)
		glTexCoord(1,1)
		glVertex( scale + x,  scale + y, z)
		glTexCoord(0,1)
		glVertex(-scale + x,  scale + y, z)
		glEnd()
		glPopMatrix()
		
	def update(self, delta):
		oldpos = Vector(self.__position)
		self.__position += self.__velocity * delta
		self.__cumdist += (self.__position - oldpos).get_length()
		if self.__special == 1 and self.__cumdist > 0.5:
			p = self.__emitter.emit(1,False)
			p.__position = Vector(self.__position)
			p.__velocity = Vector(0,0,0)
			p.__scale = self.__scale
			p.__alpha = self.__alpha
			self.__cumdist = 0

		if self.__type == EXPLOSION:
			self.__alpha *= (1. - 0.01 * delta * 100)
			self.__scale *= (1. - 0.01 * delta * 100)
			if self.__special == 0:
				self.__velocity *= (1. - (0.12 + random.random() * 0.1)*delta*50)
			else:
				self.__velocity *= (1. - 0.03*delta*100)
		if self.__type == SHOOT:
			self.__scale *= (1. - 0.02 * delta * 100)
