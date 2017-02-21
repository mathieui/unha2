import enum
from .. common import ts


class RoomType(enum.Enum):
    CHAT = 'c'
    PRIVATE = 'p'
    DIRECT = 'd'

class RawMessageType(enum.Enum):
    PING = 'ping'
    CONNECTED = 'connected'
    ADDED = 'added'
    CHANGED = 'changed'
    UPDATED = 'updated'
    REMOVED = 'removed'
    RESULT = 'result'
    FAILED = 'failed'
    ERROR = 'error'
    NONE = ''

class User:
    __slots__ = ['id', 'name']
    def __init__(self, obj):
        self.id = obj['_id']
        self.name = obj['username']

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name

    def __repr__(self):
        return '%s[%s]' % (self.name, self.id)

class Subscription:
    def __init__(self, obj):
        self.type = RoomType(obj['t'])
        self.creation_time = ts(obj['ts'])
        self.last_seen_message = ts(obj['ls'])
        self.room_name = obj['name']
        self.room_id = obj['rid']
        self.user = User(obj['u'])
        self.open = obj['open']
        self.alert = obj['alert']
        self.roles = obj.get('roles', [])
        self.unread = obj['unread']
        self.last_update = ts(obj['_updatedAt'])
        self.sub_id = obj[ '_id']

class Message:
    def __init__(self, msg):
        self.id = msg['_id']
        self.room_id = msg['rid']
        self.text = msg['msg']
        self.sent_at = ts(msg['ts'])
        self.user = User(msg['u'])
        self.received_at = ts(msg['_updatedAt'])

        if msg.get('editedAt'):
            self.edited_at = ts(msg['editedAt'])
            self.edited_by = User(msg['editedBy'])
        else:
            self.edited_at = None
            self.edited_by = ''

        self.urls = msg.get('urls', [])
        self.attachments = msg.get('attachments', [])
        self.alias = msg.get('alias', self.user.name)
        self.avatar_url = msg.get('avatar', '')
        self.groupable = msg.get('groupable', False)
        self.parseUrls = msg.get('parseUrls', False)

class UrlMeta:
    def __init__(self, obj):
        self.url = obj['url']
        self.meta = obj['meta']
        self.headers = obj['headers']
        self.parsed_url = obj['parsedUrl']

class Attachment:
    def __init__(self, obj):
        self.image_url = obj['image_url']
        self.color = obj.get('color')
