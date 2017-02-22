import enum

from ..model.base import User, RoomType, RoomMessage, ChangedStreamMessage

def _empty(msg):
    pass


def parse_room_message(data):
    msg = data['fields']['args'][0]
    return {
        'id': msg['_id'],
        'room_id': msg['rid'],
        'type': RoomMessage(msg.get('t', '')),
        'creation_time': ts(msg['ts']),
        'msg': msg['msg'],
        'user': User(msg['u']),
        'groupable': msg.get('groupable', False),
        'update_time': ts(msg['_updatedAt']),
        'avatar_url': msg.get('avatar_url', ''),
        'urls': msg.get('urls', []),
        'attachments': msg.get('attachments', []),
        'edited_time': msg['editedAt'] if msg.get('editedAt') else None,
        'edited_by': User(msg['editedBy']) if msg.get('editedBy') else None,
        'parse_urls': msg.get('parseUrls', False),
    }

def parse_url_meta(data):
    return {
        'url': data['url'],
        'meta': data['meta'],
        'headers': data['headers'],
        'parsed_url': data['parsedUrl']
    }


def parse_room_notif(msg):
    pass

def get_collection(msg):
    return msg['collection']

def parse_changed_msg(msg):
    collection = get_collection('msg')
    PARSERS['changed'][collection]

def parse_removed_users(msg):
    user_id = msg['_id']

def parse_room_message(msg):
    message = msg['fields']['args'][0]
    room_args = msg['fields']['args'][1]

    msg_t = msg.get('t')
    if t is None: # message
        return RoomMessage(message, room_args)
    else: # event
        cls = room_event_mapping.get(msg_t)
        if cls is not None:
            return cls(message, room_args)

def parse_notify_user(msg):
    event_name = msg['fields']['eventName']
    event = event_name.split('/')[1]
    args = msg['fields']['args']

def parse_rooms_changed(args):
    type_ = args[0]
    params = args[1]
    room_type = RoomType(params['t'])
    if room_type == RoomType.CHAT:
        pass
    elif room_type == RoomType.PRIVATE:
        pass
    elif room_type == RoomType.DIRECT:
        pass

def parse_changed_chat(params):
    room_id = params['_id']
    room_name = params['name']
    room_topic = params['topic']
    room_muted = params['muted']
    room_jitsitimeout = params['jitsiTimeout']

def parse_changed_direct(params):
    room_id = params['_id']

def parse_changed_private(params):
    pass

