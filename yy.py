#!/usr/bin/python                                                                                                                                                                               
 
import os,sys,socket
 
hostname,port = '127.0.0.1',9042
 
sockerr = None
addresses = socket.getaddrinfo(hostname, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
for (af, socktype, proto, canonname, sockaddr) in addresses:
    try:
        _socket = socket.socket(af, socktype, proto)
        _socket.settimeout(1.0)
        _socket.connect(sockaddr)
        sockerr = None
        break
    except socket.error as err:
        sockerr = err
        pass
    pass
if sockerr:
    raise socket.error(sockerr.errno, "Tried connecting to %s. Last error: %s" % ([a[4] for a in addresses], sockerr.strerror))
 
s = '\x02\x00\x00\x01\x00\x00\x00\x16\x00\x01\x00\x0bCQL_VERSION\x00\x053.0.0'

print '<', repr(s)
#print _socket
_socket.sendall(s)
#print dir(_socket)
x = _socket.recv(100)
print '>', repr(x)


