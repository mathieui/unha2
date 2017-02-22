
ALLOWED_USER_SUBS = [
    'notification',
    'rooms-changed',
    'subscriptions-changed',
    'otr',
    'webrtc',
    'message'
]

def sub_notify_user(uid, user_id, sub):
    assert sub in ALLOWED_USER_SUBS
    msg = {
        'msg': 'sub',
        'name': 'stream-notify-user',
        'id': uid,
        'params': [
            '%s/%s' % (user_id, sub),
            False
        ]
    }
    return msg

ALLOWED_ROOM_SUBS = ['typing', 'deleteMessage']

def sub_notify_room(uid, room_id, sub):
    assert sub in ALLOWED_ROOM_SUBS
    msg = {
        'msg': 'sub',
        'name': 'stream-notify-room',
        'id': uid,
        'params': [
            '%s/%s' % (room_id, sub),
            False
        ]
    }
    return msg

# TODO: find out wth is the special __my_messages__ room id
def sub_room_messages(uid, room_id):
    msg = {
        'msg': 'sub',
        'name': 'stream-room-messages',
        'id': uid,
        'params': [
            room_id,
            False
        ]
    }
    return msg

ALLOWED_NOTIFY_SUBS = [
    'roles-change',
    'updateEmojiCustom',
    'deleteEmojiCustom',
    'updateAvatar',
    'public-settings-changed',
    'permissions-changed'
]

def sub_notify_all(uid, sub):
    assert sub in ALLOWED_NOTIFY_SUBS
    msg = {
        'msg': 'sub',
        'name': 'stream-notify-all',
        'id': uid,
        'params': [
            'sub',
            False
        ]
    }
    return msg
