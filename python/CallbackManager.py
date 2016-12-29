import heapq
import time
import traceback

class Timer(object):

	def __init__(self, t, callback, repeat):
		if repeat:
			t = max(t, 0.001)

		now = time.time()
		timeout = now + t

		self.t = t
		self.callback = callback
		self.repeat = repeat
		self.timeout = timeout
		self.cancelled = False

	def __lt__(self, other):
		return self.timeout < other.timeout

	def Cancel(self):
		self.cancelled = True

	def __nonzero__(self):
		return not self.cancelled

class CallbackManager(object):

	def __init__(self):
		self.timers = []

	def AddCallback(self, t, callback):
		timer = Timer(t, callback, False)
		heapq.heappush(self.timers, timer)

	def AddTimer(self, t, callback):
		timer = Timer(t, callback, True)
		heapq.heappush(self.timers, timer)

	def Tick(self):
		now = time.time()

		while True:
			if not self.timers: break
			minTimer = self.timers[0]
			if now < minTimer.timeout:
				return

			timer = heapq.heappop(self.timers)
			if timer.cancelled:
				continue

			if timer.repeat:
				timer.timeout = timer.timeout + timer.t

			try:
				timer.callback()
			except:
				traceback.print_exc()

			if timer.repeat:
				heapq.heappush(self.timers, timer)
