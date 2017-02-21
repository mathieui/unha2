from hashlib import sha256

def login_sha256(uid, username, password):
    hashed = sha256(password.encode()).hexdigest()
    msg = {
        'msg': 'method',
        'method': 'login',
        'id': uid,
        'params': [{
            'user': {'username': username},
            'password': {
                'digest': hashed,
                'algorithm': 'sha-256'
            }
        }]
    }
    return msg

def login_resume(uid, token):
    msg = {
        'msg': 'method',
        'method': 'login',
        'id': uid,
        'params': [
            {'user': token}
        ]
    }
    return msg

def get_rooms(uid, date):
    msg = {
        'msg': 'method',
        'method': 'rooms/get',
        'id': uid,
        'params': [
            {'$date': date}
        ]
    }
    return msg

def get_users(uid, room_id, offline_users=False):
    msg = {
        'msg': 'method',
        'id': uid,
        'method': 'getUsersOfRoom',
        'params': [
            room_id,
            offline_users
        ]
    }
    return msg

def get_room_id(uid, room_name):
    msg = {
        'msg': 'method',
        'id': uid,
        'method': 'getRoomByNameOrId',
        'params': [room_name]
    }
    return msg

def load_history(uid, room_id, last_received, quantity, oldest_wanted=None):
    msg = {
        'msg': 'method',
        'method': 'loadHistory',
        'id': uid,
        'params': [
            room_id,
            oldest_wanted,
            quantity,
            last_received
        ]
    }
    return msg

def mark_messages_read(uid, room_id):
    msg = {
        'msg': 'method',
        'method': 'readMessages',
        'id': uid,
        'params': [room_id]
    }
    return msg

def create_channel(uid, name, users=None, readonly=False):
    if users is None:
        users = []
    msg = {
        'msg': 'method',
        'method': 'createChannel',
        'id': uid,
        'params': [
            name,
            users,
            readonly
        ]
    }
    return msg

def create_private_group(uid, name, users=None):
    if users is None:
        users = []
    msg = {
        'msg': 'method',
        'method': 'createPrivateGroup',
        'id': uid,
        'params': [
            name,
            users
        ]
    }
    return msg

def send_text_message(uid, mid, room_id, text):
    msg = {
        'msg': 'method',
        'method': 'sendMessage',
        'id': uid,
        'params': [{
            'id': mid,
            'rid': room_id,
            'msg': text
        }]
    }
    return msg

def set_presence(uid, status):
    assert status in ('online', 'busy', 'away', 'offline')
    msg = {
        'msg': 'method',
        'method': 'UserPresence:setDefaultStatus',
        'id': uid,
        'params': [status]
    }
    return msg

def get_permissions(uid):
    msg = {
        'msg': 'method',
        'method': 'permissions/get',
        'id': uid,
        'params': []
    }
    return msg

def get_user_roles(uid):
    msg = {
        'msg': 'method',
        'method': 'getUserRoles',
        'id': uid,
        'params': []
    }
    return msg

def get_room_roles(uid, room_id):
    msg = {
        'msg': 'method',
        'method': 'getRoomRoles',
        'id': uid,
        'params': [room_id]
    }
    return msg

def star_message(uid, mid, room_id, starred):
    msg = {
        'msg': 'method',
        'method': 'starMessage',
        'id': uid,
        'params': [{
            '_id': mid,
            'rid': room_id,
            'starred': starred
        }]
    }
    return msg

def delete_room(uid, room_id):
    msg = {
        'msg': 'method',
        'method': 'eraseRoom',
        'id': uid,
        'params': [room_id]
    }
    return msg

def archive_room(uid, room_id):
    msg = {
        'msg': 'method',
        'method': 'archiveRoom',
        'id': uid,
        'params': [room_id]
    }
    return msg

def unarchive_room(uid, room_id):
    msg = {
        'msg': 'method',
        'method': 'unarchiveRoom',
        'id': uid,
        'params': [room_id]
    }
    return msg

def join_room(uid, room_id, join_code=None):
    if join_code:
        params = [room_id, join_code]
    else:
        params = [room_id]
    msg = {
        'msg': 'method',
        'method': 'joinRoom',
        'id': uid,
        'params': params
    }
    return msg

def leave_room(uid, room_id):
    msg = {
        'msg': 'method',
        'method': 'leaveRoom',
        'id': uid,
        'params': [room_id]
    }
    return msg

def hide_room(uid, room_id):
    msg = {
        'msg': 'method',
        'method': 'hideRoom',
        'id': uid,
        'params': [room_id]
    }
    return msg

def open_room(uid, room_id):
    msg = {
        'msg': 'method',
        'method': 'openRoom',
        'id': uid,
        'params': [room_id]
    }
    return msg

def fav_room(uid, room_id, fav_status):
    msg = {
        'msg': 'method',
        'method': 'toggleFavorite',
        'id': uid,
        'params': [
            room_id,
            fav_status
        ]
    }
    return msg

def save_room_setting(uid, room_id, setting, value):
    msg = {
        'msg': 'method',
        'method': 'saveRoomSettings',
        'id': uid,
        'params': [
            room_id,
            setting,
            value
        ]
    }
    return msg

def get_subscriptions(uid, date=0):
    return {
        'msg': 'method',
        'method': 'subscriptions/get',
        'id': uid,
        'params': [{'$date': date}]
    }
