
class GSEntity(object):

	def __init__(self, kind, id):
		self.kind = kind
		self.id = id

	def CallServer(self, method, *args):
		import Game
		Game.sendRPC(self.id, method, args)

class _ServerProxy(object):
	pass
