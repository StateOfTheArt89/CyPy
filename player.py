#!/usr/bin/python
# -*- coding: utf-8 -*-

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import json
import math
import io
from Foundation.vector import Vector
from particle import ParticleEmitter
try:
	from PIL.Image import open
except ImportError, err:
	from Image import open
import sys

from glhelper import *

def minimum_distance(v, w, p):
	len2 = (v-w).get_length_sqrd(); 
	if len2 == 0.0:
		return (p - v).length,Vector(0,0,0)
	t = (p - v).dot(w-v) / len2
	if t < 0.:
		return (p - v).length,Vector(0,0,0)
	if t > 1.:
		return (p - w).length,Vector(0,0,0)
	projection = v + t * (w - v)
	le = (p - projection).length
	v2 = projection.cross(Vector(0,0,1))
	return le, v2

class Player:
	__tex = 0L
	__position = Vector(10.,10.,0.)
	__velocity = Vector(0.,0.,0.)
	__direction = 1
	__phase = 1
	__rotation = 0
	__rotationto = 0
	__dir = 1
	__map = None
	__shootdelay = 0.
	__shots = []

	__delme = 0
	def __init__(self, g):
		self.__tex = loadTexture("Sprites/Player/CharacterAnimationFinalish2.png")

	def setMap(self, map2):
		self.__map = map2

	def move(self,x,y):
		self.__velocity = Vector(x,y,0)
		self.__velocity = self.__velocity.normalized()
		self.__velocity *= 3

	def getPosition(self):
		return self.__position


	def display3D(self,delta):

		

		glColor4f(1,1,1,1)

		glPushMatrix()
		ismoving = False
		if self.__velocity.length != 0:
			ismoving = True
			self.__rotationto = math.degrees(math.atan2(self.__velocity[1],
									  	  			    self.__velocity[0]))+90


		torotate = self.__rotationto - self.__rotation
		if torotate > 180:
			torotate -= 360
		self.__rotation += torotate * delta * 10.
		x,y,z = self.__position
		
		glTranslate(x,y,z)
		glRotatef(self.__rotation,0,0,1)
		glEnable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D, self.__tex)

		glBegin(GL_QUADS)

		u,v = (self.__phase % 8)/8., (self.__direction)/8.
		u2,v2 = u + 1/8., v + 1/8.
		
		x = -0.5
		y = -0.5
		z = 0.5
		glTexCoord(u,v2)
		glVertex(x,y,z)
		glTexCoord(u2,v2)
		glVertex(x+1,y,z)
		glTexCoord(u2,v)
		glVertex(x+1,y+1,z)
		glTexCoord(u,v)
		glVertex(x,y+1,z)			

		glEnd()
		glPopMatrix()
		


		if self.__delme % 50 == 0 and ismoving: 
			self.__phase = (self.__phase + self.__dir)

			if self.__phase >= 5 or self.__phase == 0:
				self.__dir *= -1
		if not ismoving:
			self.__phase = 3
		# if self.__delme % 800 == 0:
		# 	self.__direction = (self.__direction + 1) % 10
		self.__delme += 1



		for s in self.__shots:
			s.display3D(delta)

	def shoot(self,x,y,z):
		self.__rotation = self.__rotationto = math.degrees(math.atan2(y-self.__position.y,x - self.__position.x))+90

		if self.__shootdelay <= 0.:
			emitter = ParticleEmitter(loadTexture("Textures/tex1.png"),1)
			emitter.setPosition(self.getPosition())
			emitter.setStartVelocity(Vector(10,0,0).rotated_around_z((self.__rotation)-90.))
			emitter.emit()
			self.__shots.append(emitter)
			self.__shootdelay = .1



	
		
	def update(self, delta):
		if self.__map == None:
			return

		self.__shots = [item for item in self.__shots if not item.isDead()]


		for s in self.__shots:
			s.update(delta)

		self.__shootdelay = max(0.,self.__shootdelay - delta)



		bbsize = 0.3
		ldist = 0.2

		noff = [[bbsize,bbsize],[-bbsize,-bbsize],[bbsize,-bbsize],[-bbsize,bbsize]]
		
		walls = self.__map.getWalls()
		
		props = self.__map.getTile(self.__position + Vector(0,0,self.__map.LAYERHEIGHT*1))
		try:
			if props["stair"] == "ny":
				walls = []
				
				for off in noff:
					h = self.__map.getHeight(self.__position + Vector(off[0],off[1],0))
					self.__position.z = max(self.__position.z,h)
				print "height:"+str(self.__position.z)
					
				noff = []
		except Exception as e:
		
			pass

		epsilon = 0.26

		newpos = Vector(self.__position)
		newpos.x += self.__velocity.x * delta * 0.5
		solid = False
		hit = Vector(0,0,0)
		for off in noff:
			checkpos = newpos + Vector(off[0],off[1],self.__map.LAYERHEIGHT)
			if self.__map.isSolid(checkpos):
				solid = True
			for w in walls:
				p1 = Vector(w[0])
				if abs(round(p1.z / self.__map.LAYERHEIGHT) - round(checkpos.z / self.__map.LAYERHEIGHT)) - 1.0 > epsilon:
					continue

				
				p2 = Vector(w[1])
				p1.z = 0
				p2.z = 0
				checkpos2 = Vector(checkpos)
				checkpos2.z = 0
				diff = p2 - p1
				length = diff.length
				dist,ort = minimum_distance(p1,p2,checkpos2)
				#print dist
				if dist < ldist:
					hit = ort
					solid = True

		if not solid:
			self.__position = newpos
	

		newpos = Vector(self.__position)
		newpos.y += self.__velocity.y * delta + hit.y * delta * 0.1
		solid = False
		hit = Vector(0,0,0)
		for off in noff:
			checkpos = newpos + Vector(off[0],off[1],self.__map.LAYERHEIGHT)
			if self.__map.isSolid(checkpos):
				solid = True
			for w in walls:
				p1 = Vector(w[0])
				if abs(round(p1.z / self.__map.LAYERHEIGHT) - round(checkpos.z / self.__map.LAYERHEIGHT)) - 1.0 > epsilon:
					continue
				p2 = Vector(w[1])
				p1.z = 0
				p2.z = 0
				checkpos2 = Vector(checkpos)
				checkpos2.z = 0
				diff = p2 - p1
				length = diff.length

				dist, ort = minimum_distance(p1,p2,checkpos2)
				#print dist
				if dist < ldist:
					hit = ort
					solid = True
		if not solid:
			self.__position = newpos





		newpos = Vector(self.__position)
		newpos.x += self.__velocity.x * delta * 0.5 + hit.x * delta * 0.1
		solid = False
		hit = Vector(0,0,0)
		for off in noff:
			checkpos = newpos + Vector(off[0],off[1],self.__map.LAYERHEIGHT)
			if self.__map.isSolid(checkpos):
				solid = True
			for w in walls:
				p1 = Vector(w[0])
				if abs(round(p1.z / self.__map.LAYERHEIGHT) - round(checkpos.z / self.__map.LAYERHEIGHT)) - 1.0 > epsilon:
					continue
				p2 = Vector(w[1])
				p1.z = 0
				p2.z = 0
				checkpos2 = Vector(checkpos)
				checkpos2.z = 0
				diff = p2 - p1
				length = diff.length
				dist,ort = minimum_distance(p1,p2,checkpos2)
				#print dist
				if dist < ldist:
					hit = ort
					solid = True

		if not solid:
			self.__position = newpos
		


		if len(noff) != 0:
			newpos = Vector(self.__position)
			newpos.z += -1.0 * delta
			solid = False
			for off in noff:
				checkpos = self.__position + Vector(off[0],off[1],self.__map.LAYERHEIGHT)
				if self.__map.isSolid(checkpos):
					solid = True
			if not solid:
				self.__position = newpos



		

		print "Player Height:"+str(self.__position.z)
		#print "Walls: "+str(walls)
	

