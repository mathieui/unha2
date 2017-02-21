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

async def ws_loop(ws,):
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            char = msg.data[0]
            content = msg.data[1:]
            if char == 'o':
                pass
            elif char == 'h':
                pass
            elif char == 'c':
                log.info('Received "c" from server, closing connection…')
                break
            elif char == 'a':
                jso = undumbs(content)
                log.debug('RECV %s', jso)
                yield jso
            else:
                log.warning('Unknown sockjs frame command: "%s"', char)
        elif msg.type == aiohttp.WSMsgType.CLOSED:
            log.info('Websocket connection closed')
            break
        elif msg.type == aiohttp.WSMsgType.ERROR:
            log.info('Websocket connection error: closing')
            break

async def ws_callback_loop(ws, handler, **handlers):
    o_handler = handlers.get('o_handler', _empty)
    h_handler = handlers.get('h_handler', _empty)
    c_handler = handlers.get('c_handler', _empty_close)
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            char = msg.data[0]
            content = msg.data[1:]
            if char == 'o':
                o_handler(content)
            elif char == 'h':
                h_handler(content)
            elif char == 'c':
                _empty_close(content)
            elif char == 'a':
                handler(undumbs(content))
            else:
                log.warning('Unknown sockjs frame command: "%s"', char)
        elif msg.type == aiohttp.WSMsgType.CLOSED:
            break
        elif msg.type == aiohttp.WSMsgType.ERROR:
            break

def get_url(host):
    sockjs_id = random.randint(100, 999)
    client_id = random.randint(1, 100)
    return 'https://%s/sockjs/%s/unha2%s/websocket' % (host, sockjs_id, client_id)

def session(loop):
    return aiohttp.ClientSession(loop=loop)

def connect(session, host):
    return session.ws_connect(get_url(host))
