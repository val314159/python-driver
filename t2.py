#import gevent.monkey;gevent.monkey.patch_all()

#from tornado.platform.asyncio import AsyncIOMainLoop
#AsyncIOMainLoop().install()

from cassandra.cluster import Cluster

cluster = Cluster()
session = cluster.connect('ks')

print 'ok'

print dir(session)
#session.set_keyspace('ks')

def dump_db():
    x = session.execute('select * from things')
    print 0,'-'*40
    for z in x:
        print 'X1', x
        pass
    print 9,'-'*40
    pass

dump_db()

session.execute('''insert into things (uuid,timestamp,name) values ('1',2,'4');''')

dump_db()

session.execute('''delete from things where uuid='1';''')
#session.execute('''truncate things''')

dump_db()
