from .libshout import libshout
from .libshout import _shout_new, _shout_free
from .libshout import _get_int, _set_int
from .libshout import _get_string, _set_string
from .libshout import _get_bool, _set_bool
from .libshout import _get_audio_info, _set_audio_info
from .libshout import _shout_open, _shout_close
from .libshout import _shout_send, _shout_sync
from .libshout import ShoutProtocol, ShoutFormat


class Shout:
    def __init__(self,
                 host=None,
                 port=8000,
                 username=None,
                 password=None,
                 mount=None,
                 protocol=ShoutProtocol.HTTP,
                 format=ShoutFormat.OGG):
        self.obj = _shout_new()

        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.mount = mount
        self.protocol = protocol
        self.format = format

    def __del__(self):
        _shout_free(self.obj)

    @property
    def host(self):
        return _get_string(self.obj, libshout.shout_get_host)

    @host.setter
    def host(self, value):
        _set_string(self.obj, libshout.shout_set_host, value)

    @property
    def port(self):
        return _get_int(self.obj, libshout.shout_get_port)

    @port.setter
    def port(self, value):
        _set_int(self.obj, libshout.shout_set_port, value)

    @property
    def username(self):
        return _get_string(self.obj, libshout.shout_get_user)

    @username.setter
    def username(self, value):
        _set_string(self.obj, libshout.shout_set_user, value)

    @property
    def password(self):
        return _get_string(self.obj, libshout.shout_get_password)

    @password.setter
    def password(self, value):
        _set_string(self.obj, libshout.shout_set_password, value)

    @property
    def mount(self):
        return _get_string(self.obj, libshout.shout_get_mount)

    @mount.setter
    def mount(self, value):
        _set_string(self.obj, libshout.shout_set_mount, value)

    @property
    def protocol(self):
        return _get_int(self.obj, libshout.shout_get_protocol)

    @protocol.setter
    def protocol(self, value):
        _set_int(self.obj, libshout.shout_set_protocol, value)

    @property
    def format(self):
        return _get_int(self.obj, libshout.shout_get_format)

    @format.setter
    def format(self, value):
        _set_int(self.obj, libshout.shout_set_format, value)

    @property
    def dumpfile(self):
        return _get_string(self.obj, libshout.shout_get_dumpfile)

    @dumpfile.setter
    def dumpfile(self, value):
        _set_string(self.obj, libshout.shout_set_dumpfile, value)

    @property
    def agent(self):
        return _get_string(self.obj, libshout.shout_get_agent)

    @agent.setter
    def agent(self, value):
        _set_string(self.obj, libshout.shout_set_agent, value)

    @property
    def public(self):
        return _get_bool(self.obj, libshout.shout_get_public)

    @public.setter
    def public(self, value):
        _set_bool(self.obj, libshout.shout_set_public, value)

    @property
    def name(self):
        return _get_string(self.obj, libshout.shout_get_name)

    @name.setter
    def name(self, value):
        _set_string(self.obj, libshout.shout_set_name, value)

    @property
    def url(self):
        return _get_string(self.obj, libshout.shout_get_url)

    @url.setter
    def url(self, value):
        _set_string(self.obj, libshout.shout_set_url, value)

    @property
    def genre(self):
        return _get_string(self.obj, libshout.shout_get_genre)

    @genre.setter
    def genre(self, value):
        _set_string(self.obj, libshout.shout_set_genre, value)

    @property
    def description(self):
        return _get_string(self.obj, libshout.shout_get_description)

    @description.setter
    def description(self, value):
        _set_string(self.obj, libshout.shout_set_description, value)

    @property
    def bitrate(self):
        return _get_audio_info(self.obj, "bitrate")

    @bitrate.setter
    def bitrate(self, value):
        _set_audio_info(self.obj, "bitrate", value)

    @property
    def samplerate(self):
        return _get_audio_info(self.obj, "samplerate")

    @samplerate.setter
    def samplerate(self, value):
        _set_audio_info(self.obj, "samplerate", value)

    @property
    def channels(self):
        return _get_audio_info(self.obj, "channels")

    @channels.setter
    def channels(self, value):
        _set_audio_info(self.obj, "channels", value)

    @property
    def quality(self):
        return _get_audio_info(self.obj, "quality")

    @quality.setter
    def quality(self, value):
        _set_audio_info(self.obj, "quality", value)

    def open(self):
        _shout_open(self.obj)

    def close(self):
        _shout_close(self.obj)

    def sync(self):
        _shout_sync(self.obj)

    def send(self, data, size):
        size = len(data)
        _shout_send(self.obj, data, size)
