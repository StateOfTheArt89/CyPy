def onUse(self,user):
	import math
	shot = entitymanager.createEntity("Entities/shot.json")
	shot.setPosition(user.getPosition())
	shot.setRotation(math.degrees(math.atan2(user.getVelocity().y, user.getVelocity().x)))
	shot.setVelocity(user.getVelocity().normalized()*10)
	shot.setOwner(user)


