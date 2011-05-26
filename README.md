Why another SMTP server for node?
=================================

A quick search on the web reveals that there are several implementations of an
[SMTP server for node.js](https://github.com/joyent/node/wiki/modules#smtp). So,
why another implementation?

Of the implementations out there, none seemed to do what I wanted from an SMTP
server, namely emit an event when a message is received. The other
implementations focused on relaying the message. That's certainly not to say
that they are wrong, but what I had in mind was something a little different
from traditional email relay...

TODO: Finish documenting this!