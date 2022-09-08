# This file is placed in the Public Domain.
# pylint: disable=W0613,W0221,C0112,C0103,C0114,C0115,C0116,R0903,W0622


"object programming"


import datetime
import os
import types


def __dir__():
    return (
            'Class',
            'Default',
            'Object',
            'Wd',
            'delete',
            'edit',
            'format',
            'get',
            'items',
            'jsn',
            'keys',
            'name',
            'otype',
            'register',
            'save',
            'types',
            'update',
            'values'
           )

## object


class Object:

    __slots__ = ('__dict__','__stp__')

    def __init__(self, *args, **kwargs):
        object.__init__(self)
        self.__stp__ = os.path.join(
            otype(self),
            os.sep.join(str(datetime.datetime.now()).split()),
        )
        if args:
            update(self, args[0])

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self. __dict__)


def delete(obj, key) -> None:
    delattr(obj, key)


def edit(obj, setter) -> None:
    for key, value in items(setter):
        register(obj, key, value)


def format(obj, args="", skip="", plain=False) -> str:
    res = []
    keyz = []
    if "," in args:
        keyz = args.split(",")
    if not keyz:
        keyz = keys(obj)
    for key in keyz:
        if key.startswith("_"):
            continue
        if skip and "," in skip:
            skips = skip.split(",")
            if key in skips:
                continue
        value = getattr(obj, key, None)
        if not value:
            continue
        if " object at " in str(value):
            continue
        txt = ""
        if plain:
            txt = str(value)
        elif isinstance(value, str) and len(value.split()) >= 2:
            txt = '%s="%s"' % (key, value)
        else:
            txt = '%s=%s' % (key, value)
        res.append(txt)
    return " ".join(res)


def get(obj, key, default=None) -> type(object):
    return obj.__dict__.get(key, default)


def name(obj) -> str:
    typ = type(obj)
    if isinstance(typ, types.ModuleType):
        return obj.__name__
    if "__self__" in dir(obj):
        return "%s.%s" % (obj.__self__.__class__.__name__, obj.__name__)
    if "__class__" in dir(obj) and "__name__" in dir(obj):
        return "%s.%s" % (obj.__class__.__name__, obj.__name__)
    if "__class__" in dir(obj):
        return obj.__class__.__name__
    if "__name__" in dir(obj):
        return obj.__name__
    return None


def items(obj) -> list[str]:
    if isinstance(obj, type({})):
        return obj.items()
    return obj.__dict__.items()


def keys(obj) -> list[str]:
    return obj.__dict__.keys()


def otype(obj) -> str:
    return str(type(obj)).split()[-1][1:-2]


def register(obj, key, value) -> None:
    setattr(obj, key, value)


def update(obj, data) -> None:
    if isinstance(data, type({})):
        obj.__dict__.update(data)
    else:
        obj.__dict__.update(vars(data))


def values(obj) -> list[type(object)]:
    return obj.__dict__.values()
