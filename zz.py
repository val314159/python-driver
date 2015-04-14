#!/usr/bin/python                                                                                                                                                                               
from tornado.platform.asyncio import AsyncIOMainLoop
AsyncIOMainLoop().install()
 
import trollius as asyncio
from trollius import From, Return
loop = asyncio.get_event_loop()
 
import os,sys
 
#from cassandra.cluster import Cluster                                                                                                                                                          
 
hostname,port = '127.0.0.1',9042
#hostname,port = '127.0.0.1',8888
 
class Conn(object):
 
    _loop = None
 
    @classmethod
    def set_loop(cls, loop):
        cls._loop = loop
        pass
 
    def __init__(_,host, port, loop):
        _.host,_.port = host,port
        run = asyncio.async(_.async_run())
        if loop:
            _.set_loop(loop)
            _._loop.run_until_complete( run )
            pass
        pass
 
    @asyncio.coroutine
    def async_run(_):
        _.connect = asyncio.open_connection(_.host,_.port)
        reader, writer = yield From(_.connect)
        print "READ AND WRITE"
        _.reader, _.writer = reader, writer

        _.writer.write(s)

        asyncio.async( _.async_read_loop() )
        pass
 
    @asyncio.coroutine
    def async_read_loop(_):
        while True:
            print "READ IT 0"
            line = yield From(_.reader.readline())
            print "LINE", repr(line)
            if not line:
                break
            pass
        pass
    pass

asyncio.tasks._DEBUG = True
 
s = '\x02\x00\x00\x01\x00\x00\x00\x16\x00\x01\x00\x0bCQL_VERSION\x00\x053.0.0'
conn = Conn(hostname,port,loop)
print "XXXXX"
print "S", repr(s)
print "YYYYY"
loop.run_forever()

