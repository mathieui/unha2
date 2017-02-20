Transport
=========


SockJS
------
The RocketChat REST API is well-documented and works well enough, but
you cannot build a bridge with it, as it lacks realtime features (being
a REST API). It is therefore quite useless if you want to create a
third-party client, except if you like http polling every second.

To do that, you have to use the realtime API, which uses SockJS as
middleman to ensure the greatest compatibility with the broken mess
that is the browser ecosystem.

The `SockJs protocol`_ is undocumented, but there is a walkthrough
of unit tests which explains things well enough.

First, you need to open a websocket on ``https://your-host/sockjs/123/client1234/websocket```, where ``123`` is a three-digit, random number (used for load balancing purposes) and ``client1234`` a unique session ID.

Once you have access to the stream, the SockJS protocol consists in chars sent by the server before each data frame:

- ``o`` to start a session
- ``c`` to close a session
- ``h`` to send a heartbeat
- ``a`` to prefix a data frame

Generally, the server will send an ``o`` right after opening the socket, a ``c`` to close it from its side, an ``a`` whenever it has data to send, and the ``h`` can be ignored.

After the ``a`` comes DDP.

DDP
---

DDP is the exchange protocol between Meteorjs applications (client/server).
The gist of it is that you take your data, serialize it as a json string,
put that string as the only element of a json array, then serialize that to
a string.

This gives us, in python:

::
    json.dumps([json.dumps({"a":"b"})])

Which gives us the following string for a frame we send to the server:

::
    ["{\"a\": \"b\"}"]

And, for a frame received from the server, we have to add SockJS, so
we receive:

::
    a["{\"a\": \"b\"}"]


.. _SockJs protocol: https://sockjs.github.io/sockjs-protocol/sockjs-protocol-0.3.html
