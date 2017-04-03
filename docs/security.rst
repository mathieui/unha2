Security
========

Not much to say about an HTTP/Websocket app, it uses TLS everywhere.
However, it does strike me as odd that the login process involves sending
your hashed password. Although it is nice to see SHA-2 there, it seems like
an afterthought, since it effectively has the same use as a raw password sent
over the wire (no SCRAM or anything). Nice to not leak cleartext in the worst
case, I guess.
