import asyncio
import datetime
from asyncio import Queue
from collections import defaultdict
from typing import Optional, Callable

import unha2.build as build
import unha2.parse as parse
import unha2.methods as methods
import unha2.subscriptions as subscriptions
import unha2.transport.websocket as sock
from unha2.model.base import RawMessageType, ChangedStreamMessage, RoomMessage
from unha2.holder import AsyncHolder


class ClientData:
    __slots__ = ['server', 'username', 'password', 'token', 'session',
                 'user_id', 'token_expires']
    def __init__(self, server: str, username: str, password: str):
        self.server: str = server
        self.username: str = username
        self.password: str = password
        self.token: str = ''
        self.session: str = ''
        self.user_id: str = ''
        self.token_expires: Optional[datetime.datetime] = None

    def credentials(self):
        return (self.username, self.password)

class ClientAPI:

    def __init__(self, data: ClientData, ws, holder: AsyncHolder):
        self._data: ClientData = data
        self._ws = ws
        self._holder: AsyncHolder = holder

    def connect(self):
        sock.send(self._ws(), build.misc.connect())

    def send_pong(self):
        sock.send(self._ws(), build.misc.pong())

    def send_msg(self, room_id: str, text: str):
        asyncio.ensure_future(methods.send_message(
            self._ws(),
            self._holder,
            room_id,
            text
        ))

    async def login(self):
        username, password = self._data.credentials()
        res = await methods.login_sha256(
            self._ws(),
            self._holder,
            username,
            password,
        )
        self._data.token = res['token']
        self._data.token_expires = res['expires']
        self._data.user_id = res['user_id']
        return res

    async def join_room(self, room_id, join_code=None):
        return await methods.join_room(self._ws(), self._holder, room_id, join_code=join_code)

    async def open_room(self, room_id):
        return await methods.open_room(self._ws(), self._holder, room_id)

    async def leave_room(self, room_id):
        return await methods.leave_room(self._ws(), self._holder, room_id)

    async def get_rooms(self):
        return await methods.get_rooms(self._ws(), self._holder, 0)

    async def get_room_id(self, room_name):
        return await methods.get_room_id(self._ws(), self._holder, room_name)

    async def load_history(self, room_id, last_received, number, oldest_wanted=None):
        return await methods.load_history(self._ws(), self._holder, room_id, last_received, number, oldest_wanted)

    async def get_subscriptions(self):
        return await methods.get_subscriptions(self._ws(), self._holder)

    def subscribe_user_all(self):
        for i in build.subs.ALLOWED_USER_SUBS:
            asyncio.ensure_future(subscriptions.notify_user(
                self._ws(),
                self._holder,
                self._data.user_id,
                i
            ))

    def subscribe_to_room(self, room):
        room_id = room['room_id']
        asyncio.ensure_future(subscriptions.room_messages(
            self._ws(),
            self._holder,
            room_id
        ))
        asyncio.ensure_future(subscriptions.notify_room(
            self._ws(),
            self._holder,
            room_id,
            'typing'
        ))

    def subscribe_to_rooms(self, room_list):
        for room in room_list:
            self.subscribe_to_room(room)

class Client:
    def __init__(self, server, username, password):
        self.data = ClientData(server, username, password)
        self._holder = AsyncHolder()
        self.api = ClientAPI(self.data, self.ws, self._holder)
        self._queue = Queue()
        self.stop = False
        self._ws = None

    def ws(self):
        return self._ws

    async def network_loop(self, loop):
        async with sock.session(loop) as session:
            async with sock.connect(session, self.data.server) as ws:
                self._ws = ws
                async for msg in sock.ws_loop(ws):
                    self._queue.put_nowait(msg)

    async def handler_loop(self):
        while not self.stop:
            msg = await self._queue.get()
            msgtype = parse.base.msg_type(msg)
            if msgtype == RawMessageType.NONE:
                self.do_connect()
            elif msgtype == RawMessageType.PING:
                self.api.send_pong()
            elif msgtype == RawMessageType.CONNECTED:
                self.session = parse.connected.parse(msg)['session']
                asyncio.ensure_future(self.do_login())
            elif msgtype == RawMessageType.RESULT:
                self._holder.recv_result(msg)
            elif msgtype == RawMessageType.READY:
                self._holder.recv_ready(msg)
            else:
                asyncio.ensure_future(self.parse(msg, msgtype))

    async def parse(self, msg, msgtype):
        raise NotImplementedError

    async def do_login(self):
        await self.api.login()

    def do_connect(self):
        self.api.connect()


class EventClient(Client):
    def __init__(self, server, username, password):
        Client.__init__(self, server, username, password)
        self.callbacks = defaultdict(list)
        self.callbacks.update({
            'added': [self.added],
            'failed': [self.failed],
            'changed': [self.changed],
            'updated': [self.updated],
            'removed': [self.removed],
        })

    async def do_login(self):
        result = await self.api.login()
        self.event('logged_in', result)

    def do_connect(self):
        self.event('connection_established')
        self.api.connect()

    def event(self, name: str, data=None):
        for cb in self.callbacks[name]:
            if asyncio.iscoroutinefunction(cb):
                asyncio.ensure_future(cb(data))
            else:
                # we could process it right now but call_soon allows
                # processing to be done in-order (since ensure_future)
                # will call_soon internally as well
                asyncio.get_event_loop().call_soon(lambda: cb(data))

    def add_cb(self, name, cb):
        self.callbacks[name].append(cb)

    def del_cb(self, name: str, cb):
        try:
            self.callbacks[name].remove(cb)
            return True
        except ValueError:
            return False

    async def parse(self, msg: dict, msgtype: RawMessageType):
        if msgtype == RawMessageType.ADDED:
            self.event('added', msg)
        elif msgtype == RawMessageType.CHANGED:
            self.event('changed', msg)
        elif msgtype == RawMessageType.UPDATED:
            self.event('updated', msg)
        elif msgtype == RawMessageType.REMOVED:
            self.event('removed', msg)
        elif msgtype == RawMessageType.FAILED:
            self.event('failed', msg)

    def added(self, msg): pass
    def removed(self, msg): pass
    def updated(self, msg): pass
    def failed(self, msg): pass

    def changed(self, msg):
        msg_type = ChangedStreamMessage(msg['collection'])
        if msg_type == ChangedStreamMessage.USERS:
            self.event('users', msg)
        elif msg_type == ChangedStreamMessage.NOTIFY_USER:
            self.event('notify_user', msg)
        elif msg_type == ChangedStreamMessage.NOTIFY_ROOM:
            self.event('notify_room', msg)
        elif msg_type == ChangedStreamMessage.ROOM_MESSAGES:
            self.event('room_message', msg)

    def room_message(self, msg):
        msg = parse.changed.room_message(msg)
        self.event('room_message::' + msg['type'].name.lower(), msg)

class OverrideClient(Client):
    """
    Simple client which connects to a server and logs in.
    """
    def __init__(self, server, username, password):
        Client.__init__(self, server, username, password)

    async def parse(self, msg, msgtype):
        if msgtype == RawMessageType.ADDED:
            pass
        elif msgtype == RawMessageType.CHANGED:
            await self.on_changed(msg)
        elif msgtype == RawMessageType.UPDATED:
            pass
        elif msgtype == RawMessageType.REMOVED:
            pass
        elif msgtype == RawMessageType.FAILED:
            pass

    async def on_changed(self, msg):
        msg_type = ChangedStreamMessage(msg['collection'])
        if msg_type == ChangedStreamMessage.USERS:
            await self.on_users(msg)
        elif msg_type == ChangedStreamMessage.NOTIFY_USER:
            await self.on_notify_user(msg)
        elif msg_type == ChangedStreamMessage.NOTIFY_ROOM:
            await self.on_notify_room(msg)
        elif msg_type == ChangedStreamMessage.ROOM_MESSAGES:
            await self.on_room_message(parse.changed.room_message(msg))

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

    async def on_users(self, msg):
        pass

    async def on_notify_user(self, msg):
        pass

    async def on_notify_room(self, msg):
        pass

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

