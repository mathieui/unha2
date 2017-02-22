import asyncio
from . common import uuid
from . import build
from . import parse
from . transport import websocket as sock

class MethodHolder:
    def __init__(self):
        self.awaited_methods = {} # uid → Future

    async def send_method(self, ws, uid, msg):
        fut = asyncio.Future()
        self.awaited_methods[uid] = fut
        sock.send(ws, msg)
        return await fut

    def send_method_noblock(self, ws, uid, msg, callback=None):
        if callback:
            fut = asyncio.Future()
            fut.add_done_callback(callback)
            self.awaited[uid] = fut
        sock.send(ws, msg)

    def recv(self, result):
        uid = result['id']
        awaited = self.awaited_methods.get(uid)
        if awaited:
            awaited.set_result(result)
            del self.awaited_methods[uid]

async def get_users(ws, holder, room_id):
    uid = uuid()
    payload = build.methods.get_users(uid, room_id)
    result = await holder.send_method(ws, uid, payload)
    total = result['result']['total']
    online = result['result']['records']
    return parse.result.parse_users(result['result'])

async def get_rooms(ws, holder, date=0):
    uid = uuid()
    payload = build.methods.get_rooms(uid, date)
    result = await holder.send_method(ws, uid, payload)
    return parse.result.parse_rooms(result['result'])

async def get_subscriptions(ws, holder, date=0):
    uid = uuid()
    payload = build.methods.get_subscriptions(uid, date)
    result = await holder.send_method(ws, uid, payload)
    return parse.result.parse_subscriptions(result['result'])

async def login_sha256(ws, holder, username, password):
    uid = uuid()
    payload = build.methods.login_sha256(uid, username, password)
    result = await holder.send_method(ws, uid, payload)
    return parse.result.parse_login(result['result'])

async def send_message(ws, holder, room_id, text):
    uid = uuid()
    mid = uuid()
    payload = build.methods.send_text_message(uid, mid, room_id, text)
    result = await holder.send_method(ws, uid, payload)
    return result

