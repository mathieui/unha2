from .. model.base import RawMessageType

def msg_type(msg):
    return RawMessageType(msg.get('msg', ''))
