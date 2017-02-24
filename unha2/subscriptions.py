from . import build
from . common import uuid
from . holder import AsyncHolder

async def room_messages(ws, holder: AsyncHolder, room_id: str):
    """Subscribe to room messages"""
    uid = uuid()
    payload = build.subs.sub_room_messages(uid, room_id)
    return await holder.send_sub(ws, uid, payload)

async def notify_room(ws, holder: AsyncHolder, room_id: str, sub: str):
    uid = uuid()
    payload = build.subs.sub_notify_room(uid, room_id, sub)
    return await holder.send_sub(ws, uid, payload)

async def notify_user(ws, holder: AsyncHolder, user_id: str, sub: str):
    uid = uuid()
    payload = build.subs.sub_notify_user(uid, user_id, sub)
    return await holder.send_sub(ws, uid, payload)
