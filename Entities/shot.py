

def onUpdate(self, delta):
	global alpha
	self.setAlpha(alpha - delta)
	if alpha < 0.01:
		self.remove()

def onCollision(self, where):
	if str(where.__class__.__name__) == "Entity":
		if self.getOwner() != where and where.getName() != "shot" and not where.isCollectible():
			where.call("onHit",0.2)
			self.remove()
	else:
		self.remove()