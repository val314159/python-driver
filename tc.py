from troll import *
from tornado.platform.asyncio import AsyncIOMainLoop
AsyncIOMainLoop().install()

loop = asyncio.get_event_loop()

import logging
logging.basicConfig()

from cassandra.cluster import Cluster

@asyncio.coroutine
def xx():
    print "hello"
    
@asyncio.coroutine
def amain():
    cluster = Cluster()
    asyncio.async( xx() )
    print 'ok'
    session = cluster.connect()
    pass

print 111
loop.create_task( amain() )
print 222
loop.run_forever()
print 333
