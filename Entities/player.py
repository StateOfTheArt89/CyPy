

def onInit(self):
	self.startAnimation("idle")
	self.__shootdelay = 0.

	self.rhand = None
	self.lhand = None
	self.head = None
	self.rshoulder = None
	self.lshoulder = None
	self.lung = None
	self.liver = None
	self.rleg = None

	self.experience = 0.
	self.strength = 10.
	self.dexterity = 10.
	self.intelligence = 10.

	self.health = 1.


	#add more attributes


def onUpdate(self,delta):
	import math
	from Foundation.vector import Vector
	from entity import Entity

	self.__shootdelay -= delta
	gamestate.centerOn(self)

	velocity.x = 0.
	velocity.y = 0.

	self.health += delta * 0.01
	self.health = min(1.,self.health)

	relX = cursorX - position.x 
	relY = cursorY - position.y

	
	velocity.x = relX
	velocity.y = relY
	velocity.z = 0
	
	velocity.x *= 0.001
	velocity.y *= 0.001
	velocity.z *= 0.001

	speed = 2.0
	if keys['d']:
		velocity.x += speed
	if keys['a']:
		velocity.x += -speed
	if keys['w']:
		velocity.y += speed
	if keys['s']:
		velocity.y += -speed

	self.rotateTo(math.degrees(math.atan2(velocity[1],velocity[0]))+90)
	
	armed = self.lhand != None or self.rhand != None

	if self.__shootdelay <= 0. and mouseL and armed:
		if self.rhand != None:
			self.rhand.call("onUse",self)
		else:
			self.lhand.call("onUse",self)
		self.__shootdelay = .1

	

	walk_anim = "walk"+("_armed" if armed else "")
	idle_anim = "idle"+("_armed" if armed else "")
	if mouseL and armed:
		walk_anim = "walk_shooting"
		idle_anim = "idle_shooting"
	if velocity.length > 0.1 and current_animation["name"] != walk_anim:
		self.startAnimation(walk_anim)
	elif velocity.length <= 0.1 and current_animation["name"] != idle_anim:
		self.startAnimation(idle_anim)

def onCollision(self, where):
	if str(where.__class__.__name__) == "Entity":
		if where.isCollectible():
			where.collect(self)
			self.addItem(where)

def onHit(self, damage):
	import random
	import sound
	self.health -= damage
	sound.playSound("Sounds/GettingHit"+str(random.randint(1,5))+".mp3")
	if self.health <= 0.:
		sound.playSound("Sounds/SterbenMitFX.mp3")
		self.remove()