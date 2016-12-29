
import Game
import sys
from GSEntity import GSEntity

print 'test_sample'

class Account(GSEntity):
	def __init__(self, *args):
		super(Account, self).__init__(*args)
		print 'Account', self.id
		Game.AddCallback(1, lambda: self.startLogin())

	def startLogin(self):
		print 'startLogin'
		self.CallServer('Login', "xixi", "123456")

class Avatar(GSEntity):
	def __init__(self, *args):
		super(Avatar, self).__init__(*args)
		print 'Avatar', self.id

Game.RegisterEntityType(0, Account)
Game.RegisterEntityType(1, Avatar)

Game.Connect("localhost", 4000)
Game.Loop(timeout=3)
