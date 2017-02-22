import asyncio
from . transport import websocket as sock

class AsyncHolder:
    """
    Wrapper for sending subscriptions and methods.
    Takes callbacks or (asyncio-)block until the
    result is received.
    """
    def __init__(self):
        self.awaited_subs = {} # uid → Future
        self.awaited_methods = {} # uid → Future

    async def send_sub(self, ws, uid, msg):
        fut = asyncio.Future()
        self.awaited_subs[uid] = fut
        sock.send(ws, msg)
        return await fut

    def send_sub_noblock(self, ws, uid, msg, callback=None):
        if callback:
            fut = asyncio.Future()
            fut.add_done_callback(callback)
            self.awaited[uid] = fut
        sock.send(ws, msg)

    async def send_method(self, ws, uid, msg):
        fut = asyncio.Future()
        self.awaited_methods[uid] = fut
        sock.send(ws, msg)
        return await fut

    def send_method_noblock(self, ws, uid, msg, callback=None):
        if callback:
            fut = asyncio.Future()
            fut.add_done_callback(callback)
            self.awaited[uid] = fut
        sock.send(ws, msg)

    def recv_result(self, result):
        uid = result['id']
        awaited = self.awaited_methods.get(uid)
        if awaited:
            awaited.set_result(result)
            del self.awaited_methods[uid]

    def recv_ready(self, ready):
        uid = ready['subs'][0]
        awaited = self.awaited_subs.get(uid)
        if awaited:
            awaited.set_result(ready)
            del self.awaited_subs[uid]

    def recv(self, msg):
        if msg['msg'] == 'result':
            self.recv_result(msg)
        elif msg['msg'] == 'ready':
            self.recv_ready(msg)
