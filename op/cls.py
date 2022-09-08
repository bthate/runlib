# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116


"object programming (classes whitelist)"


class Class:

    cls = {}

    @staticmethod
    def add(clz) -> None:
        Class.cls["%s.%s" % (clz.__module__, clz.__name__)] =  clz

    @staticmethod
    def all():
        return Class.cls.keys()

    @staticmethod
    def full(name) -> list[str]:
        name = name.lower()
        res = []
        for cln in Class.cls:
            if name in cln.split(".")[-1].lower():
                res.append(cln)
        return res

    @staticmethod
    def get(name) -> type[object]:
        return Class.cls.get(name, None)

    @staticmethod
    def remove(name) -> None:
        del Class.cls[name]
