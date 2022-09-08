# This file is placed in the Public Domain.


from setuptools import setup


def read():
    return open("README.rst", "r").read()


setup(
    name="runlib",
    version="100",
    url="https://github.com/bthate/runlib",
    author="Bart Thate",
    author_email="bthate67@gmail.com",
    description="python3 runtime library",
    long_description=read(),
    license="Public Domain",
    packages=["run"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Public Domain",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ],
)
