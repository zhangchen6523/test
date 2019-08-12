# coding: utf-8
"""
thrift_client.py
"""
import socket
import sys
from thriftTest.hello import HelloService
from thriftTest.hello.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer


class HelloServiceHandler:
    def helloString(self, msg):
        ret = "python thriftTest say: " + msg
        # print(ret)
        return ret


handler = HelloServiceHandler()
processor = HelloService.Processor(handler)
transport = TSocket.TServerSocket("localhost", 9090)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

print("Starting thrift server in python...")
server.serve()
print("done!")