import json
from datetime import datetime
from uuid import uuid4

def uuid():
    return uuid4().hex

def dumbs(payload):
    return json.dumps([json.dumps(payload)])

def ts(obj):
    return datetime.fromtimestamp(obj['$date'])
