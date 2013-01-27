

def onInit(self):
	self.startAnimation("idle")
	self.__armed = True
	self.__shootdelay = 0.
	self.__aggressive = False
	position.x = 20
	position.y = 20
	self.health = 1.

def onSpace(self,who):
	def becomeAggressive(self):
		self.__aggressive = True
	gamestate.showText("Bla",becomeAggressive,[self])



def onUpdate(self,delta):
	import math
	from Foundation.vector import Vector
	from entity import Entity
	global velocity

	self.__shootdelay -= delta

	velocity.x = 0.
	velocity.y = 0.

	distToPlayer = (entitymanager.getFocus().getPosition() - position).length

	relX = entitymanager.getFocus().getPosition().x - position.x 
	relY = entitymanager.getFocus().getPosition().y - position.y

	if entitymanager.getFocus().health <= 0.:
		self.__aggressive = False
	
	velocity.x = relX
	velocity.y = relY
	velocity.z = 0
	
	velocity.x *= 0.001
	velocity.y *= 0.001
	velocity.z *= 0.001

	speed = 2.0
	if distToPlayer < 3.:
		speed = 0.2
	if not self.__aggressive:
		speed = 0.0
	velocity = velocity.normalized()
	velocity.x *= speed
	velocity.y *= speed

	if speed == 0.0:
		self.rotateTo(math.degrees(math.atan2(relY,relX))+90)
	else:
		self.rotateTo(math.degrees(math.atan2(velocity[1],velocity[0]))+90)
	
	self.__armed = self.__aggressive

	shooting = distToPlayer < 3. and self.__aggressive
	if self.__shootdelay <= 0. and shooting:
		shot = entitymanager.createEntity("Entities/shot.json")
		shot.setPosition(position)
		shot.setRotation(math.degrees(math.atan2(velocity.y, velocity.x)))
		shot.setVelocity(velocity.normalized()*10)
		shot.setOwner(self)

		self.__shootdelay = .5


	walk_anim = "walk"+("_armed" if self.__armed else "")
	idle_anim = "idle"+("_armed" if self.__armed else "")
	if shooting and self.__armed:
		walk_anim = "walk_shooting"
		idle_anim = "idle_shooting"
	if velocity.length > 0.1 and current_animation["name"] != walk_anim:
		self.startAnimation(walk_anim)
	elif velocity.length <= 0.1 and current_animation["name"] != idle_anim:
		self.startAnimation(idle_anim)

	self.setVelocity(velocity)

def onHit(self, damage):
	import random
	import sound
	self.health -= damage
	sound.playSound("Sounds/GettingHit"+str(random.randint(1,5))+".mp3")
	if self.health <= 0.:
		sound.playSound("Sounds/SterbenMitFX.mp3")
		self.remove()

