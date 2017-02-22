from . import build
from . common import uuid

async def room_messages(ws, holder, room_id):
    """Subscribe to room messages"""
    uid = uuid()
    payload = build.subs.sub_room_messages(uid, room_id)
    result = await holder.send_sub(ws, uid, payload)
    return result
