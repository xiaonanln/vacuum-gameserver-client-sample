# coding: utf8

import threading
import asyncore
import EntityManager
import GSClient

LOOP_INTERVAL = 0.1

class BaseGameDelegate(object):
    pass

entityManager = EntityManager.EntityManager()
gameDelegate = BaseGameDelegate()
gameClient = None

def tickingRoutine():
    while True:
        print 'loop ...'
        asyncore.loop(0.1, use_poll=True)

tickingThread = threading.Thread(target=tickingRoutine)

def Setup(delegate):
    assert isinstance(delegate, BaseGameDelegate), delegate
    gameDelegate = delegate
    tickingThread.setDaemon(True)
    tickingThread.start()

def Connect(host, port):
    gameClient = GSClient.GSClient(host, port)







