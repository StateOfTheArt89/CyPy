#!/usr/bin/python
# -*- coding: utf-8 -*-
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from control import *
from glhelper import *

from GUI.button import *
from conversation import *

class TextBox(Control):

	font = GLUT_BITMAP_HELVETICA_12
	_text = ""
	_conversation = None
	_textColor = (1.,1.,1.,1.)
	_answerTextColor = (1.,0.,1.,1.)
	_backgroundImage = None

	_x = 287
	_y = 106
	_width = 450
	_height = 300

	__textWidth = 0
	__textHeigth = 0
	__textX = 0
	__textY = 0
	__vscrollto = 0.
	__vscroll = 0.

	__beginOfTextY = 0

	_upButton = None
	_downButton = None

	def __init__(self,conversation):
		Control.__init__(self,self._x,self._y,self._width,self._height,"Sprites/GUI/TextboxBack.png")
		self.__textWidth = self._width - 80
		self.__textHeigth = self._height - 20
		self.__textX = self._x + 30
		self.__textY = self._y + 20
		self.__vscroll = 0.
		self.__vscrollto = 0.
		self._text = conversation.getText().decode("utf-8").encode("ISO-8859-1")

		self._conversation = conversation
		self._upButton = Button(690,140,25,25,"Sprites/GUI/ScrollPfeilUp.png","Sprites/GUI/ScrollPfeilUpPressed.png")
		self.addChild(self._upButton)
		self._upButton.setAction(TextBox.scroll,[self,10.])
		self._downButton = Button(690,340,25,25,"Sprites/GUI/ScrollPfeilDown.png","Sprites/GUI/ScrollPfeilDownPressed.png")
		self._downButton.setAction(TextBox.scroll,[self,-10.])
		self.addChild(self._downButton)

	def scroll(self,amount):
		self.__vscrollto += amount

	def update(self, delta):
		if self._upButton.isPressed():
			self.scroll(delta*80)
		if self._downButton.isPressed():
			self.scroll(-delta*80)

	def keyboardup(self, key, x, y):
		for i in range(10):
			if i >= len(self._conversation.getAnswers()):
				break
			if key == str(i) and self._conversation.getAnswers()[i] is not None:
				self._conversation.getAnswers()[i].chooseThis()
				self.setEnabled(False)
				self.setVisible(False)
		Control.keyboardup(self, key, x, y)

	def mouseClick(self, button, state, x, y):
		if not self._isEnabled:
			return False
		result = Control.mouseClick(self, button, state, x, y)

		if x > self.__textX and x < self.__textX + self.__textWidth:
			startOfAnswersY = self.__beginOfTextY + self.__vscroll + self.__textY
			answerId = int((y-startOfAnswersY)/20)
			result = True
			if answerId >= 0 and answerId < len(self._conversation.getAnswers()):
				self._conversation.getAnswers()[answerId].chooseThis()
				self.setEnabled(False)
				self.setVisible(False)
		return result

	def display2D(self, delta):
		if not self.isVisible():
			return
		glPushMatrix()

		self.__vscroll += (self.__vscrollto - self.__vscroll)*delta
		#glTranslatef(0,self.__vscroll,0)
		self.drawBackground()

		splittedText = self._text.split(" ")
		glColor(*(self._textColor))
		currentCursorX = 0
		currentCursorY = 15
		glScissor(int(self.__textX), int(self.__textY + 25 + 45), int(self._width), int(self._height-45))
		glEnable(GL_SCISSOR_TEST)

		glColor4f(0,0,0,1)
		glDisable(GL_TEXTURE_2D)
		glBegin(GL_QUADS)
		glVertex(0,0,0.9)
		glVertex(4000,0,0.9)
		glVertex(4000,self._y,0.9)
		glVertex(0,self._y,0.9)
		glEnd()
		glColor4f(1,1,1,1)

		glWindowPos(self.__textX + currentCursorX, self.__textY + currentCursorY + self.__vscroll)
		glDisable(GL_TEXTURE_2D)

		for textpart in splittedText:
			expectedLength = self.getStringLength(textpart)
			if expectedLength + currentCursorX > self.__textWidth:
				currentCursorY += 20
				currentCursorX = 0
				glWindowPos(self.__textX, self.__textY + currentCursorY + self.__vscroll)
			for c in textpart:
				glutBitmapCharacter(self.font, ord(c))
				currentCursorX += glutBitmapWidth(self.font, ord(c))
			glutBitmapCharacter(self.font, ord(" "))
			currentCursorX += glutBitmapWidth(self.font, ord(" "))

		glColor(*(self._answerTextColor))
		currentCursorX = 0
		currentCursorY += 20
		self.__beginOfTextY = currentCursorY
		glWindowPos(self.__textX, self.__textY + currentCursorY + self.__vscroll)
		counter = 1
		answers = self._conversation.getAnswers()
		for answer in answers:
			currentCursorY += 20
			glWindowPos(self.__textX, self.__textY + currentCursorY + self.__vscroll)
			for c in (str(counter) + ". " + answer.getText()):
				glutBitmapCharacter(self.font, ord(c))
				currentCursorX += glutBitmapWidth(self.font, ord(c))
			counter += 1

		Control.display2D(self, delta)
		glDisable(GL_SCISSOR_TEST)
		glPopMatrix()


	def getStringLength(self, string):
		length = 0
		for c in string:
			length += glutBitmapWidth(self.font, ord(c))
		return length

