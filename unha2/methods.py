from typing import Optional, List
from . common import uuid
from . import build
from . import parse
from . holder import AsyncHolder

async def get_users(ws, holder: AsyncHolder, room_id: str) -> dict:
    uid = uuid()
    payload = build.methods.get_users(uid, room_id)
    result = await holder.send_method(ws, uid, payload)
    return parse.result.users(result['result'])

async def load_history(ws, holder: AsyncHolder, room_id: str, last_received: str, quantity: int, oldest_wanted=None):
    uid = uuid()
    payload = build.methods.load_history(uid, room_id, last_received, quantity, oldest_wanted)
    result = await holder.send_method(ws, uid, payload)
    return parse.result.load_history(result['result'])

async def get_rooms(ws, holder: AsyncHolder, date=0) -> dict:
    uid = uuid()
    payload = build.methods.get_rooms(uid, date)
    result = await holder.send_method(ws, uid, payload)
    return parse.result.rooms(result['result'])

async def get_subscriptions(ws, holder: AsyncHolder, date=0) -> dict:
    uid = uuid()
    payload = build.methods.get_subscriptions(uid, date)
    result = await holder.send_method(ws, uid, payload)
    return parse.result.subscriptions(result['result'])

async def login_sha256(ws, holder: AsyncHolder, username: str, password: str) -> dict:
    uid = uuid()
    payload = build.methods.login_sha256(uid, username, password)
    result = await holder.send_method(ws, uid, payload)
    return parse.result.login(result['result'])

async def login_resume(ws, holder: AsyncHolder, token: str) -> dict:
    uid = uuid()
    payload = build.methods.login_resume(uid, token)
    result = await holder.send_method(ws, uid, payload)
    return parse.result.login(result['result'])

async def send_message(ws, holder: AsyncHolder, room_id: str, text: str) -> dict:
    uid = uuid()
    mid = uuid()
    payload = build.methods.send_text_message(uid, mid, room_id, text)
    result = await holder.send_method(ws, uid, payload)
    return result

async def get_room_id(ws, holder: AsyncHolder, room_name: str) -> dict:
    uid = uuid()
    payload = build.methods.get_room_id(uid, room_name)
    result = await holder.send_method(ws, uid, payload)
    return parse.result.room_id(result['result'])

async def join_room(ws, holder: AsyncHolder, room_id: str, join_code: Optional[str]=None) -> dict:
    uid = uuid()
    payload = build.methods.join_room(uid, room_id, join_code)
    result = await holder.send_method(ws, uid, payload)
    return parse.result.join_room(result)

async def open_room(ws, holder: AsyncHolder, room_id: str) -> dict:
    uid = uuid()
    payload = build.methods.open_room(uid, room_id)
    result = await holder.send_method(ws, uid, payload)
    return parse.result.open_room(result)

async def leave_room(ws, holder: AsyncHolder, room_id: str) -> dict:
    uid = uuid()
    payload = build.methods.leave_room(uid, room_id)
    result = await holder.send_method(ws, uid, payload)
    return result

async def create_channel(ws, holder: AsyncHolder, name: str, users: Optional[List[str]]=None, readonly=False) -> dict:
    uid = uuid()
    payload = build.methods.create_channel(uid, name, users, readonly)
    result = await holder.send_method(ws, uid, payload)
    return result

async def create_private_group(ws, holder: AsyncHolder, name: str, users: Optional[List[str]]=None) -> dict:
    uid = uuid()
    payload = build.methods.create_private_group(uid, name, users)
    result = await holder.send_method(ws, uid, payload)
    return result

async def set_presence(ws, holder: AsyncHolder, status: str) -> dict:
    uid = uuid()
    payload = build.methods.set_presence(uid, status)
    result = await holder.send_method(ws, uid, payload)
    return result
