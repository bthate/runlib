# This file is placed in the Public Domain.
# pylint: disable=W0613,W0221,C0112,C0103,C0114,C0115,C0116,R0903


"object programming (database)"


import _thread


from .obj import Object, get, items, otype, update
from .cls import Class
from .dft import Default
from .jsn import hook
from .wdr import Wd
from .utl import fns, fntime


## database


dblock = _thread.allocate_lock()


def locked(lock):

    def lockeddec(func, *args, **kwargs):

        def lockedfunc(*args, **kwargs):
            lock.acquire()
            res = None
            try:
                res = func(*args, **kwargs)
            finally:
                lock.release()
            return res

        lockeddec.__wrapped__ = func
        lockeddec.__doc__ = func.__doc__
        return lockedfunc

    return lockeddec


class Db():

    @staticmethod
    def all(otp, timed: dict = None) -> list[Object]:
        result = []
        for fnm in fns(Wd.getpath(otp), timed):
            obj = hook(fnm)
            if "__deleted__" in obj and obj.__deleted__:
                continue
            result.append((fnm, obj))
        if not result:
            return []
        return result

    @staticmethod
    def find(otp, selector=None, index=None, timed=None) -> list[Object]:
        if selector is None:
            selector = {}
        _nr = -1
        result = []
        for fnm in fns(Wd.getpath(otp), timed):
            obj = hook(fnm)
            if selector and not search(obj, selector):
                continue
            if "__deleted__" in obj and obj.__deleted__:
                continue
            _nr += 1
            if index is not None and _nr != index:
                continue
            result.append((fnm, obj))
        return result

    @staticmethod
    def last(otp) -> tuple[str, Object]:
        fnm = fns(Wd.getpath(otp))
        if fnm:
            fnn = fnm[-1]
            return (fnn, hook(fnn))
        return (None, None)

    @staticmethod
    def match(otp, selector=None, index=None, timed=None) -> (str, Object):
        res = sorted(
                     Db.find(otp, selector, index, timed), key=lambda x: fntime(x[0]))
        if res:
            return res[-1]
        return (None, None)


class Selector(Default):

    pass


def find(name, selector=None, index=None, timed=None) -> list[Object]:
    names = Class.full(name)
    if not names:
        names = [x for x in Wd.types() if name in x]
    db = Db()
    result = []
    for nme in names:
        for fnm, obj in db.find(nme, selector, index, timed):
            result.append((fnm, obj))
    return result


def last(obj) -> None:
    db = Db()
    _path, _obj = db.last(otype(obj))
    if _obj:
        update(obj, _obj)


def search(obj, selector) -> bool:
    res = False
    select = Selector(selector)
    for key, value in items(select):
        val = get(obj, key)
        if value in str(val):
            res = True
            break
    return res


Class.add(Default)
Class.add(Object)
Class.add(Selector)
