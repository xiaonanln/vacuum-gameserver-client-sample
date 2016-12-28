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

def Loop():
    while True:
        asyncore.loop(0.1, use_poll=True)

def Setup(delegate):
    assert isinstance(delegate, BaseGameDelegate), delegate
    gameDelegate = delegate

def Connect(host, port):
    gameClient = GSClient.GSClient(host, port)
    gameClient.messageHandler = handleMessage

def handleMessage(msgType, msg):
    print 'handleMessage', msgType, msg
    if msgType == 2:
        handleCreateEntity(msg['K'], msg['E'])
    else:
        print 'invalid message type', msgType

def handleCreateEntity(entityKind, entityID):
    print 'handleCreateEntity', entityKind, entityID
    entityManager.CreateEntity(entityKind, entityID)
