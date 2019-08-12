# coding: utf-8
"""
thrift_client.py
"""

import sys
import time
from thriftTest.hello import HelloService

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

try:
    transport = TSocket.TSocket('localhost', 9090)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = HelloService.Client(protocol)
    transport.open()
    now = time.time()
    print("start time"+str(now))
    for i in range(0,10000):
        msg = client.helloString("Hello china!"+str(i))
        # print("server - " + msg)
    print("end time" + str(time.time()-now))
    transport.close()

except Thrift.TException as ex:
    print("%s" % (ex.message))