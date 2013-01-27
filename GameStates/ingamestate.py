#!/usr/bin/python
# -*- coding: utf-8 -*-

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
try:
	from PIL.Image import open
except ImportError, err:
	from Image import open
import sys

from gamestate import *
from glhelper import *

from map import Map
from Shaders.basicshader import BasicShader  
from player import Player
from particle import *

from GUI.pausemenu import *
from GUI.itemmenu import *
from GUI.actionbar import *
from GUI.textbox import *
from sound import *
from entity import *
from entitymanager import *

#GameState für das Hauptspiel
class InGameState(GameState):
	mouseX = 0
	mouseY = 0

	cursorX = 0.0
	cursorY = 0.0
	cursorZ = 0.0

	translateX = 0.
	translateY = 0.

	testemit = None

	__actionBar = None
	__itemmenu = None
	__pauseMenu = None

	__backgroundMusic = None
	__entitymanager = None

	def __init__(self, name, gamestatemanager):
		GameState.__init__(self,name, gamestatemanager)
		self.__actionBar = ActionBar(100,476,800,100)
		self.__itemmenu = ItemMenu(0,0,1024,576,"Sprites/GUI/IngameGui.png")
		testAnswer = Answer("Falsche Antwort...",sys.exit,[])
		testConversation = Conversation("Bla bla",[])
		testConversation.addAnswer(testAnswer)
		self.__textBox = TextBox(testConversation)
		self.__textBox.setEnabled(False)
		self.__textBox.setVisible(False)
		self.__pauseMenu = PauseMenu(0,0,1024,576,gamestatemanager)
		self.__pauseMenu.setEnabled(False)


	def getEntityManager(self):
		return self.__entitymanager

	def start(self):
		GameState.start(self)

		self.load()
	
	def stop(self):
		GameState.stop(self)
		if self.__backgroundMusic is not None:
			self.__backgroundMusic.stop()

	def loadMap(self, string):
	#		self.__dict__[string.rsplit('.')[0]] = Map(self,string)
		return Map(self,string)

	def getHealth(self):
		return self.__entitymanager.getFocus().health

	def load(self):
		self.__fbo = createFBO(self._gamestatemanager.getGame().width,self._gamestatemanager.getGame().height)
		self.__glow_fbo = createFBO(self._gamestatemanager.getGame().width,self._gamestatemanager.getGame().height)

		self.__shader = BasicShader()
		self.test = self.loadMap("Maps/CyPyGGJ.json")
		self.__backgroundMusic = Sound("Music/Sketches/cyberpunkOverworld-Sketch1.mp3",True)
		self.__backgroundMusic.play()
		self.__entitymanager = EntityManager(self._gamestatemanager.getGame())
		player = self.__entitymanager.createEntity("Entities/player.json")
		player.setPosition(self.test.getStartPosition())
		self.__entitymanager.setFocus(player)
		self.__entitymanager.createEntity("Entities/enemy.json")
		self.__entitymanager.createEntity("Entities/gun.json").setPosition(Vector(15,15,0))
		self.__entitymanager.createEntity("Entities/gun.json").setPosition(Vector(12,15,0))
		self.__entitymanager.createEntity("Entities/gun.json").setPosition(Vector(15,12,0))
		self.__entitymanager.createEntity("Entities/light.json").setPosition(Vector(15,15,0))
		self.__entitymanager.createEntity("Entities/fog.json").setPosition(Vector(30,30,0))
		self.__entitymanager.createEntity("Entities/fog.json").setPosition(Vector(5,30,0))
		self.__entitymanager.createEntity("Entities/fog.json").setPosition(Vector(30,5,0))

	def update3DCursor(self):
		modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
		projection = glGetDoublev(GL_PROJECTION_MATRIX)
		viewport = glGetIntegerv(GL_VIEWPORT) 
		winX = float(self.mouseX)
		winY = float(viewport[3] - float(self.mouseY))
		winZ = glReadPixels(self.mouseX,int(winY), 1,1,GL_DEPTH_COMPONENT, GL_FLOAT)
		(self.cursorX,self.cursorY,self.cursorZ) = gluUnProject( winX, winY, winZ[0][0], modelview, projection, viewport )

	def mouseClick(self, button, state, x, y):
		if not self.__actionBar.mouseClick(button, state, x, y) and not self.__entitymanager.mouseClick(button, state,x,y) and not self.__textBox.mouseClick(button, state, x, y):
			GameState.mouseClick(self,button,state,x,y)
		self.__itemmenu.mouseClick(button, state, x, y)
		self.__pauseMenu.mouseClick(button, state, x, y)


	def mouse(self, x, y):
		GameState.mouse(self,x,y)
		self.__entitymanager.mouse(x,y)
		self.__itemmenu.mouse(x,y)
		self.mouseX = x
		self.mouseY = y

	def showText(self,text,onclose,args):
		testAnswer = Answer("Das war dein letztes Wort",onclose,args)
		testAnswer2 = Answer("Deine Mudda",onclose,args)
		testConversation = Conversation("Gayorg: \nCyPy? Das klingt ja wie GayPy!",[])
		testConversation.addAnswer(testAnswer)
		testConversation.addAnswer(testAnswer2)
		self.__textBox = TextBox(testConversation)
		self.__textBox_onClose = onclose
		self.__textBox_onClose_args = args


	def keyboard(self, key, x, y):
		GameState.keyboard(self, key, x, y)
		if key == ' ':
			if self.__textBox.isVisible():
				self.__textBox.setVisible(False)
				self.__textBox_onClose(*self.__textBox_onClose_args)
				key = 0 #hack
		self.__entitymanager.keyboard(key,x,y)
		self.__actionBar.keyboard(key, x, y)
		self.__itemmenu.keyboard(key, x, y)

	def keyboardup(self, key, x, y):
		GameState.keyboardup(self, key, x, y)
		self.__entitymanager.keyboardup(key,x,y)
		self.__actionBar.keyboardup(key, x, y)
		self.__itemmenu.keyboardup(key, x, y)
		self.__textBox.keyboardup(key, x, y)
		if key == 'p':
			self.__pauseMenu.setEnabled(True)

	def special(self, key, x, y):
		if key == 27:
			sys.exit(0)
		self.specialkeys[key] = True
		self.__entitymanager.special(key,x,y)

	def specialup(self, key, x, y):
		self.specialkeys[key] = False
		self.__entitymanager.special(key,x,y)


	def display3D(self, delta):
		self.__fbo.begin()
		glClearColor(0,0,0,0);
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT );
		

		glPushMatrix()
		self.translateX = min(-self._gamestatemanager.getGame().width / 140.0,self.translateX)
		self.translateY = min(-self._gamestatemanager.getGame().height / 140.0,self.translateY)
		

		glTranslate(self.translateX, self.translateY,0)
		self.test.display3D(delta)
		self.update3DCursor()
		self.__entitymanager.display3D(delta)
		
		if self.testemit != None:
			self.testemit.display3D(delta)

		glPopMatrix()
		#self.__shader.unbind()
		self.__fbo.end()

		self.__glow_fbo.begin()
		glClearColor(0,0,0,0);
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT );
		

		glPushMatrix()
		self.translateX = min(-self._gamestatemanager.getGame().width / 140.0,self.translateX)
		self.translateY = min(-self._gamestatemanager.getGame().height / 140.0,self.translateY)
		
		
		glTranslate(self.translateX, self.translateY,0)
		self.__entitymanager.display3D(delta,"glow")
		glPopMatrix()
		self.__glow_fbo.end()


	def display2D(self, delta):
		glClearColor(1.,1.,1.,1.)
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
		
		glActiveTexture(GL_TEXTURE1)
		self.__glow_fbo.bind()
		glActiveTexture(GL_TEXTURE0)
		
		self.__shader.bind()
		self.__fbo.display2D(delta)
		glActiveTexture(GL_TEXTURE1)
		glBindTexture(GL_TEXTURE_2D,0)
		glActiveTexture(GL_TEXTURE0)
		
		self.__shader.unbind()
		self.__itemmenu.display2D(delta)
		self.__actionBar.display2D()
		self.__textBox.display2D(delta)
		self.__pauseMenu.display2D(delta)
		self.__shader.unbind()
		print glGetError()

	def getMap(self):
		return self.test

	def centerOn(self, entity):
		pos = entity.getPosition()

		self.translateX = -pos.x
		self.translateY = -pos.y

	def update(self, delta):

		for e in self.__entitymanager.getEntities():
			self.test.trigger(e)
		self.__entitymanager.update(delta)
		self.__itemmenu.setEntity( self.__entitymanager.getFocus())
		self.__itemmenu.update(delta)
		self.__actionBar.update(delta)
		self.__actionBar.setPlayerHealth(self.getHealth())



	
