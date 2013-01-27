#!/usr/bin/python
# -*- coding: utf-8 -*-
import io
import itertools
from entity import Entity

class Trigger(object):
	__script = None
	__entered = []
	def __init__(self,o):
		self.__receipe = o
		props = o.get("properties",{})
		self.__receipe["x"] /= 64.
		self.__receipe["y"] /= 64.
		self.__receipe["width"] /= 64.
		self.__receipe["height"] /= 64.
		self.__entered = []
		if "script" in props:
			self.__script = compile(io.open(props["script"]).read(),"<string>","exec")

	def trigger(self, entity):
		x = self.__receipe["x"]
		y = self.__receipe["y"]
		w = self.__receipe["width"]
		h = self.__receipe["height"]
		x2 = entity.getPosition().x
		y2 = entity.getPosition().y

		if x2 >= x and y2 >= y and x2 <= x+w and y2 <= y+h:
			if not (entity in self.__entered):
				self.call("onEnter",entity)
				self.__entered.append(entity)
			else:
				self.call("onStay",entity)
		else:
			if (entity in self.__entered):
				self.call("onLeave",entity)
				self.__entered.remove(entity)



		


	def call(self, method, *args):
		if method in self.__script.co_names:
			#game = self.__game
			# gamestate = self.__game.getGameStateManager().getCurrentGameState()
			# entitymanager = gamestate.getEntityManager()
			# keys =  gamestate.keys
			# specialkeys = gamestate.specialkeys
			# mouseL = gamestate.mouseL
			# mouseR = gamestate.mouseR
			# mouseM = gamestate.mouseM
			# cursorX = gamestate.cursorX
			# cursorY = gamestate.cursorY
			# cursorZ = gamestate.cursorZ
			# current_animation = self.__animation
			
			# position = self.__position
			# velocity = self.__velocity
			# alpha = self.__alpha



			exec(self.__script,locals(),globals())
			call_method = method+"("+(",".join(itertools.chain(["self"],["args["+str(x)+"]" for x in range(len(args))])))+")"
			exec(call_method,locals(),globals())
			

