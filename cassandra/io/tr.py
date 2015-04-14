#!/usr/bin/python
import gevent
from gevent import select, socket, ssl
from gevent.event import Event
from gevent.queue import Queue

from collections import defaultdict
from functools import partial
import logging
import os

from six.moves import xrange

from errno import EALREADY, EINPROGRESS, EWOULDBLOCK, EINVAL

from cassandra import OperationTimedOut
from cassandra.connection import Connection, ConnectionShutdown
from cassandra.protocol import RegisterMessage

#use_tornado=True
#if use_tornado:
#from tornado.platform.asyncio import AsyncIOMainLoop
#AsyncIOMainLoop().install()
#pass

import trollius as asyncio
from trollius import From, Return
loop = asyncio.get_event_loop()

log = logging.getLogger(__name__)

def is_timeout(err):
    return (
        err in (EINPROGRESS, EALREADY, EWOULDBLOCK) or
        (err == EINVAL and os.name in ('nt', 'ce'))
    )


class AsyncIOConnection(Connection):
    """
    An implementation of :class:`.Connection` that utilizes ``asyncio``.
    """

    _total_reqd_bytes = 0
    _read_watcher = None
    _write_watcher = None
    _socket = None

    @classmethod
    def factory(cls, *args, **kwargs):
        print "TFACTOR", (args,kwargs)
        timeout = kwargs.pop('timeout', 5.0)
        conn = cls(*args, **kwargs)
        '''
        conn.connected_event.wait(timeout)
        if conn.last_error:
            raise conn.last_error
        elif not conn.connected_event.is_set():
            conn.close()
            raise OperationTimedOut("Timed out creating connection")
        else:
            return conn
            '''
        return conn



    @asyncio.coroutine
    def async_run(_):
        _.connect = asyncio.open_connection(_.host,_.port)
        reader, writer = yield From(_.connect)
        print "READ AND WRITE"
        _.reader, _.writer = reader, writer

        print "<", repr(s)
        _.writer.write(s)
        print "WAIT TO DRAIN"
        yield From (_.writer.drain() )
        print "DRAINED IT"

        #asyncio.async( _.async_read_loop() )
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



    def __init__(self, *args, **kwargs):
        print "TINIT", (args,kwargs)
        Connection.__init__(self, *args, **kwargs)

        self.connected_event = Event()
        self._write_queue = Queue()

        self._callbacks = {}
        self._push_watchers = defaultdict(set)

        sockerr = None
        addresses = socket.getaddrinfo(self.host, self.port, socket.AF_UNSPEC, socket.SOCK_STREAM)
        for (af, socktype, proto, canonname, sockaddr) in addresses:
            try:
                self._socket = socket.socket(af, socktype, proto)
                if self.ssl_options:
                    self._socket = ssl.wrap_socket(self._socket, **self.ssl_options)
                self._socket.settimeout(1.0)
                self._socket.connect(sockaddr)
                sockerr = None
                break
            except socket.error as err:
                sockerr = err
        if sockerr:
            raise socket.error(sockerr.errno, "Tried connecting to %s. Last error: %s" % ([a[4] for a in addresses], sockerr.strerror))

        if self.sockopts:
            for args in self.sockopts:
                self._socket.setsockopt(*args)



        run = asyncio.async(_.async_run())
        loop.run_until_complete( run )
        asyncio.async( _.async_read_loop() )



        self._read_watcher = gevent.spawn(self.handle_read)
        self._write_watcher = gevent.spawn(self.handle_write)
        self._send_options_message()

    def close(self):
        print "TCLOSE"
        with self.lock:
            if self.is_closed:
                return
            self.is_closed = True

        log.debug("Closing connection (%s) to %s" % (id(self), self.host))
        if self._read_watcher:
            self._read_watcher.kill(block=False)
        if self._write_watcher:
            self._write_watcher.kill(block=False)
        if self._socket:
            self._socket.close()
        log.debug("Closed socket to %s" % (self.host,))

        if not self.is_defunct:
            self.error_all_callbacks(
                ConnectionShutdown("Connection to %s was closed" % self.host))
            # don't leave in-progress operations hanging
            self.connected_event.set()

    def handle_close(self):
        print "TH_CLOSE"
        log.debug("connection closed by server")
        self.close()

    def handle_write(self):
        print "TH_WRITE"
        run_select = partial(select.select, (), (self._socket,), ())
        while True:
            try:
                next_msg = self._write_queue.get()
                run_select()
                print "GOT WRITE"
            except Exception as exc:
                if not self.is_closed:
                    log.debug("Exception during write select() for %s: %s", self, exc)
                    self.defunct(exc)
                return

            try:
                print "NEXT MSG", repr(next_msg)
                self._socket.sendall(next_msg)
            except socket.error as err:
                log.debug("Exception during socket sendall for %s: %s", self, err)
                self.defunct(err)
                return  # Leave the write loop

    def handle_read(self):
        print "TH_READ"
        run_select = partial(select.select, (self._socket,), (), ())
        while True:
            try:
                run_select()
                print "GOT READ"
            except Exception as exc:
                if not self.is_closed:
                    log.debug("Exception during read select() for %s: %s", self, exc)
                    self.defunct(exc)
                return

            try:
                while True:
                    buf = self._socket.recv(self.in_buffer_size)
                    print("READ", len(buf), "BYTES")
                    if len(buf) < 10:
                        print(repr(buf))
                    self._iobuf.write(buf)
                    if len(buf) < self.in_buffer_size:
                        break
            except socket.error as err:
                if not is_timeout(err):
                    log.debug("Exception during socket recv for %s: %s", self, err)
                    self.defunct(err)
                    return  # leave the read loop

            if self._iobuf.tell():
                self.process_io_buffer()
            else:
                log.debug("Connection %s closed by server", self)
                self.close()
                return

    def push(self, data):
        print "TPUSH", repr(data)
        chunk_size = self.out_buffer_size
        for i in xrange(0, len(data), chunk_size):
            self._write_queue.put(data[i:i + chunk_size])

    def register_watcher(self, event_type, callback, register_timeout=None):
        print "T_RW"
        self._push_watchers[event_type].add(callback)
        self.wait_for_response(
            RegisterMessage(event_list=[event_type]),
            timeout=register_timeout)

    def register_watchers(self, type_callback_dict, register_timeout=None):
        print "T_RW2"
        for event_type, callback in type_callback_dict.items():
            self._push_watchers[event_type].add(callback)
        self.wait_for_response(
            RegisterMessage(event_list=type_callback_dict.keys()),
            timeout=register_timeout)
