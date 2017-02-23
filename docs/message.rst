Message toplevel
================

- Everything received is a message (is of the shape ``{'msg': 'something'}``.
- Except the useless ``{'server-id': 0}`` at the beginning.

Message types
-------------

- ``ping`` - frequently received - reply with ``{'msg': 'pong'}``
- ``connected`` - received after connecting
- ``ready`` - received after subscribing to an event
- ``result`` - result of a remote method call

- ``added`` - things added to a collection (seen so far: own user, kadira debugging stuff)
- ``changed`` - about everything else (new messages, joins, room events, etc)
- ``removed`` - removed stuff

- ``error`` - error


Collections for the "changed" type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``stream-notify-user``
- ``stream-notify-all``
- ``stream-notify-room``
- ``stream-room-messages``

Sub-types for the "stream-room-messages" event
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each event data in a ``stream-room-messages`` ``changed`` event has a
specific type, accessible at ``t``. Its possible values are:

- ``uj`` - A user joined the room
- ``ul`` - A user left the room
- ``au`` - A user was added to the room by someone
- ``ru`` - A user was removed from the room by someone
- ``user-muted`` - A user was muted
- ``user-unmuted`` - A user was unmuted
- ``subscription-role-added`` - A user got a new role
- ``subscription-role-removed`` - A user lost a role
- ``room_changed_topic`` - The room topic changed
- Nothing - normal message (can be new message, edited message, starred message, pinned message too)

Sub-types for the "stream-notify-user" event
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``notification``
- ``rooms-changed``
- ``subscriptions-changed``
- ``otr``
- ``webrtc``
- ``message``
