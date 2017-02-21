import json
import logging
import random

import aiohttp

from .. common import dumbs, undumbs

log = logging.getLogger(__name__)

def send(ws, payload):
    log.debug('SEND %s', payload)
    ws.send_str(dumbs(payload))

def _empty(msg):
    pass

def _empty_close(msg):
    raise StopAsyncIteration

async def ws_loop(ws, handler, o_handler=_empty, h_handler=_empty,
                       c_handler=_empty_close):
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            char = msg.data[0]
            content = msg.data[1:]
            if char == 'o':
                o_handler(content)
            elif char == 'h':
                h_handler(content)
            elif char == 'o':
                _empty_close(content)
            elif char == 'a':
                handler(undumbs(content))
            else:
                log.warning('Unknown sockjs frame command: "%s"', char)
        elif msg.type == aiohttp.WSMsgType.CLOSED:
            break
        elif msg.type == aiohttp.WSMsgType.ERROR:
            break

async def asyncio_loop(loop, host, handler, **handlers):
    o_handler = handlers.get('o_handler', _empty)
    h_handler = handlers.get('h_handler', _empty)
    c_handler = handlers.get('c_handler', _empty_close)
    async with aiohttp.ClientSession(loop=loop) as session:
        sockjs_id = random.randint(100, 999)
        client_id = random.randint(1, 100)
        url = 'https://%s/sockjs/%s/unha2%s/websocket' % (host, sockjs_id, client_id)
        async with session.ws_connect(url) as ws:
            await ws_loop(ws, handler, o_handler=o_handler,
                          h_handler=h_handler,
                          c_handler=c_handler)
