# This file is placed in the Public Domain.


"console tests"


import unittest


from run import Client


class TestClient(unittest.TestCase):

    def test_console(self):
        clt = Client()
        self.assertEqual(type(clt), Client)
