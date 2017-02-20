import asyncio
from . common import dumbs

class MethodHolder:
    def __init__(self):
        self.awaited_methods = {} # uid → Future

    async def send_method_await(self, ws, uid, msg):
        fut = asyncio.Future()
        self.awaited_methods[uid] = fut
        ws.send_str(dumbs(msg))
        return await fut

    def send_method(self, ws, uid, msg, callback=None):
        if callback:
            fut = asyncio.Future()
            fut.add_done_callback(callback)
            self.awaited[uid] = fut
        ws.send_str(dumbs(msg))

    def recv(self, result):
        uid = result['id']
        awaited = self.awaited_methods.get(uid)
        if awaited:
            awaited.set_result(result)
            del self.awaited_methods[uid]
