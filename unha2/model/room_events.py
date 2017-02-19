import enum
from datetime import datetime

class RoomType(enum.Enum):
    CHAT = 'c'
    PRIVATE = 'p'
    DIRECT = 'd'

class RoomEvent:
    def __init__(self, msg, roomargs):
        self.id = msg['_id']
        self.room = msg['rid']
        self.time = datetime.fromtimestamp(msg['ts']['$date'] / 1000)
        self.room_type = RoomType(roomargs['roomType'])

class RoomJoined(RoomEvent):
    __slots__ = ['id', 'room', 'userid', 'username', 'time', 'room_type']
    def __init__(self, msg, roomargs):
        super().__init__(msg, roomargs)
        self.userid = msg['u']['_id']
        self.username = msg['u']['username']
    def __repr__(self):
        return '%s joined the room %s' % (self.username, self.room)

class RoomLeft(RoomEvent):
    __slots__ = ['id', 'room', 'userid', 'username', 'time', 'room_type']
    def __init__(self, msg, roomargs):
        super().__init__(msg, roomargs)
        self.userid = msg['u']['_id']
        self.username = msg['u']['username']
    def __repr__(self):
        return '%s left the room %s' % (self.username, self.room)

class RoomAdded(RoomEvent):
    __slots__ = ['id', 'room', 'time', 'user', 'actor', 'actorid', 'room_type']
    def __init__(self, msg, roomargs):
        super().__init__(msg, roomargs)
        self.user = msg['msg']
        self.actorid= msg['u']['_id']
        self.actor = msg['u']['username']
    def __repr__(self):
        return '%s added %s to the room %s' % (self.actor, self.user, self.room)

class RoomRemoved(RoomEvent):
    __slots__ = ['id', 'room', 'time', 'user', 'actor', 'actorid', 'room_type']
    def __init__(self, msg, roomargs):
        super().__init__(msg, roomargs)
        self.user = msg['msg']
        self.actorid= msg['u']['_id']
        self.actor = msg['u']['username']
    def __repr__(self):
        return '%s removed %s from the room %s' % (self.actor, self.user, self.room)

class RoomRoleAdded(RoomEvent):
    __slots__ = ['id', 'room', 'role', 'time', 'user', 'actor', 'actorid', 'room_type']
    def __init__(self, msg, roomargs):
        super().__init__(msg, roomargs)
        self.user = msg['msg']
        self.role = msg['role']
        self.actorid= msg['u']['_id']
        self.actor = msg['u']['username']
    def __repr__(self):
        return '%s gave %s the %s role in %s' % (self.actor, self.user, self.role, self.room)

class RoomRoleRemoved(RoomEvent):
    __slots__ = ['id', 'room', 'role', 'time', 'user', 'actor', 'actorid', 'room_type']
    def __init__(self, msg, roomargs):
        super().__init__(msg, roomargs)
        self.user = msg['msg']
        self.role = msg['role']
        self.actorid= msg['u']['_id']
        self.actor = msg['u']['username']
    def __repr__(self):
        return '%s removed the %s role from %s in %s' % (self.actor, self.role, self.user, self.room)

class RoomMuted(RoomEvent):
    __slots__ = ['id', 'room', 'time', 'user', 'actor', 'actorid', 'room_type']
    def __init__(self, msg, roomargs):
        super().__init__(msg, roomargs)
        self.user = msg['msg']
        self.actorid= msg['u']['_id']
        self.actor = msg['u']['username']
    def __repr__(self):
        return '%s muted %s in %s' % (self.actor, self.user, self.room)

class RoomUnmuted(RoomEvent):
    __slots__ = ['id', 'room', 'time', 'user', 'actor', 'actorid', 'room_type']
    def __init__(self, msg, roomargs):
        super().__init__(msg, roomargs)
        self.user = msg['msg']
        self.actorid= msg['u']['_id']
        self.actor = msg['u']['username']
    def __repr__(self):
        return '%s unmuted %s in %s' % (self.actor, self.user, self.room)

class RoomMessage(RoomEvent):
    __slots__ = ['id', 'room', 'time', 'text', 'username', 'urls', 'reactions', 'userid', 'room_type']
    def __init__(self, msg, roomargs):
        super().__init__(msg, roomargs)
        self.username = msg['u']['username']
        self.userid = msg['u']['_id']
        self.text = msg['msg']
        self.urls = msg.get('urls', [])
        self.reactions = msg.get('reactions', {})
    def __repr__(self):
        return '%s sent on %s: %s' % (self.username, self.room, self.text)

