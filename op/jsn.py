# This file is placed in the Public Domain.
# pylint: disable=W0613,W0221,C0112,C0103,C0114,C0115,C0116,R0903


"object programming (json)"


import datetime
import json
import os


from json import JSONDecoder, JSONEncoder


from .obj import Object, update
from .cls import Class
from .utl import cdir
from .wdr import Wd


## json


class ObjectDecoder(JSONDecoder):

    def  __init__(self, *args, **kwargs):
        ""
        JSONDecoder.__init__(self, *args, **kwargs)

    def decode(self, inp, _w=None):
        ""
        value = json.loads(inp)
        return Object(value)

    def raw_decode(self, inp, *args, **kwargs):
        ""
        return JSONDecoder.raw_decode(self, inp, *args, **kwargs)


class ObjectEncoder(JSONEncoder):

    def  __init__(self, *args, **kwargs):
        ""
        JSONEncoder.__init__(self, *args, **kwargs)

    def encode(self, obj):
        ""
        return JSONEncoder.encode(self, obj)

    def default(self, obj):
        ""
        if isinstance(obj, dict):
            return obj.items()
        if isinstance(obj, Object):
            return vars(obj)
        if isinstance(obj, list):
            return iter(obj)
        if isinstance(obj,
                      (type(str), type(True), type(False),
                       type(int), type(float))
                     ):
            return obj
        try:
            return JSONEncoder.default(self, obj)
        except TypeError:
            return str(obj)

    def iterencode(self, obj, *args, **kwargs):
        ""
        return JSONEncoder.iterencode(self, obj, *args, **kwargs)


def dump(obj, opath) -> str:
    cdir(opath)
    with open(opath, "w", encoding="utf-8") as ofile:
        json.dump(
            obj.__dict__, ofile, cls=ObjectEncoder, indent=4, sort_keys=True
        )
    return obj.__stp__


def dumps(obj) -> str:
    return json.dumps(obj, cls=ObjectEncoder)


def hook(hfn) -> Object:
    if hfn.count(os.sep) > 2:
        oname = hfn.split(os.sep)[-3:]
    else:
        oname = hfn.split(os.sep)
    cname = oname[0]
    cls = Class.get(cname)
    if cls:
        obj = cls()
    else:
        obj = Object()
    fnm = os.sep.join(oname)
    load(obj, fnm)
    return obj


def load(obj, opath) -> Object:
    splitted = opath.split(os.sep)
    stp = os.sep.join(splitted[-4:])
    lpath = os.path.join(Wd.workdir, "store", stp)
    if os.path.exists(lpath):
        with open(lpath, "r", encoding="utf-8") as ofile:
            res = json.load(ofile, cls=ObjectDecoder)
            update(obj, res)
    obj.__stp__ = stp


def loads(jss) -> Object:
    return json.loads(jss, cls=ObjectDecoder)


def save(obj) -> str:
    prv = os.sep.join(obj.__stp__.split(os.sep)[:1])
    obj.__stp__ = os.path.join(
                       prv,
                       os.sep.join(str(datetime.datetime.now()).split())
                      )
    opath = Wd.getpath(obj.__stp__)
    dump(obj, opath)
    os.chmod(opath, 0o444)
    return obj.__stp__
