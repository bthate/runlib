# This file is placed in the Public Domain.


"composition tests"


import unittest


from run import Commands, scan


import bsc


class TestScan(unittest.TestCase):

    def test_composite(self):
        scan(bsc)
        self.assertTrue("cmd" in Commands.cmds)
