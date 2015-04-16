
# this module is meant to be imported as a *
# so keep the import SIMPLE

import trollius as asyncio
from trollius import From, Return
loop = asyncio.get_event_loop()
def Loop(): return asyncio.get_event_loop()

import logging
logging.basicConfig()

###########
class AioLock(object):
    @asyncio.coroutine
    def acquire  (_,blocking=1): print "acquire", blocking
    def release  (_):            print "release"
    def __enter__(_):            print "__enter__"
    def __exit__ (_,t,v,tb):     print "__exit__",t,v,tb
    pass

class AioRLock(object):
    @asyncio.coroutine
    def acquire  (_,blocking=1): print "Racquire", blocking
    def release  (_):            print "Rrelease"
    def __enter__(_):            print "__Renter__"
    def __exit__ (_,t,v,tb):     print "__Rexit__",t,v,tb
    pass

@asyncio.coroutine
def aio_sleep(x):
    print "MY SLEEP"
    import time
    return time.old_sleep(x)

class obj(object): pass

_current = obj()
_current.name = 'NONE'

def get_current(): return _current

class AioThread(object):
    def __init__(_, target, name):
        print "THREAD OFF", target, name
        _.target, _.name = target, name
        _.running = None
        pass
    def start(_):
        _.running = loop.call_soon( _.target )
        print "### _.running:", _.running
        _.current = _
        pass
    @asyncio.coroutine
    def join(_):
        print "JOIN"
        pass
    def is_alive(_):
        return True
    pass

class AioEvent(object):
    def __init__(_): _.state = False
    def set(_): _.state = True
    def is_set(_): return _.state
    @asyncio.coroutine
    def wait(_, timeout=None):
        while 1:
            print "WAIT"
            import time
            time.sleep(1)
            pass
        pass
    pass

def aio_monkey_patch():
    print "monkey patch it------0",'.'*80
    import threading,time
    '''
    threading.OldLock = threading.Lock
    threading.Lock   = AioLock
    threading.RLock  = threading.RLock
    threading.RLock  = AioRLock
    '''
    threading.currentThread = get_current
    threading.current_thread = get_current
    threading.Thread = threading.Thread
    threading.Thread = AioThread
    threading.Event  = threading.Event
    threading.Event  = AioEvent    
    time.old_sleep = time.sleep
    time.sleep = aio_sleep
    print "monkey patch it------9",'.'*80
    pass
