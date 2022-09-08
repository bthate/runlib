# This file is placed in the Public Domain.
# pylint: disable=C0112,C0103,C0114,C0115,C0116


import os
import pathlib
import time


def cdir(path) -> None:
    if os.path.exists(path):
        return
    if os.sep in path:
        path = os.path.dirname(path)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def elapsed(seconds, short=True) -> str:
    txt = ""
    nsec = float(seconds)
    year = 365*24*60*60
    week = 7*24*60*60
    nday = 24*60*60
    hour = 60*60
    minute = 60
    years = int(nsec/year)
    nsec -= years*year
    weeks = int(nsec/week)
    nsec -= weeks*week
    nrdays = int(nsec/nday)
    nsec -= nrdays*nday
    hours = int(nsec/hour)
    nsec -= hours*hour
    minutes = int(nsec/minute)
    sec = nsec - minutes*minute
    if years:
        txt += "%sy" % years
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += "%sd" % nrdays
    if years and short and txt:
        return txt
    if hours:
        txt += "%sh" % hours
    if nrdays and short and txt:
        return txt
    if minutes:
        txt += "%sm" % minutes
    if hours and short and txt:
        return txt
    if sec == 0:
        txt += "0s"
    else:
        txt += "%ss" % int(sec)
    txt = txt.strip()
    return txt


def fns(path, timed=None) -> list[str]:
    if not path:
        return []
    if not os.path.exists(path):
        return []
    res = []
    dpath = ""
    for rootdir, dirs, _files in os.walk(path, topdown=False):
        if dirs:
            dpath = sorted(dirs)[-1]
            if dpath.count("-") == 2:
                ddd = os.path.join(rootdir, dpath)
                fls = sorted(os.listdir(ddd))
                if fls:
                    opath = os.path.join(ddd, fls[-1])
                    if (
                        timed
                        and "from" in timed
                        and timed["from"]
                        and fntime(opath) < timed["from"]
                       ):
                        continue
                    if timed and timed.to and fntime(opath) > timed.to:
                        continue
                    res.append(opath)
    return sorted(res, key=fntime)


def fntime(daystr) -> float:
    after = 0
    daystr = " ".join(daystr.split(os.sep)[-2:])
    if "." in daystr:
        daystr, after = daystr.rsplit(".")
    tme = time.mktime(time.strptime(daystr, "%Y-%m-%d %H:%M:%S"))
    if after:
        try:
            tme = tme + float(".%s"% after)
        except ValueError:
            pass
    return tme


def spl(txt) -> list:
    try:
        res = txt.split(",")
    except (TypeError, ValueError):
        res = txt
    return [x for x in res if x]
