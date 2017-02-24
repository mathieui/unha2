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

Those are all notifications you have to subscribe to.
All the notifications have an ``id`` attribute that is set to ``"id"``
for some reason.

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

- ``notification`` - On new message

::

    {
      'msg': 'changed',
      'collection': 'stream-notify-user',
      'id': 'id',
      'fields': {
        'eventName': '<user-id>/notification',
        'args': [
          {
            'title': '@<sender-nickname>',
            'text': '<message-text>',
            'payload': {
              '_id': '<notification-id?>',
              'rid': '<room-id>',
              'sender': {
                '_id': '<sender-user-id>',
                'username': '<sender-nickname>'
              },
              'type': 'd'
            }
          }
        ]
      }
    }

- ``rooms-changed``

::

    {
      'msg': 'changed',
      'collection': 'stream-notify-user',
      'id': 'id',
      'fields': {
        'eventName': '<user-id>/rooms-changed',
        'args': [
          'inserted',
          {
            '_id': '<notification-id?>',
            'name': '<room-name>',
            't': 'p',
            'u': {
              '_id': '<room-host-id>',
              'username': '<host-nickname>'
            },
            'ro': False
          }
        ]
      }
    }

- ``subscriptions-changed`` - On things happening in subscribed rooms?
   - On new message in an existing room

::

    {
      'msg': 'changed',
      'collection': 'stream-notify-user',
      'id': 'id',
      'fields': {
        'eventName': '<user-id>/subscriptions-changed',
        'args': [
          'inserted',
          {
            't': 'p',
            'ts': {'$date': 1487895106540},
            'name': '<room-name>',
            'rid': '<room-id>',
            'u': {
              '_id': '<user-id>', 'username': '<user-nickname>'
             },
             'open': True,
             'alert': False,
             'unread': 0,
             '_updatedAt': {'$date': 1487895106616},
             '_id': '<notification-id?>'
          }
        ]
      }
    }

-
  - On getting added to a room:

::

    {
      'msg': 'changed',
      'collection': 'stream-notify-user',
      'id': 'id',
      'fields': {
        'eventName': '<user-id>/subscriptions-changed',
        'args': [
          'updated',
          {
            't': 'd',
            'ts': {'$date': 1487510338929},
            'ls': {'$date': 1487787132063},
            'name': '<sender-nickname>',
            'rid': '<room-id>',
            'u': {
              '_id': '<user-id>',
              'username': '<user-nickname>'
            },
            'open': True,
            'alert': True,
            'unread': 1,
            '_updatedAt': {'$date': 1487894400304},
            '_id': '<notification-id?>'
          }
        ]
      }
    }

- ``otr``

::

    {
      'msg': 'changed',
      'collection': 'stream-notify-user',
      'id': 'id',
      'fields': {
        'eventName': '<user-id>/otr',
        'args': [
          'handshake',
          {
            'roomId': '<room-id>',
            'userId': '<requester-id>',
            'publicKey': '{"crv":"P-256","ext":true,"key_ops":[],"kty":"EC","x":"joweSiQY7MqoFoLKHelRnfgBiiEMLQ77pNQ8LFvwK-A","y":"Y5ghdabGGy2eZnbPHDimUlTLW2xqsIW_W17P4eOjgGM"}'
          }
        ]
      }
    }

- ``webrtc`` - ? (video/audio conferences go through jitsi meet, afaik)
- ``message`` - ? (not triggered on messages, so far)

Note: many actions generate twice the events if you are subscribed to several
feeds. For example, getting added to a room generates a ``rooms-changed`` and
a ``subscriptions-changed`` event; a new messgaes a ``subscriptions-changed``
and a ``notification``, etc…

Sub-types for the "stream-notify-room" event
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``deleteMessage`` - The only one present in the docs. It doesn’t appear to do anything even on message deletion
- ``typing`` - Typing notifications

::

    {
      'msg': 'changed',
      'collection': 'stream-notify-room',
      'id': 'id',
      'fields': {
        'eventName': '<room-id>/typing',
        'args': ['<user-nick>', user_is_typing (bool)]
      }
    }
