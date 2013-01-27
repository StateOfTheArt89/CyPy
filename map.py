#!/usr/bin/python
# -*- coding: utf-8 -*-

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import json
import io
try:
	from PIL.Image import open
except ImportError, err:
	from Image import open
import sys
import math
from Foundation.vector import Vector
from glhelper import *
from trigger import Trigger



class Map:
	__list = {} # opengl display lists
	
	# Render passes
	OPAQUE      = 0
	TRANSPARENT = 1

	# Map configuration
	LAYERHEIGHT = 0.5 # height of 1 layer
	WALLHEIGHT = 0.48

	# Map rendering configuration
	ATLASOFFSET = 0.001

	__walls = []
	__triggers = []
	__start = Vector(0,0,0)
	
	def __init__(self, g, mapname):
		# Load map
		self.__receipe = json.load(io.open(mapname))
		self.cook()

	def cook(self):
		tilesets = self.__receipe.get("tilesets",[])
		if len(tilesets) != 1:
			print("There is currently only one tileset per map supported")
			return
		self.__width = self.__receipe.get("width",0)
		self.__height = self.__receipe.get("height",0)

		tileinfo = []
		tileset = tilesets[0]
		self.__tex = loadTexture(tileset["image"].replace("..","."),True)
		firstgid = tileset.get("firstgid",1)
		props = tileset.get("tileproperties",{})
		for i in xrange(0,firstgid + 256):
			tprops = props.get(str(i-1),{})
			info = {}
			info.update(transparent=tprops.get("transparent","false") != "false")
			info.update(solid=tprops.get("solid","false") != "false")
			info.update(atlas=i-firstgid)
			tileinfo.append(info)

		#load tiles
		self.__tiles = []
		layers = self.__receipe.get("layers",[])
		for l in filter(lambda x:x.get("type","") == "tilelayer", layers):
			square = []
			x = 0
			row = []
			for i in xrange(self.__width):
				row.append([])
			for d in l.get("data",[]):
				tile = {"id":d}
				tile.update(tileinfo[d])
				row[x].append(tile)
				x+=1
				if x >= self.__width:
					#square.append(row)
					#row = []
					x = 0
			self.__tiles.append(row)

		self.__walls = []
		self.__triggers = []
		self.__start = Vector(0,0,0)
		for l in filter(lambda x:x.get("type","") == "objectgroup", layers):
			for o in l.get("objects",[]):
				o_type = o.get("type","")

				if o_type == "":
					o_type = "wall" #pniethen fix

				if o_type == "start":
					xs = (o.get("x",0) + o.get("width",64)/2) * 1/64.
					ys = (o.get("y",0) + o.get("height",64)/2) * 1/64.
					self.__start = Vector(xs,ys,0) #TODO: implement z
				elif o_type == "wall":
					wall = {}
					wall.update(top=int(o.get("properties",{}).get("top",5)))
					wall.update(side=int(o.get("properties",{}).get("side",15)))
					drawlines = [] # for rendering
					colllines = [] # for collision

					offset = Vector(o["x"]/64., o["y"]/64.,0.)#TODO: fixme
					
					last = Vector(0.,0.,0.)
					lastdraw = Vector(0.,0.,0.)
					lastset = False
					first = True
					vertex = 1
					pol = o.get("polyline",o.get("polygon",{}))
					for p in pol:
						cur = Vector(p["x"]/64.,p["y"]/64.,0.)
						curdraw = Vector(cur)
						if lastset:
							colllines.append([cur + offset, last + offset])

							diff2 = last - cur
							segments = int(math.ceil(diff2.length))

							for i in xrange(segments):
								if i > 0:
									drawlines.append([curdraw + offset, lastdraw+offset])
								diff = diff2.normalized()
								lastdraw = curdraw
								curdraw += diff							
						last = Vector(cur)
						lastset = True
						vertex += 1
					wall.update(colllines=colllines)
					wall.update(drawlines=drawlines)

					self.__walls.append(wall)
				elif o["type"] == "trigger":
					self.__triggers.append(Trigger(o))

	def trigger(self, entity):
		for t in self.__triggers:
			t.trigger(entity)

			
	def getHeight(self, vec):
		l = len(self.__tilelayers)-1
		x = int(vec.x)
		y = int(vec.y)

		return 0.0 #TODO: fixme

	def getTile(self, vec):
		l = int(vec.z / self.LAYERHEIGHT)
		x = int(vec.x)
		y = int(vec.y)

		try:
			return self.__tiles[l][x][y]
		except:
			return None

	def isSolid(self, vec):
		tile = self.getTile(vec)
		if tile == None:
			return True
		return tile["solid"]

	def getWalls(self):
		return self.__walls

	def getStartPosition(self):
		return self.__start


	def renderPass(self,pazz):
		if pazz not in self.__list or self.__list[pazz] is None:		
			self.__list[pazz] = glGenLists(1)
			glNewList(self.__list[pazz], GL_COMPILE_AND_EXECUTE);

			z = 0.0
			x = 0
			y = 0

			glEnable(GL_TEXTURE_2D)
			if pazz == self.TRANSPARENT:
				glDepthMask(GL_FALSE)
				glEnable(GL_BLEND)
			else:
				glDisable(GL_BLEND)

			glBegin(GL_QUADS)
			for l in self.__tiles:
				z+=0.001
				for y in range(len(l)):
					for x in range(len(l[y])):
						tile = l[x][y]

						if tile["id"] == 0 or ((not tile["transparent"]) and pazz == 1) or ((tile["transparent"]) and pazz == 0):
							continue

						
						u,v,u2,v2 = atlasUV(tile["atlas"],16,16)

						glTexCoord(u,v)
						glVertex(x,y,z)
						glTexCoord(u2,v)
						glVertex(x+1,y,z)
						glTexCoord(u2,v2)
						glVertex(x+1,y+1,z)
						glTexCoord(u,v2)
						glVertex(x,y+1,z)			
						
			if pazz == self.OPAQUE:
				for wall in self.__walls:
					lines = wall["colllines"]
					for l in lines:
						diff = l[1] - l[0]
						ortho = diff.normalized().cross(Vector(0,0,1)) * 0.25 * 0.5

						ve1 = l[0] + ortho 
						ve2 = l[1] + ortho
						ve3 = l[1] - ortho 
						ve4 = l[0] - ortho

						#print (ve1,ve2,ve3,ve4)

						u,v,u2,v2 = atlasUV(wall["top"],16,16)

						glTexCoord(u,v)
						glVertex(ve1 + Vector(0,0,self.WALLHEIGHT))
						glTexCoord(u2,v)
						glVertex(ve2 + Vector(0,0,self.WALLHEIGHT))
						glTexCoord(u2,v2)
						glVertex(ve3 + Vector(0,0,self.WALLHEIGHT))
						glTexCoord(u,v2)
						glVertex(ve4 + Vector(0,0,self.WALLHEIGHT))		


						u,v,u2,v2 = atlasUV(wall["side"],16,16)

						glTexCoord(u,v2)
						glVertex(ve1 + Vector(0,0,0))		
						glTexCoord(u2,v2)
						glVertex(ve2 + Vector(0,0,0))
						glTexCoord(u2,v)
						glVertex(ve2 + Vector(0,0,self.WALLHEIGHT))
						glTexCoord(u,v)
						glVertex(ve1 + Vector(0,0,self.WALLHEIGHT))

						glTexCoord(u,v2)
						glVertex(ve3 + Vector(0,0,0))		
						glTexCoord(u2,v2)
						glVertex(ve4 + Vector(0,0,0))
						glTexCoord(u2,v)
						glVertex(ve4 + Vector(0,0,self.WALLHEIGHT))
						glTexCoord(u,v)
						glVertex(ve3 + Vector(0,0,self.WALLHEIGHT))

						last = l[0]					
			glEnd()
			glDepthMask(GL_TRUE)
			glEndList()
		else:
			glCallList(self.__list[pazz])

	def display3D(self, delta):

		glBindTexture(GL_TEXTURE_2D, self.__tex)
		self.renderPass(self.OPAQUE)
		self.renderPass(self.TRANSPARENT)

	def update(self, delta):
		pass


