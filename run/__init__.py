# This file is placed in the Public Domain.


"Prosecutor. Court. Reconsider OTP-CR-117/19."
# This file is placed in the Public Domain.
# pylint: disable=R,C,W,C0302


"runtime"


## import


import inspect
import os
import sys
import traceback


from .obj import Class, Default, Wd, name
from .hdl import Command, Event
from .thr import launch


def __dir__():
    return (
            'Cfg',
            'command',
            'launch',
            'scan',
            'scandir',
           )


__all__ = __dir__()


## define


Cfg = Default()


## utility


def command(cli, txt, event=None):
    evt = event and event() or Event()
    evt.parse(txt)
    evt.orig = repr(cli)
    cli.handle(evt)
    return evt


def from_exception(exc, txt="", sep=" "):
    result = []
    for frm in traceback.extract_tb(exc.__traceback__):
        fnm = os.sep.join(frm.filename.split(os.sep)[-2:])
        result.append(f"{fnm}:{frm.lineno}")
    nme = name(exc)
    res = sep.join(result)
    return f"{txt} {res} {nme}: {exc}"


def savepid(name=None):
    if not name:
        name = sys.argv[0]
    k = open(os.path.join(Wd.workdir, '%s.pid' % name), "w", encoding='utf-8')
    k.write(str(os.getpid()))
    k.close()


def scan(mod):
    scancls(mod)
    for key, cmd in inspect.getmembers(mod, inspect.isfunction):
        if key.startswith("cb"):
            continue
        names = cmd.__code__.co_varnames
        if "event" in names:
            Command.add(cmd)


def scancls(mod):
    for _k, clz in inspect.getmembers(mod, inspect.isclass):
        Class.add(clz)


def scandir(path, func):
    res = []
    if not os.path.exists(path):
        return res
    for _fn in os.listdir(path):
        if _fn.endswith("~") or _fn.startswith("__"):
            continue
        try:
            pname = _fn.split(os.sep)[-2]
        except IndexError:
            pname = path
        mname = _fn.split(os.sep)[-1][:-3]
        res.append(func(pname, mname))
    return res
