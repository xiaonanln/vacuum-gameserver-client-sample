
class EntityManager(object):

	def __init__(self):
		self.registeredEntityTypes = {}
		self.entities = {}

	def CreateEntity(self, kind, id):
		print 'CreateEntity', kind, id

		if kind not in self.registeredEntityTypes:
			raise Exception("Entity kind %s is not registered" % kind)

		if id in self.entities:
			raise Exception("Entity %s already exists: %s", id, self.entities[id])

		cls = self.registeredEntityTypes[kind]
		entity = cls(kind, id)
		self.entities[id] = entity

	def RegisterEntityType(self, kind, cls):
		assert kind not in self.registeredEntityTypes, kind
		from GSEntity import GSEntity
		assert issubclass(cls, GSEntity), cls
		self.registeredEntityTypes[kind] = cls
