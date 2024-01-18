# [![Pushi WebSocket](res/logo.png)](http://pushi.hive.pt)

Simple yet powerful infra-structure for handling of WebSocket connections.

## Objectives

The server itself should be based on a common infra-structure like the one
present in frameworks like node.js that should abstract the socket connection
layer (select layer) on an event driven basis. The infra-structure itself should
be non-blocking and asynchronous for performance and scalability.

The API layer should be provided by a simple WSGI application implemented using
the [Appier Framework](https://github.com/hivesolutions/appier) to keep things
simple and fast.

For persistence the pushi infra-structure uses the MongoDB database infra-structure
to avoid any unwanted complexities and provide fast performance.

## Inspiration

Pushi was heavily inspired by the [Pusher](http://pusher.com) service, and aims
at providing a free alternative to it (for cost reducing).

## Channels

The channel is the base object for communication and there are four types of channels
so that each one has its own objectives.

### Public Channels

Channels that may be subscribed by any connection without any sort of validation.

### Private Channels

Authenticated channels for which the access is constrained to only server side
validated connections. The validation is performed using a REST-JSON based API.

### Presence Channels

Channels that provide extra information on the situation on the channel, for instance
allow the identification of a set of connection using a single `user_id` tag. Using
this approach it's possible to know when a new user connects to a channel and when
one disconnects (no more connections with the same `user_id` are present). These channels
are considered private and so are subject to validation from the server side.

### Personal Channels

This channels provide the capability to aggregate a series of (personal) subscriptions
into a single channel (for simplicity). This way it's easy to aggregate a stream of
notifications that arise from a group of channels. This channel must be used together
with the publish subscribe model. A channel of this type should be named `personal-<user_id>`.

### Peer Channels

Targeted at chat environment allows for the creation of automatic channels for the
various elements (users) that are subscribed to a peer channel. The activation of the
automatic peer channel configuration is archived using the `peer` flag in the `channel_data`
structure upon the subscription of such channel. This channel type **should not be created directly
but instead should be created through presence channels**.

The management of these kind of channels implies that the `peer` advertisement flag is set
for a channel shared among the peers, from that moment the peer is visible to all the
other peers upon subscription of that shared channel. These kind of channels should
be used together with the presence channels.

The naming of these kind of channels will always follow the structure
`peer-base_channel:user_1&user_2&user_3`.

## Persistence

It's possible to use pushi to store messages in the server side in a publish/subscriber
way so that a `user_id` may subscribe for a certain channel even when it's offline.

### Subscribe

To be able to subscribe for a channel use the `apps/<app_id>/subscribe` route with the
`user_id` and the `event` parameters indicating both the id and the name of the event
that should be subscribed.

### Unsubscribe

To revert the subscribe operation one should call the `apps/<app_id>/unsubscribe` route
with the same `user_id` and the `event` parameters.

### Usage

When a user connects to the channel that it has subscribed the last messages are returned
as part of the `channel_data` structure.

## Running

To be able to run the pushi infra-structure under a normal non encrypted connection
and bind to the complete set of network interfaces in the host the following command:

    APP_HOST=0.0.0.0 \
    APP_PORT=8080 \
    SERVER_HOST=0.0.0.0 \
    SERVER_PORT=80 \
    python pushi/src/pushi/base/state.py < /dev/null &> ~/pushi.log &

To be able to run in using SSL encryption additional commands must be used, please note
that the SSL port used by the app is not the default one:

    APP_SERVER=netius \
    APP_HOST=0.0.0.0 \
    APP_PORT=9090 \
    APP_SSL=1 \
    APP_SSL_KEY=/path/to/file.key \
    APP_SSL_CER=/path/to/file.cer \
    SERVER_HOST=0.0.0.0 \
    SERVER_PORT=443 \
    SERVER_SSL=1 \
    SERVER_SSL_KEY=/path/to/file.key \
    SERVER_SSL_CER=/path/to/file.cer \
    python pushi/src/pushi/base/state.py < /dev/null &> ~/pushi.log &

## Quick Start

### Client Side

```javascript
var pushi = new Pushi("YOU_APP_KEY");
pushi.bind("message", function(event, data) {
    jQuery("body").append("<div>" + data + "</div>");
});
```

### Server Side

```python
import pushi

proxy = pushi.Pushi(
    app_id = "YOU_APP_ID",
    app_key = "YOU_APP_KEY",
    app_secret = "YOU_APP_SECRET"
)
proxy.trigger_event(
    channel = "global",
    data = "hello world",
    event = "message"
)
```

## License

Pushi System is currently licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).

## Build Automation

[![Build Status](https://app.travis-ci.com/hivesolutions/pushi.svg?branch=master)](https://travis-ci.com/github/hivesolutions/pushi)
[![Build Status GitHub](https://github.com/hivesolutions/pushi/workflows/Main%20Workflow/badge.svg)](https://github.com/hivesolutions/pushi/actions)
[![Coverage Status](https://coveralls.io/repos/hivesolutions/pushi/badge.svg?branch=master)](https://coveralls.io/r/hivesolutions/pushi?branch=master)
[![PyPi Status](https://img.shields.io/pypi/v/pushi.svg)](https://pypi.python.org/pypi/pushi)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/)
