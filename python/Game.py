# coding: utf8

import sys
import time
import asyncore
import EntityManager
import GSClient
import CallbackManager

from proto import CLIENT_CREATE_ENTITY
from proto import CLIENT_TO_SERVER_RPC
from proto import SERVER_TO_CLIENT_RPC

LOOP_INTERVAL = 0.1

class BaseGameDelegate(object):
    pass

entityManager = EntityManager.EntityManager()
callbackManager = CallbackManager.CallbackManager()
gameDelegate = BaseGameDelegate()
gameClient = None

def RegisterEntityType(kind, cls):
    entityManager.RegisterEntityType(kind, cls)

def Loop(timeout=None):
    timeout = time.time() + timeout if timeout is not None else None
    while timeout is None or time.time() < timeout:
        sys.stderr.write('.')
        asyncore.loop(0.1, use_poll=True, count=1)
        callbackManager.Tick()

def Setup(delegate):
    global gameDelegate
    assert isinstance(delegate, BaseGameDelegate), delegate
    gameDelegate = delegate

def Connect(host, port):
    global gameClient
    gameClient = GSClient.GSClient(host, port)
    gameClient.messageHandler = handleMessage

def AddCallback(t, callback):
    return callbackManager.AddCallback(t, callback)

def AddTimer(t, callback):
    return callbackManager.AddTimer(t, callback)

def handleMessage(msgType, msg):
    print 'handleMessage', msgType, msg
    if msgType == CLIENT_CREATE_ENTITY:
        handleCreateEntity(msg['K'], msg['E'])
    elif msgType == SERVER_TO_CLIENT_RPC:
        # {u'A': [True], u'M': u'OnLogin', u'E': u'WLVN_6d_YzpcAAAO'}
        handleServerToClientRPC(msg['E'], msg['M'], msg['A'])
    else:
        print 'invalid message type', msgType

def handleCreateEntity(entityKind, entityID):
    print 'handleCreateEntity', entityKind, entityID
    entityManager.CreateEntity(entityKind, entityID)

def handleServerToClientRPC(entityID, methodName, args):
    print 'handleServerToClientRPC', entityID, methodName, args


def sendRPC(entityID, method, args):
    msg = {
        'E': entityID,
        'M': method,
        'A': args,
    }
    gameClient.SendMsg(CLIENT_TO_SERVER_RPC, msg)
