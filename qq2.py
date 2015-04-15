#!/usr/bin/python

#from tornado.platform.asyncio import AsyncIOMainLoop
#AsyncIOMainLoop().install()
 
import trollius as asyncio
from trollius import From, Return
loop = asyncio.get_event_loop()

import os,sys
 
hostname,port = '127.0.0.1',9042
 
class Conn(object):
 
    def __init__(_,host, port):
        _.host,_.port = host,port
        run = asyncio.async(_.async_run())
        pass
 
    @asyncio.coroutine
    def async_run(_):
        _.connect = asyncio.open_connection(_.host,_.port)
        reader, writer = yield From(_.connect)
        print "READ AND WRITE"
        _.reader, _.writer = reader, writer

        print "<", repr(s)
        _.writer.write(s)
        #yield From( _.drain() )

        asyncio.async( _.async_read_loop() )
        pass

    @asyncio.coroutine
    def async_read_loop(_):
        while True:
            print "READ IT 0"
            #print "READ IT 0", dir(_.reader)
            line = yield From(_.reader.read(100))
            print "LINE:", repr(line)
            if not line:
                break
            pass
        pass
    pass

asyncio.tasks._DEBUG = True
 
s = '\x02\x00\x00\x01\x00\x00\x00\x16\x00\x01\x00\x0bCQL_VERSION\x00\x053.0.0'
#conn = Conn(hostname,port)

@asyncio.coroutine
def amain():
    print "AMAIN:"
    print "XXXXX 1"
    conn = Conn(hostname,port)
    print "XXXXX 2"
    print "XXXXX 3"

asyncio.async( amain() )

print "XXXXX"
loop.run_forever()
print "YYYYY"
loop.run_forever()
print "ZZZZZ"

