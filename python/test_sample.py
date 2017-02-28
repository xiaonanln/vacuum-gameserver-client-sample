
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

	def OnLogin(self, ok):
		print '%s.OnLogin ok=%s' % (self, ok)

class Avatar(GSEntity):
	def __init__(self, *args):
		super(Avatar, self).__init__(*args)
		print 'Avatar', self.id

Game.RegisterEntityType("Account", Account)
Game.RegisterEntityType("Avatar", Avatar)

Game.Connect("localhost", 4000)
Game.Loop(timeout=3)
