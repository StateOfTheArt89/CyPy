#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Verbindet Antwort mit einer Funktion, die ausgeführt wird, wenn die Antwort ausgewählt wird'''
class Answer(object):
	_text = ""
	_function = None
	_args = None

	def __init__(self, text, function, args):
		self._text = text
		self._function = function
		self._args = args

	def getText(self):
		return self._text

	def chooseThis(self):
		self._function(*(self._args))


''' Klasse, die ein Gespräch mit NPCs repräsentiert '''
class Conversation(object):
	_text = ""
	_answers = None

	def __init__(self,text,answers):
		self._text = text
		self._answers = answers

	def addAnswer(self,answerObj):
		self._answers.append(answerObj)

	def getText(self):
		return self._text

	def getAnswers(self):
		return self._answers

	def chooseAnswer(id):
		self._answers[id].chooseThis()