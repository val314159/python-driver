
# this module is meant to be imported as a *
# so keep the import SIMPLE

import trollius as asyncio
from trollius import From, Return
loop = asyncio.get_event_loop()
def Loop(): return asyncio.get_event_loop()

import logging
logging.basicConfig()
