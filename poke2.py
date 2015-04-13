import trollius as asyncio
from trollius import From

#import urllib.parse
import sys

@asyncio.coroutine
def print_http_headers(hostname, port, path='/'):
    #url = urllib.parse.urlsplit(url)
    connect = asyncio.open_connection(hostname, port)
    reader, writer = yield From( connect )
    query = ('HEAD {path} HTTP/1.0\r\n'
             'Host: {hostname}\r\n'
             '\r\n').format(path=path, hostname=hostname)
    writer.write(query.encode('latin-1'))
    while True:
        line = yield From(reader.readline())
        if not line:
            break
        line = line.decode('latin1').rstrip()
        if line:
            print('HTTP header> %s' % line)
                
    # Ignore the body, close the socket
    writer.close()
                
#url = sys.argv[1]
loop = asyncio.get_event_loop()
#task = asyncio.async(print_http_headers('127.0.0.1',9042))
task = asyncio.async(print_http_headers('www.yahoo.com',80))
loop.run_until_complete(task)
loop.close()

