# This file is placed in the Public Domain.
# pylint: disable=C0112,C0103,C0114,C0115,C0116


"object programming (working directory)"


import os


class Wd:

    workdir = ".op"

    @staticmethod
    def get() -> str:
        return Wd.workdir

    @staticmethod
    def getpath(path) -> str:
        return os.path.join(Wd.workdir, "store", path)

    @staticmethod
    def set(val) -> None:
        Wd.workdir = val

    @staticmethod
    def storedir():
        return os.path.join(Wd.workdir, "store", '')

    @staticmethod
    def types() -> list[str]:
        sdr = Wd.storedir()
        res = []
        for fnm in os.listdir(sdr):
            if fnm not in res:
                res.append(fnm)
        return res
