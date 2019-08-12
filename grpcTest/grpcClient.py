#! /usr/bin/env python
# -*- coding: utf-8 -*-
import grpc
import time
from grpcTest import helloworld_pb2_grpc, helloworld_pb2

_HOST = '127.0.0.1'
_PORT = '50051'

def run():
    conn = grpc.insecure_channel(_HOST + ':' + _PORT)
    client = helloworld_pb2_grpc.GreeterStub(channel=conn)
    now = time.time()
    print("start time" + str(now))
    for i in range(0, 10000):
        response = client.SayHello(helloworld_pb2.HelloRequest(name='hello,world!'+str(i)))
        # print("Greeter client received: " + response.message)
    print("end time" + str(time.time() - now))
    conn.close()

if __name__ == '__main__':
    run()