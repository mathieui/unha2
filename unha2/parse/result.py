from .. common import ts
from .. model.base import RoomType, User, RoomMessage

def login(result):
    return {
        'user_id': result['id'],
        'token': result['token'],
        'expires': ts(result['tokenExpires'])
    }

def emojis(result):
    return [{
        'id': i['_id'],
        'name': i['name'],
        'aliases': i['aliases'],
        'extension': i['extension'],
        'last_update': ts(i['_updatedAt']['$date']),
    } for i in result]

def load_history(result):
    messages = result['messages'][::-1] # oldest first
    return [{
        'id': i['_id'],
        'room_id': i['rid'],
        'type': RoomMessage(i.get('t', '')),
        'msg': i['msg'],
        'creation_time': ts(i['ts']),
        'user': User(i['u']),
        'update_time': ts(i['_updatedAt']),
        'edition_time': ts(i['editedAt']) if i.get('editedAt') else None,
        'edition_user': i.get('editedBy', ''),
        'urls': i.get('urls', []),
        'attachments': i.get('attachments', []),
        'alias': i.get('alias', ''),
        'avatar': i.get('avatar', ''),
        'groupable': i.get('groupable', False),
        'parse_urls': i.get('parseUrls', False)
    } for i in messages]

def user_roles(result):
    return [{
        'id': i['room-id'],
        'user': User(i['u']),
        'roles': i['roles'],
        'role_id': i['_id']
    } for i in result]

def subscriptions(result):
    return {
        'update': _parse_subscription_update(result['update']),
        'remove': _parse_subscription_remove(result['remove'])
    }

def _parse_subscription_remove(result):
    return [{
        'room_id': i['_id'],
        'deleted_at': ts(i['_deletedAt'])
    } for i in result]

def _parse_subscription_update(result):
    return [{
        'type': RoomType(i['t']),
        'creation_time': ts(i['ts']) if i.get('ts') else None,
        'last_seen_message': ts(i['ls']) if i.get('ls') else None,
        'name': i['name'],
        'room_id': i['rid'],
        'user': User(i['u']),
        'open': i['open'],
        'alert': i['alert'],
        'roles': i.get('roles', []),
        'unread': i['unread'],
        'last_update': ts(i['_updatedAt']),
        'sub_id': i['_id']
    } for i in result]

def users(result):
    return {
        'total_number': result['total'],
        'users': result['records']
    }

def rooms(result):
    return {
        'update': _parse_rooms_update(result['update']),
        'remove': _parse_rooms_remove(result['remove'])
    }

def _parse_rooms_update(rooms):
    return [{
        'id': room['_id'],
        'type': RoomType(room['t']),
        'name': room.get('name', ''),
        'topic': room.get('topic', '')
    } for room in rooms]

def _parse_rooms_remove(rooms):
    return [{'id': room['_id']} for room in rooms]

def permissions(result):
    return [{
        'id': i['_id'],
        'roles': i['roles'],
        'last_update': ts(i['_updatedAt']),
        'meta': i['meta']
    } for i in result]

def join_room(result):
    return result

def open_room(result):
    return result

def create_channel(result):
    return {
        'id': result['rid']
    }

def room_id(result):
    return {'room_id': result}

create_group = create_channel
