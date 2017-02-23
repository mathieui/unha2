import json
from datetime import datetime
from uuid import uuid4

def uuid() -> str:
    return uuid4().hex

def dumbs(payload: dict) -> str:
    return json.dumps([json.dumps(payload)])

def undumbs(payload: str) -> dict:
    return json.loads(json.loads(payload)[0])

def ts(obj: dict) -> datetime:
    return datetime.fromtimestamp(obj['$date'] // 1000)
