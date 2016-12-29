# encoding: utf8

import asyncore
import socket
import sys
import struct
import json

LENGTH_FIELD_SIZE = 4
MESSAGE_TYPE_FIELD_SIZE = 2

class RecvState_ReceiveLength(object):
	def __init__(self):
		self.left = LENGTH_FIELD_SIZE
		self.data = ''

	def recv(self, gsclient):
		data = gsclient.recv(self.left)
		self.left -= len(data)
		self.data += data
		if self.left <= 0:
			gsclient.packetLength = struct.unpack("<I", self.data)[0]
			print 'read packet length', gsclient.packetLength
			return RecvState_ReceiveMessageType()
		else:
			return self

class RecvState_ReceiveMessageType(object):
	def __init__(self):
		self.left = MESSAGE_TYPE_FIELD_SIZE
		self.data = ''

	def recv(self, gsclient):
		data = gsclient.recv(self.left)
		self.left -= len(data)
		self.data += data
		if self.left <= 0:
			gsclient.messageType = struct.unpack("<H", self.data)[0]
			print 'read message type', gsclient.messageType
			payloadSize = gsclient.packetLength - LENGTH_FIELD_SIZE - MESSAGE_TYPE_FIELD_SIZE
			return RecvState_ReceivePayload(payloadSize)
		else:
			return self

class RecvState_ReceivePayload(object):
	def __init__(self, payloadSize):
		self.left = payloadSize
		self.data = ''

	def recv(self, gsclient):
		data = gsclient.recv(self.left)
		self.left -= len(data)
		self.data += data
		if self.left <= 0:
			msg = json.loads(self.data, encoding='UTF-8')
			print 'received message', msg
			gsclient.onMessageReceived(gsclient.messageType, msg)
			return RecvState_ReceiveLength()
		else:
			return self

class GSClient(asyncore.dispatcher_with_send):

	BUFFER_SIZE = 4096

	def __init__(self, host, port):
		asyncore.dispatcher_with_send.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect((host, port))
		self.packetLength = None
		self.recvState = RecvState_ReceiveLength()
		self.messageHandler = None

	def handle_read(self):
		print 'readable'
		self.recvState = self.recvState.recv(self)

	def onMessageReceived(self, msgType, msg):
		self.messageHandler(msgType, msg)

	def handle_error(self):
		self.close()
		import traceback
		traceback.print_exc()
		# asyncore.dispatcher_with_send.handle_error(self)

	def SendMsg(self, msgType, msg):
		print 'SendMsg', msgType, msg
		payload = json.dumps(msg, separators=',:')
		packetLength = len(payload) + LENGTH_FIELD_SIZE + MESSAGE_TYPE_FIELD_SIZE

		header = struct.pack('<IH', packetLength, msgType)
		self.send(header + payload)
