#!/usr/bin/python
# -*- coding: utf-8 -*-

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from glhelper import *
import gamestatemanager
import game
import math
import itertools
from particle import *


from Foundation.vector import Vector
import json
import io

global_id = 0

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

class Entity(object):
	__receipe = {}
	__tex = 0
	__position = Vector(0.,0.,0.)
	__velocity = Vector(0.,0.,0.)
	__rotation = 0.
	__rotationto = 0.
	__texture_slicex = 0
	__texture_slicey = 0
	__size = []
	__offset = []
	__frame = 0
	__id = 0
	__emitter = []
	__animation = None
	__frame = 0.
	__animation_pause = False
	__animation_dir = 1.
	__transparent = False
	__can_be_removed = False
	__alpha = 1.
	__owner = None
	__collectible = False
	__collected = False
	__collidable = True
	__inventory = []


	def __init__(self,game, receipe):
		global global_id
		self.__receipe = json.load(io.open(receipe))
		self.__script = None
		self.__game = game
		if "script" in self.__receipe:
			self.__script = compile(io.open(self.__receipe["script"]).read(),"<string>","exec")
		self.__tex = loadTexture(self.__receipe.get("texture","defaultTexturePathMissing"))
		self.__texture_slicex = self.__receipe.get("texture_slice_x",1)
		self.__texture_slicey = self.__receipe.get("texture_slice_y",1)
		self.__size = self.__receipe.get("size",[32,32])
		self.__offset = self.__receipe.get("offset",[-0.5,-0.5,-0.5])
		self.__frame = 0
		self.__id = global_id + 1
		self.__emitter = []
		self.__animation = None
		self.__frame = 0.
		self.__animation_pause = False
		self.__animation_dir = 1.
		self.__velocity = Vector(0,0,0)
		self.__position = Vector(0,0,0)
		self.__rotation = 0.
		self.__transparent = self.__receipe.get("transparent",False)
		self.__can_be_removed = False
		self.__alpha = 1.
		self.__owner = None
		self.__collectible = self.__receipe.get("collectible",False)
		self.__collected = False
		self.__collidable = True
		self.__inventory = []
		self.__texture2d = None
		self.__glow = self.__receipe.get("glow",False)
		path2d = self.__receipe.get("texture2d",None)
		if path2d != None:
			self.__texture2d = loadTexture(path2d)
		global_id += 1

		self.call("onInit")

	def setOwner(self, owner):
		self.__owner = owner

	def getOwner(self):
		return self.__owner

	def getInventory(self):
		return self.__inventory

	def addItem(self, ent):
		self.__inventory.append(ent)


			

	def call(self, method, *args):
		if method in self.__script.co_names:
			#game = self.__game
			gamestate = self.__game.getGameStateManager().getCurrentGameState()
			entitymanager = gamestate.getEntityManager()
			keys =  gamestate.keys
			specialkeys = gamestate.specialkeys
			mouseL = gamestate.mouseL
			mouseR = gamestate.mouseR
			mouseM = gamestate.mouseM
			cursorX = gamestate.cursorX
			cursorY = gamestate.cursorY
			cursorZ = gamestate.cursorZ
			current_animation = self.__animation
			
			position = self.__position
			velocity = self.__velocity
			alpha = self.__alpha



			exec(self.__script,locals(),globals())
			call_method = method+"("+(",".join(itertools.chain(["self"],["args["+str(x)+"]" for x in range(len(args))])))+")"
			exec(call_method,locals(),globals())
			
	def isPlayable(self):
		return self.__receipe.get("playable",False)

	def getName(self):
		return self.__receipe.get("name","unknown")

	def setName(self, name):
		self.__name = name

	def remove(self):
		self.__can_be_removed = True

	def getPosition(self):
		return self.__position

	def isCollectible(self):
		return self.__collectible

	def isCollidable(self):
		return self.__collidable

	def collect(self, by):
		self.call("onCollectedBy",by)
		self.__owner = by
		self.__collected = True
		self.__collidable = False

	def drop(self):
		self.__position = self.__owner.getPosition()
		self.__collected = False
		self.__owner = None
		self.__collidable = True

	def getVelocity(self):
		return self.__velocity

	def setPosition(self, pos):
		self.__position = pos

	def setVelocity(self, vel):
		self.__velocity = vel

	def setRotation(self, rot):
		self.__rotation = self.__rotationto = rot

	def rotateTo(self,rot):
		self.__rotationto = rot

	def getRotation(self):
		return self.__rotation

	def isMoving(self):
		return self.__velocity.length > 0.01

	def startAnimation(self, name):
		for a in self.__receipe["animations"]:
			if a.get("name","unknown") == name:
				self.__animation = a
				self.__frame = a["start"]
				self.__animation_pause = False

	def pauseAnimation(self):
		self.__animation_pause = True

	def resumeAnimation(self):
		self.__animation_pause = False

	def setAlpha(self, alpha):
		self.__alpha = alpha

	def canBeRemoved(self):
		return self.__can_be_removed




	def display3D(self,delta,pazz="default"):
		if self.__can_be_removed or self.__collected:
			return

		if pazz == "glow" and not self.__glow:
			return
		elif self.__glow and pazz != "glow":
			return


		glColor4f(1,1,1,self.__alpha)

		if self.__transparent:
			glDepthMask(GL_FALSE)

		glPushMatrix()

		#if self.isMoving():
		#self.__rotationto = math.degrees(math.atan2(self.__velocity[1],self.__velocity[0]))+90


		torotate = self.__rotationto - self.__rotation
		if torotate > 180:
			torotate -= 360
		self.__rotation += torotate * delta * 10.
	
		
		
		glTranslate(self.__position.x, self.__position.y, self.__position.z)
		glRotatef(self.__rotation,0,0,1)

		glEnable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D, self.__tex)

		u,v,u2,v2 = atlasUV(round(self.__frame), self.__texture_slicex, self.__texture_slicey)
		s = self.__size

		


		x,y,z = self.__offset

		glBegin(GL_QUADS)
		glTexCoord(u,v2)
		glVertex(x,y,z)

		glTexCoord(u2,v2)
		glVertex(x+s[0],y,z)

		glTexCoord(u2,v)
		glVertex(x+s[0],y+s[1],z)

		glTexCoord(u,v)
		glVertex(x,y+s[1],z)		

		glEnd()

		glPopMatrix()



		self.call("onRender",delta)


		for e in self.__emitter:
			e.display3D(delta)


		if self.__transparent:
			glDepthMask(GL_TRUE)


	def updateCollision(self, delta):
		# TODO: make Bounding box more arbritary
		bbsizex, bbsizey = self.__receipe["bounding_box"]
		bbsizex /= 2.
		bbsizey /= 2.

		ldist = min(bbsizex, bbsizey)

		noff = [[bbsizex,bbsizey],[-bbsizex,-bbsizey],[bbsizex,-bbsizey],[-bbsizex,bbsizey]]
		
		current_map = self.__game.getGameStateManager().getCurrentGameState().getMap()

		walls = current_map.getWalls()
		
		props = current_map.getTile(self.__position + Vector(0,0,current_map.LAYERHEIGHT))

		epsilon = 0.26

		newpos = Vector(self.__position)
		newpos.x += self.__velocity.x * delta * 0.5
		solid = False
		impdist = 5
		hit = Vector(0,0,0)

		def nearwall(p1,p2,pos):
			x1 = p1.x
			x2 = p2.x
			if x1 > x2:
				x1,x2 = x2,x1
			y1 = p1.y
			y2 = p2.y
			if y1 > y2:
				y1,y2 = y2,y1

			return pos.inPlanarRect([x1-1.5,y1-1.5,x2+1.5,y2+1.5])

		for off in noff:
			checkpos = newpos + Vector(off[0],off[1],current_map.LAYERHEIGHT*1.1)
			if current_map.isSolid(checkpos):
				solid = True
			for w2 in walls:
				for w in w2["colllines"]:
					p1 = Vector(w[0])
					p2 = Vector(w[1])
					if not nearwall(p1,p2,newpos):
						continue

					if abs(round(p1.z / current_map.LAYERHEIGHT) - round(checkpos.z / current_map.LAYERHEIGHT)) - 1.0 > epsilon:
						continue




					
					
					p1.z = 0
					p2.z = 0
					checkpos2 = Vector(checkpos)
					checkpos2.z = 0
					diff = p2 - p1
					length = diff.length
					dist,ort = minimum_distance(p1,p2,checkpos2)
					#print dist
					if dist < ldist:
						#hit = ort
						solid = True

		if not solid:
			self.__position = newpos
		else:
			self.call("onCollision",newpos)
	

		newpos = Vector(self.__position)
		newpos.y += self.__velocity.y * delta + hit.y * delta * 0.1
		solid = False
		hit = Vector(0,0,0)
		for off in noff:
			checkpos = newpos + Vector(off[0],off[1],current_map.LAYERHEIGHT)
			if current_map.isSolid(checkpos):
				solid = True
			for w2 in walls:
				for w in w2["colllines"]:
					p1 = Vector(w[0])
					p2 = Vector(w[1])
					if not nearwall(p1,p2,newpos):
						continue
					
					if abs(round(p1.z / current_map.LAYERHEIGHT) - round(checkpos.z / current_map.LAYERHEIGHT)) - 1.0 > epsilon:
						continue

					

					
					p1.z = 0
					p2.z = 0
					checkpos2 = Vector(checkpos)
					checkpos2.z = 0
					diff = p2 - p1
					length = diff.length

					dist, ort = minimum_distance(p1,p2,checkpos2)
					#print dist
					if dist < ldist:
						#hit = ort
						solid = True
		if not solid:
			self.__position = newpos
		else:
			self.call("onCollision",newpos)





		newpos = Vector(self.__position)
		newpos.x += self.__velocity.x * delta * 0.5 + hit.x * delta * 0.1
		solid = False
		hit = Vector(0,0,0)
		for off in noff:
			checkpos = newpos + Vector(off[0],off[1],current_map.LAYERHEIGHT)
			if current_map.isSolid(checkpos):
				solid = True
			for w2 in walls:
				for w in w2["colllines"]:
					p1 = Vector(w[0])
					p2 = Vector(w[1])
					if not nearwall(p1,p2,newpos):
						continue
					

					if abs(round(p1.z / current_map.LAYERHEIGHT) - round(checkpos.z / current_map.LAYERHEIGHT)) - 1.0 > epsilon:
						continue
					
					p1.z = 0
					p2.z = 0
					checkpos2 = Vector(checkpos)
					checkpos2.z = 0
					diff = p2 - p1
					length = diff.length
					dist,ort = minimum_distance(p1,p2,checkpos2)
					#print dist
					if dist < ldist:
						#hit = ort
						solid = True

		if not solid:
			self.__position = newpos
		else:
			self.call("onCollision",newpos)

		gamestate = self.__game.getGameStateManager().getCurrentGameState()
		entitymanager = gamestate.getEntityManager()
		for e in entitymanager.getEntities():
			if not e.isCollidable():
				continue
			if e == self:
				continue
			# todo coll detect improve
			dist = (e.getPosition() - self.getPosition()).length
			if dist < 0.5:
				self.call("onCollision",e)


		# if len(noff) != 0:
		# 	newpos = Vector(self.__position)
		# 	newpos.z += -1.0 * delta
		# 	solid = False
		# 	for off in noff:
		# 		checkpos = self.__position + Vector(off[0],off[1],current_map.LAYERHEIGHT*0.5)
		# 		if current_map.isSolid(checkpos):
		# 			solid = True
		# 	if not solid:
		# 		self.__position = newpos
			self.__position.z = 0.0

	def shoot(self,_dir,speed=10.):
		emitter = ParticleEmitter(loadTexture("Textures/tex1.png"),1)
		emitter.setPosition(self.getPosition() + Vector(0,0,0.25))
		emitter.setScale(.15)
		emitter.setStartVelocity(_dir.normalized() * 10)
		emitter.emit()
		self.__emitter.append(emitter)

	def updateAnimation(self, delta):
		self.__frame += delta * self.__animation["fps"] * self.__animation_dir
		anim_type = self.__animation.get("type","default")
		if anim_type == "default":
			if self.__frame >= self.__animation["end"]:
				self.__frame = self.__animation["start"]
		elif anim_type == "pingpong":
			if self.__frame > self.__animation["end"]:	
				self.__animation_dir = -1.
			elif self.__frame <= self.__animation["start"]:
				self.__animation_dir = 1.

	def display2D(self, delta):
		if self.__texture2d == None:
			return
		glEnable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D,self.__texture2d)
		glPushMatrix()
		glBegin(GL_QUADS)
		glTexCoord(0,0)
		glVertex(0,0,0)
		glTexCoord(1,0)
		glVertex(32,0,0)
		glTexCoord(1,1)
		glVertex(32,32,0)
		glTexCoord(0,1)
		glVertex(0,32,0)
		glEnd()
		glPopMatrix()


	def update(self, delta):
		if self.__can_be_removed or self.__collected:
			return
		self.call("onUpdate",delta)
		self.__emitter = [item for item in self.__emitter if not item.isDead()]
		for e in self.__emitter:
			e.update(delta)
		if "bounding_box" in self.__receipe:
			self.updateCollision(delta)
		if "animations" in self.__receipe and self.__animation != None and not self.__animation_pause:
			self.updateAnimation( delta)
		

