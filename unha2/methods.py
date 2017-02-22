import asyncio
from . common import uuid
from . import build
from . import parse
from . transport import websocket as sock

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

