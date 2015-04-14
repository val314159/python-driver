
from cassandra import OperationTimedOut
from cassandra.connection import Connection, ConnectionShutdown
from cassandra.protocol import RegisterMessage

class AsyncIOConnection(Connection):
    @classmethod
    def factory(cls, *args, **kwargs):
        print "TFACTOR", (args,kwargs)
        timeout = kwargs.pop('timeout', 5.0)
        conn = cls(*args, **kwargs)
        return conn
    def __init__(self, *args, **kwargs):
        print "TINIT", (args,kwargs)
        Connection.__init__(self, *args, **kwargs)
        pass

