import asyncio
import logging
logging.basicConfig(level='DEBUG')

import unha2.client as client

class ExampleClient(client.Client):
    def __init__(self, server, user, password):
        client.Client.__init__(self, server, user, password)

    async def login(self):
        await super().login()
        rooms = await self.get_subscriptions()
        for room in rooms['update']:
            self.subscribe_to_room(room)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    client = ExampleClient('demo.rocket.chat', 'my_username', 'my_password')
    asyncio.ensure_future(client.handler_loop())
    loop.run_until_complete(client.main(loop))
