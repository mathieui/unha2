import json
from datetime import datetime
from uuid import uuid4

def uuid():
    return uuid4().hex

def dumbs(payload):
    return json.dumps([json.dumps(payload)])

def undumbs(payload):
    return json.loads(json.loads(payload)[0])

def ts(obj):
    return datetime.fromtimestamp(obj['$date'] // 1000)
