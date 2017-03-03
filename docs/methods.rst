Methods
=======

"methods" are the way of doing RPC in Rocket over a websocket stream.
They are simply a json object containing ``msg: "method"`` and a unique
identifier to be able to distinguish the result from the stream.

After the server returned it, results are wrapped in a json object with
``msg: "result"`` and contained inside a ``result`` sub-object.

However, do not expect consistency in the type of the result payload,
as it can be:

- `a list containing exactly one element`_
- 1_
- nothing_
- `an object`_
- `nothing but replaced with an "error" element`_
- `a boolean`_

Undocumented but useful methods
===============================

- ``getRoomIdByNameOrId`` - As it sounds. It is a necessity.
- ``channelsList`` - List channels with a filter
- ``getUsersOfRoom`` - Get the userlist + number of users
- ``readMessages`` - Mark messages as read

.. _1:  https://rocket.chat/docs/developer-guides/realtime-api/method-calls/delete-rooms/
.. _a list containing exactly one element: https://rocket.chat/docs/developer-guides/realtime-api/method-calls/create-channels/
.. _a list of multiple things: https://rocket.chat/docs/developer-guides/realtime-api/method-calls/get-subscriptions/
.. _nothing but replaced with an "error" element: https://rocket.chat/docs/developer-guides/realtime-api/method-calls/login/

.. _nothing: https://rocket.chat/docs/developer-guides/realtime-api/method-calls/archive-rooms/
.. _an object: https://rocket.chat/docs/developer-guides/realtime-api/method-calls/load-history/
.. _a boolean: https://rocket.chat/docs/developer-guides/realtime-api/method-calls/joining-channels/
