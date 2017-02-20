from . base import User, RoomType
from .. common import ts

class RoomEvent:
    def __init__(self, msg, roomargs):
        self.id = msg['_id']
        self.room = msg['rid']
        self.time = ts(msg['ts'])
        self.room_type = RoomType(roomargs['roomType'])

class RoomJoined(RoomEvent):
    __slots__ = ['id', 'room', 'user', 'time', 'room_type']
    def __init__(self, msg, roomargs):
        super().__init__(msg, roomargs)
        self.user = User(msg['u'])
    def __repr__(self):
        return '%s joined the room %s' % (self.user, self.room)

class RoomLeft(RoomEvent):
    __slots__ = ['id', 'room', 'user', 'time', 'room_type']
    def __init__(self, msg, roomargs):
        super().__init__(msg, roomargs)
        self.user = User(msg['u'])
    def __repr__(self):
        return '%s left the room %s' % (self.user, self.room)

class RoomAdded(RoomEvent):
    __slots__ = ['id', 'room', 'time', 'user', 'actor', 'room_type']
    def __init__(self, msg, roomargs):
        super().__init__(msg, roomargs)
        self.user = msg['msg']
        self.actor = User(msg['u'])
    def __repr__(self):
        return '%s added %s to the room %s' % (self.actor, self.user, self.room)

class RoomRemoved(RoomEvent):
    __slots__ = ['id', 'room', 'time', 'user', 'actor', 'room_type']
    def __init__(self, msg, roomargs):
        super().__init__(msg, roomargs)
        self.user = msg['msg']
        self.actor = User(msg['u'])
    def __repr__(self):
        return '%s removed %s from the room %s' % (self.actor, self.user, self.room)

class RoomRoleAdded(RoomEvent):
    __slots__ = ['id', 'room', 'role', 'time', 'user', 'actor', 'room_type']
    def __init__(self, msg, roomargs):
        super().__init__(msg, roomargs)
        self.user = msg['msg']
        self.role = msg['role']
        self.actor = User(msg['u'])
    def __repr__(self):
        return '%s gave %s the %s role in %s' % (self.actor, self.user, self.role, self.room)

class RoomRoleRemoved(RoomEvent):
    __slots__ = ['id', 'room', 'role', 'time', 'user', 'actor', 'room_type']
    def __init__(self, msg, roomargs):
        super().__init__(msg, roomargs)
        self.user = msg['msg']
        self.role = msg['role']
        self.actor = User(msg['u'])
    def __repr__(self):
        return '%s removed the %s role from %s in %s' % (self.actor, self.role, self.user, self.room)

class RoomMuted(RoomEvent):
    __slots__ = ['id', 'room', 'time', 'user', 'actor', 'room_type']
    def __init__(self, msg, roomargs):
        super().__init__(msg, roomargs)
        self.user = msg['msg']
        self.actor = User(msg['u'])
    def __repr__(self):
        return '%s muted %s in %s' % (self.actor, self.user, self.room)

class RoomUnmuted(RoomEvent):
    __slots__ = ['id', 'room', 'time', 'user', 'actor', 'room_type']
    def __init__(self, msg, roomargs):
        super().__init__(msg, roomargs)
        self.user = msg['msg']
        self.actor = User(msg['u'])
    def __repr__(self):
        return '%s unmuted %s in %s' % (self.actor, self.user, self.room)

class RoomMessage(RoomEvent):
    __slots__ = ['id', 'room', 'time', 'text', 'user', 'urls', 'reactions', 'room_type']
    def __init__(self, msg, roomargs):
        super().__init__(msg, roomargs)
        self.user = User(msg['u'])
        self.text = msg['msg']
        self.urls = msg.get('urls', [])
        self.reactions = msg.get('reactions', {})
    def __repr__(self):
        return '%s sent on %s: %s' % (self.user, self.room, self.text)

T_TO_OBJ = {
    'uj': RoomJoined,
    'ul': RoomLeft,
    'au': RoomAdded,
    'ru': RoomRemoved,
    'subscription-role-added': RoomRoleAdded,
    'subscription-role-removed': RoomRoleRemoved,
    'user-muted': RoomMuted,
    'user-unmuted': RoomUnmuted,
    'room-changed-topic': lambda *args: None
}
