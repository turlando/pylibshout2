# pylibshout2

A _not-so-pythonic_ binding to libshout2.

## Missing

* Only OGG streaming over HTTP protocol has been tested so far.
* `shout_metadata_new()`, `shout_metadata_free()` and `shout_metadata_add()`
  have not been ported yet.

Everything else should work fine.

## Installing

Make sure you have `libshout.so.2` in your `LD_LIBRARY_PATH`, then just run
`python3 setup.py install`.

## Usage

```python
from pylibshout2 import Shout

shout = Shout(
    host='localhost',
    username='source',
    password='hackme',
    mount='/pylibshout2')
```

These are the minimum required parameters to establish a connection to the
Icecast server. The protocol and the format will respectively default to HTTP
and OGG, wich you can still specify at object-creation time adding as follows:

```python
from pylibshout2 import Shout, ShoutProtocol, ShoutFormat

shout = Shout(
    host='localhost',
    port=8000,
    username='source',
    password='hackme',
    mount='/pylibshout2',
    protocol=ShoutProtocol.ICY,
    format=ShoutFormat.MP3)
```

You can change all those params (and more) until you perform `shout.open()`
that will actually connect to the server and create the stream.

```python
from pylibshout2 import Shout, ShoutProtocol, ShoutFormat

shout = Shout()

shout.host = 'localhost'
shout.port = 8000
shout.username = 'source'
shout.password = 'hackme'
shout.mount = '/pylibshout2'
shout.protocol = ShoutProtocol.HTTP
shout.format = ShoutFormat.OGG

shout.dumpfile = False
shout.agent = 'pylibshout2/0.0.1'
shout.public = True

shout.name = "Awesome stream"
shout.url = "https://github.com/turlando/pylibshout2"
shout.genre = "Run & Blame"

shout.bitrate = 192
shout.samplerate = 44100
shout.channels = 2
shout.quality = 6
```

Please refer to libshout2 documentation for more information.

To stream a file just add:

```python

with open('some/path', 'rb') as fp:
    while True:
        chunk = fp.read(4096)
        if not chunk:
            break
        shout.send(chunk, 4096)
        shout.sync()
```

While the rest of the library is kinda pythonic, this is definitely not and
also ugly in my opinion. The send() and sync() methods will be kept of course,
but I want to build a more friendly way to send a stream in the future on top
of those.

Don't forget to close the stream afterwards.

```python
shout.close()
```
