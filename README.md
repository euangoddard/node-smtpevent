Why another SMTP server for node?
=================================

A quick search on the web reveals that there are several implementations of an
[SMTP server for node.js](https://github.com/joyent/node/wiki/modules#smtp). So,
why another implementation?

Of the implementations out there, none seemed to do what I wanted from an SMTP
server, namely emit an event when a message is received. The other
implementations focused on relaying the message. That's certainly not to say
that they are wrong, but what I had in mind was something a little different
from traditional email relay.

As a web developer, I often come across situations where being able to interact
with a web site via email might come in handy and I would like the toolset to
be able to do this. Consider the following workflows:

Unsubscribe from mail list
--------------------------

Many services which send bulk email provide some unsubscribe mechanism for their
mail shots. Some have a click through to a web page to change your preferences,
but others have a `mailto:` link to, e.g., _unsubscribe@example.com_. In this
case an SMTP daemon based on node-smtpevent, would take the from address and use
this to process the unsubscribe request.

Reply to forum thread
---------------------

Web forums often offer a mechanism to keep contributors up-to-date with the
latests posts in a forum thread. If you want to quickly contribute to the thread
without visiting the web site (e.g. from your smart phone) it may be easier to
simply reply to the email notification. In this case the daemon would route the
incoming message back into the forum thread and attribute it using data encoded
in the to address. 