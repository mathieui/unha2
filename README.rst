Unha2
=====

This is a work-in-progress library to interact with Rocket.Chat_ using
websockets (the "realtime API").

The main goal is to be able to build an XMPP client bridge that doesn’t
require webhooks or admin rights, and that appears as a normal XMPP
chatroom (e.g. ``#general%demo.rocket.chat@my.xmpp.server``), in the same
spirit as biboumi_.

Currently, nothing works (experimenting the desired level of abstraction).

Thanks
======

Many things were found out from reading the source of purple-rocketchat_, so
I want to thank its author for taking the time to write the plugin.

.. _Rocket.Chat: https://rocket.chat/
.. _biboumi: https://biboumi.louiz.org/
.. _purple-rocketchat: https://bitbucket.org/EionRobb/purple-rocketchat
