import asyncio
from asyncio import Queue

import unha2.build as build
import unha2.model as model
import unha2.parse as parse
import unha2.methods as methods
import unha2.subscriptions as subscriptions
import unha2.transport.websocket as sock
from unha2.model.base import RawMessageType, ChangedStreamMessage, RoomMessage
from unha2.holder import AsyncHolder

class Client:
    """
    Simple client which connects to a server and logs in.
    """
    def __init__(self, server, username, password):
        self.holder = AsyncHolder()
        self.server =server
        self.username = username
        self.password = password
        self.queue = Queue()
        self.stop = False
        self.ws = None
        self.session = ''
        self.token = ''
        self.user_id = ''
        self.expires = None

    async def handler_loop(self):
        while not self.stop:
            msg = await self.queue.get()
            type_ = parse.base.msg_type(msg)
            if type_ == RawMessageType.NONE:
                self._connect()
            elif type_ == RawMessageType.PING:
                self._send_pong()
            elif type_ == RawMessageType.CONNECTED:
                self.session = parse.connected.parse(msg)['session']
                asyncio.ensure_future(self.login())
            elif type_ == RawMessageType.RESULT:
                self.holder.recv_result(msg)
            elif type_ == RawMessageType.READY:
                self.holder.recv_ready(msg)
            elif type_ == RawMessageType.ADDED:
                pass
            elif type_ == RawMessageType.CHANGED:
                self.on_changed(msg)
            elif type_ == RawMessageType.UPDATED:
                pass
            elif type_ == RawMessageType.REMOVED:
                pass
            elif type_ == RawMessageType.FAILED:
                pass

    def on_changed(self, msg):
        msg_type = ChangedStreamMessage(msg['collection'])
        if msg_type == ChangedStreamMessage.USERS:
            self.on_users(msg)
        elif msg_type == ChangedStreamMessage.NOTIFY_USER:
            self.on_notify_user(msg)
        elif msg_type == ChangedStreamMessage.NOTIFY_ROOM:
            self.on_notify_room(msg)
        elif msg_type == ChangedStreamMessage.ROOM_MESSAGES:
            self.on_room_message(parse.changed.room_message(msg))

    def on_users(self, msg):
        pass

    def on_notify_user(self, msg):
        pass

    def on_notify_room(self, msg):
        pass

    def on_room_message(self, msg):
        room_dispatch = {
            RoomMessage.USER_JOINED: self.on_user_joined,
            RoomMessage.USER_LEFT: self.on_user_left,
            RoomMessage.USER_ADDED: self.on_user_added,
            RoomMessage.USER_REMOVED: self.on_user_removed,
            RoomMessage.USER_MUTED: self.on_user_muted,
            RoomMessage.USER_UNMUTED: self.on_user_unmuted,
            RoomMessage.ROLE_ADDED: self.on_role_added,
            RoomMessage.ROLE_REMOVED: self.on_role_removed,
            RoomMessage.TOPIC_CHANGED: self.on_topic_changed,
            RoomMessage.NORMAL_MESSAGE: self.on_normal_message,
            RoomMessage.REMOVE: lambda x: None
        }
        return room_dispatch[msg['type']](msg)

    def on_user_joined(self, msg):
        pass

    def on_user_left(self, msg):
        pass

    def on_user_added(self, msg):
        pass

    def on_user_removed(self, msg):
        pass

    def on_user_muted(self, msg):
        pass

    def on_user_unmuted(self, msg):
        pass

    def on_role_added(self, msg):
        pass

    def on_role_removed(self, msg):
        pass

    def on_normal_message(self, msg):
        pass

    def on_topic_changed(self, msg):
        pass

    def _connect(self):
        sock.send(self.ws, build.misc.connect())

    def _send_pong(self):
        sock.send(self.ws, build.misc.pong())

    def send_msg(self, room_id, text):
        asyncio.ensure_future(methods.send_message(
            self.ws,
            self.holder,
            room_id,
            text
        ))

    async def login(self):
        res = await methods.login_sha256(
            self.ws,
            self.holder,
            self.username,
            self.password
        )
        self.token = res['token']
        self.expires = res['expires']
        self.user_id = res['user_id']
        return res

    async def get_rooms(self):
        return await methods.get_rooms(self.ws, self.holder, 0)

    async def get_room_id(self, room_name):
        return await methods.get_room_id(self.ws, self.holder, room_name)

    async def load_history(self, room_id, last_received, number, oldest_wanted=None):
        return await methods.load_history(self.ws, self.holder, room_id, last_received, number, oldest_wanted)

    async def get_subscriptions(self):
        return await methods.get_subscriptions(self.ws, self.holder)

    def subscribe_user_all(self):
        for i in build.subs.ALLOWED_USER_SUBS:
            asyncio.ensure_future(subscriptions.notify_user(
                self.ws,
                self.holder,
                self.user_id,
                i
            ))

    def subscribe_to_room(self, room):
        room_id = room['room_id']
        asyncio.ensure_future(subscriptions.room_messages(
            self.ws,
            self.holder,
            room_id
        ))
        asyncio.ensure_future(subscriptions.notify_room(
            self.ws,
            self.holder,
            room_id,
            'typing'
        ))

    def subscribe_to_rooms(self, room_list):
        for room in room_list:
            self.subscribe_to_room(room)

    async def network_loop(self, loop):
        async with sock.session(loop) as session:
            async with sock.connect(session, self.server) as ws:
                self.ws = ws
                async for msg in sock.ws_loop(ws):
                    self.queue.put_nowait(msg)
