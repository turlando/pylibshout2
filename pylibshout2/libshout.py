from enum import IntEnum

from ctypes import CDLL
from ctypes.util import find_library
from ctypes import c_int, c_void_p, c_char_p, c_size_t

import atexit


class ShoutReturnCode(IntEnum):
    SUCCESS = 0
    INSANE = -1
    NOCONNECT = -2
    NOLOGIN = -3
    SOCKET = -4
    MALLOC = -5
    METADATA = -6
    CONNECTED = -7
    UNCONNECTED = -8
    UNSUPPORTED = -9
    BUSY = 10
    NOTLS = 11
    TLSBADCERT = -12
    RETRY = -13


class ShoutProtocol(IntEnum):
    HTTP = 0
    XAUDIOCAST = 1
    ICY = 2
    ROARAUDIO = 3


class ShoutFormat(IntEnum):
    OGG = 0
    MP3 = 1
    WEBM = 2
    WEBMAUDIO = 3


def check_return_code(f):
    def decorated(obj, *args, **kwargs):
        ret = f(obj, *args, **kwargs)

        if ret != ShoutReturnCode.SUCCESS:
            err = _get_error(obj)
            raise Exception("Error calling {}: {}\n{}"
                            .format(f.__name__, ShoutReturnCode(ret).name,
                                    err))
    return decorated


def _get_error(obj):
    f = libshout.shout_get_error
    f.argtypes = [c_void_p]
    f.restype = c_char_p
    ret = f(obj)
    if not ret:
        raise MemoryError("shout_get_error returned a NULL pointer.")
    return bytes(ret).decode()


def _get_int(obj, f):
    f.restype = c_int
    return f(obj)


@check_return_code
def _set_int(obj, f, n):
    f.argtypes = [c_void_p, c_int]
    return f(obj, n)


def _get_string(obj, f):
    f.restype = c_char_p
    ret = f(obj)
    if not ret:
        raise MemoryError("{} returned a NULL pointer.".format(f.__name__))
    return bytes(ret).decode()


@check_return_code
def _set_string(obj, f, s):
    f.argtypes = [c_void_p, c_char_p]
    return f(obj, s.encode('ascii'))


def _get_bool(obj, f):
    f.restype = c_int
    return bool(f(obj))


def _get_audio_info(obj, name):
    f = libshout.shout_get_audio_info
    f.argtypes = [c_void_p, c_char_p]
    f.restype = c_char_p
    ret = f(obj, name)
    ret = int(ret.decode())
    return ret


@check_return_code
def _set_audio_info(obj, name, value):
    f = libshout.shout_set_audio_info
    f.argtypes = [c_void_p, c_char_p, c_char_p]
    f.restype = c_int
    return f(obj, name, str(value).encode('ascii'))


@check_return_code
def _set_bool(obj, f, b):
    f.argtypes = [c_void_p, c_int]
    return f(obj, int(b))


def _shout_new():
    libshout.shout_new.restype = c_void_p
    obj = libshout.shout_new()
    if not obj:
        raise MemoryError("shout_new returned a NULL pointer.")
    return obj


def _shout_free(obj):
    libshout.shout_free.argtypes = [c_void_p]
    libshout.shout_free(obj)


@check_return_code
def _shout_open(obj):
    libshout.shout_open.argtypes = [c_void_p]
    libshout.shout_open.restype = c_int
    return libshout.shout_open(obj)


@check_return_code
def _shout_close(obj):
    libshout.shout_close.argtypes = [c_void_p]
    libshout.shout_close.restype = c_int
    return libshout.shout_close(obj)


def _shout_sync(obj):
    libshout.shout_sync.argtypes = [c_void_p]
    libshout.shout_sync(obj)


@check_return_code
def _shout_send(obj, data, size):
    libshout.shout_send.argtypes = [c_void_p, c_char_p, c_size_t]
    libshout.shout_send.restype = c_int
    return libshout.shout_send(obj, data, size)


lib_path = find_library('shout')
if not lib_path:
    raise Exception("libshout not found.")

try:
    libshout = CDLL(lib_path)
except OSError as e:
    raise Exception("Error loading libshout: {}".format(e))

libshout.shout_init()
atexit.register(libshout.shout_shutdown)
